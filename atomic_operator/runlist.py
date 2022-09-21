import os
from string import Template
from typing import List

from .base import Base
from .models import ConfigFile, Host
from .frameworks.atomic import Atomic
from .frameworks.emulation import EmulationPhase, EmulationPlanDetails
from .frameworks.loader import Loader


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

    def _build_emulation_run_list(self) -> List[EmulationPlanDetails]:
        content = set()
        if self.adversary:
            self.__logger.info(f"Getting content from adversary '{self.adversary}'.")
            # getting content based on the expected format string for the adversary provided
            content.update(
                self._get_content(
                    pattern=self.EMULATION_PATTERN.substitute(
                        adversary=self.adversary
                    )
                )
            )
        if self.config_file and self.config_file.frameworks.adversary_emulations.tests:
            for test in self.config_file.frameworks.adversary_emulations.tests:
                self.__logger.info(f"Getting content from adversary '{test.name}'.")
                self.__logger.info(
                    self.EMULATION_PATTERN.substitute(
                        adversary=test.name
                    )
                )
                # getting content based on what is defined with the provided config file
                content.update(
                    self._get_content(
                        pattern=self.EMULATION_PATTERN.substitute(
                            adversary=test.name.lower()
                        )
                    )
                )
        return_list = []
        # now that we have our list of content paths lets find them, load, and parse them
        for item in content:
            name = self._get_file_name(item)
            loaded_content = self.load_yaml(str(item))
            if loaded_content:
                phase_list = []
                for i in loaded_content:
                    if not i.get('emulation_plan_details') and i.get('id'):
                        phase_list.append(EmulationPhase(**i))
                # we are getting all th emulation plan details
                emulation = [x for x in loaded_content if x.get('emulation_plan_details')]
                if emulation:
                    # We grab the first item which has additional information about the emulation process
                    emulation = emulation[0]
                    emulation = emulation.pop('emulation_plan_details')
                emulation.update({
                    'path': os.path.dirname(str(item)),
                    'phases': phase_list,
                    'hosts': self._get_emulation_hosts(name)
                })
                # Now we create a EmulationPlanDetails object which contains our EmulationPhases
                return_list.append(EmulationPlanDetails(**emulation))
        return return_list

    def _get_art_hosts(self, name):
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


    def _get_art_inventories_from_config_file(self, technique_name: str = None, test_guid: str = None) -> List[Host]:
        host_list = []
        if self.config_file and self.config_file.frameworks.atomic_tests:
            for test in self.config_file.frameworks.atomic_tests:
                if technique_name and test.technique and technique_name.upper() == test.technique.upper():
                    # the provided technique name string and the defined test technique name are equal
                    if test.inventories and self.config_file.inventory:
                        for inventory in self.config_file.inventory:
                            if inventory.name in test.inventories:
                                host_list.extend(inventory.hosts)
                elif test_guid and test.guid and test_guid == test.guid:
                    # the provided test_guid string and the defined test guid are equal
                    if test.inventories and self.config_file.inventory:
                        for inventory in self.config_file.inventory:
                            if inventory.name in test.inventories:
                                host_list.extend(inventory.hosts)
        return host_list

    def _build_atomic_run_list(self) -> List[Atomic]:
        """Builds the Atomic Red Team run list.

        This method combines any provided technique(s), test_guid(s) and config file into a single
        run list object for easier processing.

        Returns:
            List[Atomic]: Returns a list of Atomic objects.
        """
        return_list = []
        if self.techniques or self.test_guids:
            content = Loader().load()
            if content:
                if "all" in self.techniques:
                    # key is attack_technique ID and 
                    # val is Atomic object
                    for key,val in content.items():
                        if self.host_list:
                            val.hosts = self.host_list
                        return_list.append(val)
                elif self.techniques:
                    for key,val in content.items():
                        if key in self.techniques:
                            if self.host_list:
                                val.hosts = self.host_list
                            if self.config_file:
                                host_list = self._get_art_inventories_from_config_file(technique_name=key)
                                if host_list:
                                    val.hosts = host_list if not val.hosts else val.hosts.extend(host_list)
                            return_list.append(val)
                elif self.test_guids:
                    for key,val in content.items():
                        if val.atomic_tests:
                            test_list = []
                            for test in val.atomic_tests:
                                if test.auto_generated_guid in self.test_guids:
                                    test_list.append(test)
                                    if self.config_file:
                                        val.hosts.extend(self._get_art_inventories_from_config_file(test_guid=test.auto_generated_guid))
                            val.atomic_tests = test_list
                            if self.host_list:
                                val.hosts = self.host_list
                            return_list.append(val)
            else:
                self.__logger.critical("Unable to find or load Atomic Red Team content from the expected location.")
        return return_list

    def build(self):
        if self.adversary:
            #if self.config_file and self.config_file.frameworks.adversary_emulations:
            return self._build_emulation_run_list()
        elif self.techniques or self.test_guids:
            return self._build_atomic_run_list()
