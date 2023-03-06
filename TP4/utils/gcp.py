import asyncio
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta

import aiohttp
import async_timeout
import google.auth
import pandas as pd
import panel as pn
import pyarrow as pa
import redis
from logzero import logger

from TP4.constants.constants import (
    DATAFRAME_EXPIRY_SECONDS,
    DPS_API_KEY,
    DPS_HOST,
    DPS_TEAM_NAME,
    ENV,
    ENV_CERT,
    ENV_DEMO,
    ENV_DEV,
    ENV_IRI,
    ENV_POC_SKY,
    ENV_PROD,
    FILTERS_EXPIRY_SECONDS,
    METRICS_SERVICE_API_KEY,
    METRICS_SERVICE_HOST,
    REDIS_HOST,
    REDIS_PORT,
)

DASHBOARD_USAGE_URL_TIMEOUT = 60
DASHBOARD_USAGE_LIMIT_PER_HOST = 5


def execute_multiple_queries_at_once(list_functions, filters):
    with ThreadPoolExecutor() as executor:
        if isinstance(filters, list):
            if len(list_functions == len(filters)):
                futures = [executor.submit(f, filter) for f, filter in zip(list_functions, filters)]
        else:
            futures = [executor.submit(f, filters) for f in list_functions]
        all_results = []
        for idx, future in enumerate(as_completed(futures)):
            result, index = future.result()
            all_results.append([result, index])
        all_results = sorted(all_results, key=lambda x: x[-1])
    all_dataframe = [result[0] for result in all_results]
    return all_dataframe


def multithread_queries_execution_for_monitoring(list_functions, table_names, countries, time_period_types, positions):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(f, table_name, country, time_period_type, position) for
                   f, table_name, country, time_period_type, position in zip(list_functions, table_names, countries,
                                                                             time_period_types, positions)]
        all_results = []
        for idx, future in enumerate(as_completed(futures)):
            result, index = future.result()
            all_results.append([result, index])
        all_results = sorted(all_results, key=lambda x: x[-1])
    all_dataframe = [result[0] for result in all_results]
    return all_dataframe


def get_dashboard_identifier_from_session() -> str:
    """
    Get the dashboard_identifier if from the app url
    return: dashboard_identifier
    """
    # The app_url is of the form /xxxxx so remove the first character
    try:
        return pn.state.app_url[1:]
    except:
        return "No ID"


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_df_from_redis(query):
    r = get_redis()
    context = pa.default_serialization_context()
    try:
        df_from_redis = context.deserialize(r.get(query))
        df = df_from_redis.copy()
        del df_from_redis
    except:
        df = "Empty"
    return df, r, context


def get_date_from_redis(table_name):
    r = get_redis()
    context = pa.default_serialization_context()
    try:
        date = context.deserialize(r.get(table_name))
    except:
        date = "Empty"
    return date, r, context


def set_df_to_redis(query, df, redis_client, context):
    try:
        redis_client.set(query, context.serialize(df).to_buffer().to_pybytes(),
                         ex=timedelta(seconds=DATAFRAME_EXPIRY_SECONDS))
    except:
        return None


def set_last_date_to_redis(table_name, last_modification_date, redis_client, context):
    try:
        redis_client.set(table_name, context.serialize(last_modification_date).to_buffer().to_pybytes(),
                         ex=timedelta(seconds=FILTERS_EXPIRY_SECONDS))
    except:
        return None


def replace_invalid_characters_in_labels(labels):
    """
    Ensures label keys and values contain only characters allowed by BigQuery.
    For label requirements, see:
    https://cloud.google.com/bigquery/docs/labels-intro#requirements
    return: fixed_labels
    """
    if labels is None or len(labels) == 0:
        return None

    valid_labels = {}

    for k, v in labels.items():
        # Keys have a minimum length of 1 character and cannot be empty.
        if k is None or len(k) <= 1:
            continue

        # Keys can contain only lowercase letters, numeric characters, underscores, and dashes.
        k = re.sub('[^a-z0-9_-]', '_', k.lower())  # Anything else convert to underscore

        # Keys must start with a lowercase letter or international character.
        if not k[0].islower():
            k = "key_" + k

        # Keys have a maximum length of 63 characters.
        k = k[:63]

        # Values can be empty, and have a maximum length of 63 characters.
        if v is not None:
            # Values can contain only lowercase letters, numeric characters, underscores, and dashes.
            # To be able to convert email addresses back
            v = re.sub('[@]', '_at_', v.lower())
            v = re.sub('[.]', '_dot_', v)
            v = re.sub('[+]', '_plus_', v)
            v = re.sub('[^a-z0-9_-]', '_', v)  # Anything else convert to underscore
            v = v[:63]

        # Finally, add the valid key/value pair to the return labels
        valid_labels[k] = v

    return valid_labels


def flushall():
    redis_client = get_redis()
    redis_client.flushall()


def check_emptiness_of_dataframes(list_of_dfs):
    results = []
    for df in list_of_dfs:
        if df.shape[0] > 0:
            results.append(True)
        else:
            results.append(False)
    return results


def save_configurations(table_ref, configurations_dict):
    df_configurations = pd.DataFrame.from_dict([configurations_dict])
    df_configurations.to_gbq(destination_table=table_ref, if_exists="append")


async def send_dashboard_usage_async(url: str, headers: dict, dashboard_identifier: str, usage_data: dict):
    """Post the dashboard usage data asynchronously.

    Args:
        url: DPS url
        headers: request headers
        dashboard_identifier: dashboard identifier
        usage_data: request payload
    Returns:
        Dict: Dashboard validation result
    """
    try:
        logger.info(f"Sending DPS dashboards usage for dashboard_identifier: {dashboard_identifier}")

        connector = aiohttp.TCPConnector(limit_per_host=DASHBOARD_USAGE_LIMIT_PER_HOST)
        async with aiohttp.ClientSession(connector=connector) \
                as session, async_timeout.timeout(DASHBOARD_USAGE_URL_TIMEOUT):
            async with session.post(url, headers=headers, data=json.dumps(usage_data)) as response:
                await response.text()

        logger.info(f"DPS dashboards usage endpoint response status: {response.status}")
    except Exception as e:
        logger.error(f"Error sending usage data for dashboard_identifier: {dashboard_identifier} to DPS url: {url}, "
                     f"error: {str(e)}")


def get_all_redis_keys_from_string(string):
    r = get_redis()
    list_key = []
    for key in r.scan_iter(f"*{string}*"):
        list_key.append(key)
    return list_key


def get_all_redis_keys_from_list_of_string(list_of_string):
    list_complete = []
    for string in list_of_string:
        if isinstance(string, str):
            list_keys = get_all_redis_keys_from_string(string)
            list_complete.append(list_keys)
    if len(list_complete) > 0:
        list_right = list_complete[0]
    else:
        return None
    for i in range(1, len(list_complete)):
        list_right = list(set(list_right) & set(list_complete[i]))
    return list_right


def delete_redis_key_from_cache(key):
    r = get_redis()
    r.delete(key)


def delete_all_redis():
    r = get_redis()
    r.flushall()
