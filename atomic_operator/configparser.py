from logging import config
import os
from .base import Base
from .utils.exceptions import MalformedFile
from .models import Host


class ConfigParser(Base):

    __config_file = None
    __techniques = []
    __test_config = {}
    __hosts = {}

    def __init__(self, config_file=None):
        if config_file:
            self.config_file = self.__load_config(config_file)
            self.__parse_test_guids()
        else:
            self.config_file = None

    def __load_config(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError('Please provide a config_file path that exists')
        from .atomic.loader import Loader
        config = Loader().load_technique(config_file)
        if not config.get('atomic_tests') and not isinstance(config, list):
            raise MalformedFile('Please provide one or more atomic_tests within your config_file')
        return config

    def __parse_hosts(self, inventory):
        host_list = []
        for host in inventory.get('hosts'):
            inputs = inventory['authentication']
            host_list.append(
                self.create_remote_host_object(
                    hostname=host,
                    username=inputs['username'] if inputs.get('username') else None,
                    password=inputs['password'] if inputs.get('password') else None,
                    ssh_key_path=inputs['ssh_key_path'] if inputs.get('ssh_key_path') else None,
                    private_key_string=inputs['private_key_string'] if inputs.get('private_key_string') else None,
                    verify_ssl=inputs['verify_ssl'] if inputs.get('verify_ssl') else False,
                    ssh_port=inputs['port'] if inputs.get('port') else 22,
                    ssh_timeout=inputs['timeout'] if inputs.get('timeout') else 5
                )
            )
        return host_list

    def create_remote_host_object(self, 
        hostname=None,
        username=None,
        password=None,
        ssh_key_path=None,
        private_key_string=None,
        verify_ssl=False,
        ssh_port=22,
        ssh_timeout=5):
            return Host(
                hostname=hostname,
                username=username,
                password=password,
                ssh_key_path=ssh_key_path,
                private_key_string=private_key_string,
                verify_ssl=verify_ssl,
                port=ssh_port,
                timeout=ssh_timeout
            )

    def __parse_test_guids(self):
        if self.config_file:
            for item in self.config_file['atomic_tests']:
                if item.get('guid'):
                    if item['guid'] not in self.__test_config:
                        self.__test_config[item['guid']] = []
                    if item.get('inventories') and self.config_file.get('inventory'):
                        # process inventories to run commands remotely
                        for inventory in item['inventories']:
                            if self.config_file['inventory'].get(inventory):
                                self.__test_config[item['guid']] = self.__parse_hosts(self.config_file['inventory'][inventory])

    def set_tests(self, guids=None, techniques=None, hosts=None, username=None, password=None,
                            ssh_key_path=None,private_key_string=None, verify_ssl=False, 
                            ssh_port=22, ssh_timeout=5
        ):
            if not isinstance(hosts, list):
                hosts = [hosts]
            if guids:
                if not isinstance(guids, list):
                    guids = [guids]
                for guid in guids:
                    if guid not in self.__test_config:
                        self.__test_config[guid] = []
                    for host in hosts:
                        self.__test_config[guid].append(
                            self.create_remote_host_object(
                                hostname=host,
                                username=username,
                                password=password,
                                ssh_key_path=ssh_key_path,
                                private_key_string=private_key_string,
                                verify_ssl=verify_ssl,
                                ssh_port=ssh_port,
                                ssh_timeout=ssh_timeout
                            )
                        )
            if techniques:
                if 'all' in techniques and not guids:
                    if 'all' not in self.__test_config:
                        self.__test_config['all'] = []
                    for host in hosts:
                        self.__test_config['all'].append(
                            self.create_remote_host_object(
                                hostname=host,
                                username=username,
                                password=password,
                                ssh_key_path=ssh_key_path,
                                private_key_string=private_key_string,
                                verify_ssl=verify_ssl,
                                ssh_port=ssh_port,
                                ssh_timeout=ssh_timeout
                            )
                        )
                elif 'all' not in techniques:
                    for technique in techniques:
                        if technique not in self.__test_config:
                            self.__test_config[technique] = []
                        for host in hosts:
                            self.__test_config[technique].append(
                                self.create_remote_host_object(
                                    hostname=host,
                                    username=username,
                                    password=password,
                                    ssh_key_path=ssh_key_path,
                                    private_key_string=private_key_string,
                                    verify_ssl=verify_ssl,
                                    ssh_port=ssh_port,
                                    ssh_timeout=ssh_timeout
                                )
                            )

    @property
    def config(self):
        if self.__test_config:
            return self.__test_config
        else:
            return None

    def is_defined(self, guid: str):
        if self.config and guid in self.config:
            return True
        return False

    def get_inputs(self, guid: str): 
        """Retrieves any defined inputs for a given atomic test GUID

        Args:
            guid (str): An Atomic test GUID

        Returns:
            dict: A dictionary of defined input arguments or empty
        """
        if self.config_file:
            for item in self.config_file['atomic_tests']:
                if item['guid'] == guid:
                    return item.get('input_arguments', {})
        return {}

    def get_inventory(self, guid: str):
        """Retrieves a list of Runner objects based on a Atomic Test GUID

        Args:
            guid (str): An Atomic test GUID

        Returns:
            list: Returns a list of Runner objects if GUID is found else None
        """
        return_list = []
        if self.config_file:
            for item in self.config_file['atomic_tests']:
                if item['guid'] == guid and item.get('inventories') and self.config_file.get('inventory'):
                    # process inventories to run commands remotely
                    for inventory in item['inventories']:
                        if self.config_file['inventory'].get(inventory):
                            return_list.append(
                                self.__parse_hosts(self.config_file['inventory'][inventory])
                            )
        return return_list
