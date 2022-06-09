import os
from string import Template
from typing import List

from .base import Base
from .models import ConfigFile, Host
from .frameworks.emulation import EmulationPhase, EmulationPlanDetails


class RunList(Base):

    EMULATION_PATTERN = Template("$adversary/Emulation_Plan/yaml/*.yaml")

    def __init__(self, 
        adversary: str = None, 
        techniques: List = [], 
        test_guids: List = [], 
        host_list: List[Host] = [], 
        config_file: ConfigFile = None
    ):
        self.adversary = adversary
        self.techniques = techniques
        self.test_guids = test_guids
        self.host_list = host_list
        self.config_file = config_file

    def _get_content(self, pattern):
        return self._find_content(
            path=Base.CONFIG.content_path,
            pattern=pattern
        )

    def _get_emulation_hosts(self, name):
        host_list = []
        if self.adversary.upper() == name.upper() and self.host_list:
            host_list.extend(self.host_list)
        if self.config_file and self.config_file.frameworks.adversary_emulations.tests:
            for test in self.config_file.frameworks.adversary_emulations.tests:
                if test.name.upper() == name.upper():
                    if test.inventories and self.config_file.inventory:
                        for inventory in self.config_file.inventory:
                            if inventory.name in test.inventories:
                                host_list.extend(inventory.hosts)
        return host_list

    def _build_emulation_run_list(self):
        content = set()
        if self.adversary:
            self.__logger.info(f"Getting content from adversary '{self.adversary}'.")
            content.update(self._get_content(
                pattern=self.EMULATION_PATTERN.substitute(
                    adversary=self.adversary
                )
            ))
        if self.config_file and self.config_file.frameworks.adversary_emulations.tests:
            for test in self.config_file.frameworks.adversary_emulations.tests:
                self.__logger.info(f"Getting content from adversary '{test.name}'.")
                self.__logger.info(self.EMULATION_PATTERN.substitute(
                        adversary=test.name
                    ))
                content.update(self._get_content(
                    pattern=self.EMULATION_PATTERN.substitute(
                        adversary=test.name.lower()
                    )
                ))
        return_list = []
        for item in content:
            name = self._get_file_name(item)
            loaded_content = self.load_yaml(str(item))
            if loaded_content:
                phase_list = []
                for i in loaded_content:
                    if not i.get('emulation_plan_details') and i.get('id'):
                        phase_list.append(EmulationPhase(**i))
                emulation = [x for x in loaded_content if x.get('emulation_plan_details')]
                if emulation:
                    emulation = emulation[0]
                    emulation = emulation.pop('emulation_plan_details')
                emulation.update({
                    'path': os.path.dirname(str(item)),
                    'phases': phase_list,
                    'hosts': self._get_emulation_hosts(name)
                })
                return_list.append(EmulationPlanDetails(**emulation))
        return return_list

    def _build_atomic_run_list(self, content, run_list):
        raise NotImplementedError(
            "Building atomic test run list is not implemented at this time."
        )
        if self.techniques or self.test_guids:
            self.patterns.add("**/T*/T*.yaml")
        pass

    def build(self):
        if self.adversary or self.config_file and self.config_file.frameworks.adversary_emulations:
            return self._build_emulation_run_list()
        elif self.techniques or self.test_guids:
            if self.config_file and self.config_file.frameworks.atomic_tests:
                return self._build_atomic_run_list()
