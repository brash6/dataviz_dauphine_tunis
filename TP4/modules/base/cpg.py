
class CPG():
    def __init__(self, cpg_table, dict_user_attributes):
        self.tenant_id = dict_user_attributes["tenant_id"]
        self.cpg_table = cpg_table
        self.cpg_tenant_project_id = dict_user_attributes["cpg_tenant_project_id"]
        self.project_id = dict_user_attributes["project_id"]
        self.cpg_company = dict_user_attributes["cpg_company"]
        self.cpg_country = dict_user_attributes["country"]
        self.supplier_cpg = dict_user_attributes["supplier"]
        self.global_partitions = dict_user_attributes["global_partitions"]
        self.local_partitions = dict_user_attributes["local_partitions"]
        self.country_partition = dict_user_attributes["country_partition"]
        self.is_custom_taxonomy = dict_user_attributes["is_custom_taxonomy"]
        self.load_custom_taxonomy = False
