import os
from .base import Base
from .utils.exceptions import MalformedFile

from rudder import Host, Runner


class ConfigParser(Base):

    __config_file = None

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

    @property
    def config_file(self):
        return self.__config_file

    @config_file.setter
    def config_file(self, value):
        if value:
            self.__config_file = self.__load_config(value)

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

    def is_defined(self, guid: str):
        if self.config_file:
            for item in self.config_file['atomic_tests']:
                if item['guid'] == guid:
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
                                Runner(
                                    hosts=self.__parse_hosts(self.config_file['inventory'][inventory]),
                                    executor=self.config_file['inventory'][inventory]['executor'],
                                    command=''
                                )
                            )
        return return_list
