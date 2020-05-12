from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.base_spec_check import BaseK8Check


class MinimizeCapabilities(BaseK8Check):

    def __init__(self):
        # CIS-1.5 5.2.9
        name = "Minimize the admission of containers with capabilities assigned"
        id = "CKV_K8S_37"
        supported_kind = ['containers', 'initContainers']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def get_resource_id(self, conf):
        return conf['parent'] + '.securityContext.capabilities.drop'

    def scan_spec_conf(self, conf):
        if "securityContext" in conf:
            if "capabilities" in conf["securityContext"]:
                if "drop" in conf["securityContext"]["capabilities"]:
                    for d in conf["securityContext"]["capabilities"]["drop"]:
                        if "ALL" in d:
                            return CheckResult.PASSED
        return CheckResult.FAILED

check = MinimizeCapabilities()