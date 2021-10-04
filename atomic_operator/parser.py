import os
from .base import Base
from .utils.exceptions import MalformedFile

from rudder import Host, Runner


class ConfigParser(Base):

    def __init__(self, config_file: str):
        """Parses a provide path to a configuration data file (yaml).

        Args:
            config_file (str): A path to a valid config_file.

        Raises:
            FileNotFoundError: Raises if provided a config_file path that does not exist
            MalformedFile: Raises if the provided config file does not meet the defined format
        """
        self.config = self.__load_config(config_file)

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
                Host(
                    hostname=host,
                    username=inputs['username'] if inputs.get('username') else None,
                    password=inputs['password'] if inputs.get('password') else None,
                    ssh_key_path=inputs['ssh_key_path'] if inputs.get('ssh_key_path') else None,
                    private_key_string=inputs['private_key_string'] if inputs.get('private_key_string') else None,
                    verify_ssl=inputs['verify_ssl'] if inputs.get('verify_ssl') else False,
                    port=inputs['port'] if inputs.get('port') else 22,
                    timeout=inputs['timeout'] if inputs.get('timeout') else 5
                )
            )
        return host_list

    def is_defined(self, guid: str) -> bool:
        for item in self.config['atomic_tests']:
            if item['guid'] == guid:
                return True
        return False

    def get_inputs(self, guid: str) -> dict: 
        """Retrieves any defined inputs for a given atomic test GUID

        Args:
            guid (str): An Atomic test GUID

        Returns:
            dict: A dictionary of defined input arguments or empty
        """
        for item in self.config['atomic_tests']:
            if item['guid'] == guid:
                return item.get('input_arguments', {})
        return {}

    def get_inventory(self, guid: str) -> list:
        """Retrieves a list of Runner objects based on a Atomic Test GUID

        Args:
            guid (str): An Atomic test GUID

        Returns:
            list: Returns a list of Runner objects if GUID is found else None
        """
        return_list = []
        for item in self.config['atomic_tests']:
            if item['guid'] == guid and item.get('inventories') and self.config.get('inventory'):
                # process inventories to run commands remotely
                for inventory in item['inventories']:
                    if self.config['inventory'].get(inventory):
                        return_list.append(
                            Runner(
                                hosts=self.__parse_hosts(self.config['inventory'][inventory]),
                                executor=self.config['inventory'][inventory]['executor'],
                                command=''
                            )
                        )
        return return_list
