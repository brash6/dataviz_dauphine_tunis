import numpy as np
from scipy import stats


def promo_detector(data,
                   min_sales_volume=0, min_sales_value=0,
                   method='Mean', nb_months=3, discount_threshold=0.1, align_center=False,
                   io_detector=False, z_score=3):
    """
    Estimate the promotion flag
    Inputs:
        - data: pandas dataframe
        - min_sales_volume: quantity sales drop line considered in the valuation (minimum quantity volume to be considered)
        - min_sales_value: value sales drop line considered in the valuation (minimum sales value in euros to be considered)
        - method: price averaging method ('Mean', 'Median', 'Quantile75', 'Second highest')
        - nb_months: number of months as averaging window size
        - discount_threshold: daily price < (1-discount_threshold) * period price → promo✓
        - align_center: window align center (boolean)
        - io_detector: i/o promotion detector check box (if true: detect i/o sales as promo)
        - z_score: z-score [(𝑥−𝜇)/𝜎] value to detect i/o values (high z-score means the data point is many standard deviations away from the mean)
    Return:
        - data: pandas dataframe with (promo_flag_estimator) column added
    """
    if method == 'Mean':
        data = data.assign(
            avg_period_price=data.rolling(nb_months * 30, min_periods=1, center=align_center).avg_daily_price.mean())
    elif method == 'Median':
        data = data.assign(
            avg_period_price=data.rolling(nb_months * 30, min_periods=1, center=align_center).avg_daily_price.median())
    elif method == 'Quantile75':
        data = data.assign(
            avg_period_price=data.rolling(nb_months * 30, min_periods=1, center=align_center).avg_daily_price.quantile(0.75))
    else:
        if align_center:
            for i in range(0, len(data)):
                data.loc[i, 'avg_period_price'] = list(data.loc[i - (nb_months * 15):i + (nb_months * 15), 'avg_daily_price'].drop_duplicates().nlargest(2).values)[-1]  # 2nd highest price
        else:
            for i in range(0, len(data)):
                data.loc[i, 'avg_period_price'] = list(data.loc[i - (nb_months * 30):i, 'avg_daily_price'].drop_duplicates().nlargest(2).values)[-1]  # 2nd highest price

    # Set promo flag using the discount_threshold
    data["promo_flag_estimator"] = [1 if d <= ((1 - discount_threshold) * p) else 0 for (d, p) in zip(data['avg_daily_price'], data['avg_period_price'])]

    # Set I/O detected as promo
    if io_detector:
        io_indexes = data.index[(np.abs(stats.zscore(data['sales'])) > z_score)].tolist()
        data.loc[io_indexes, 'promo_flag_estimator'] = 1

    # Consider drop line value for minimum sales (ignore day promos with less amount of sales value)
    data["promo_flag_estimator"] = data["promo_flag_estimator"] * [1 if x >= min_sales_volume else 0 for x in data['quantity']]
    data["promo_flag_estimator"] = data["promo_flag_estimator"] * [1 if x >= min_sales_value else 0 for x in data['sales']]

    return data
