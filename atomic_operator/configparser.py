import os
from .base import Base
from .utils.exceptions import MalformedFile
from .models import Host
from .atomic.loader import Loader


class ConfigParser(Base):

    def __init__(self, config_file=None, techniques=None, test_guids=None, 
                       host_list=None, username=None, password=None,
                       ssh_key_path=None, private_key_string=None, verify_ssl=False,
                       ssh_port=22, ssh_timeout=5, select_tests=False
                ):
        """Parses a provided config file as well as parameters to build a run list
        
        This list combines Atomics and potentially filters 
        tests defined within that Atomic object based on passed
        in parameters and config_file.

        Additionally, a list of Host objects are added to their
        defined techniques or test_guids based on config and/or
        passed in parameters.

        Example: Example structure returned from provided values
        [
            Atomic(
                attack_technique='T1016', 
                display_name='System Network Configuration Discovery', 
                path='/Users/josh.rickard/_Swimlane2/atomic-operator/redcanaryco-atomic-red-team-22dd2fb/atomics/T1016', 
                atomic_tests=[
                    AtomicTest(
                        name='System Network Configuration Discovery', 
                        description='Identify network configuration information.\n\nUpon successful execution, ...', 
                        supported_platforms=['macos', 'linux'], 
                        auto_generated_guid='c141bbdb-7fca-4254-9fd6-f47e79447e17', 
                        executor=AtomicExecutor(
                            name='sh', 
                            command='if [ -x "$(command -v arp)" ]; then arp -a; else echo "arp is missing from ....', 
                            cleanup_command=None, 
                            elevation_required=False, steps=None
                        ), 
                        input_arguments=None, 
                        dependency_executor_name=None, 
                        dependencies=[]
                    )
                ], 
                hosts=[
                    Host(
                        hostname='192.168.1.1', 
                        username='username', 
                        password='some_passowrd!', 
                        verify_ssl=False, 
                        ssh_key_path=None, 
                        private_key_string=None, 
                        port=22, 
                        timeout=5
                    )
                ],
                supporting_files=[
                    'redcanaryco-atomic-red-team-22dd2fb/atomics/T1016/src/top-128.txt', 
                    'redcanaryco-atomic-red-team-22dd2fb/atomics/T1016/src/qakbot.bat'
                ]
            )
        ]
        """
        self.__config_file = self.__load_config(config_file)
        self.techniques = techniques
        self.test_guids = test_guids
        self.select_tests = select_tests
        self.__host_list = []
        if host_list:
            for host in self.parse_input_lists(host_list):
                self.__host_list.append(self.__create_remote_host_object(
                    hostname=host,
                    username=username,
                    password=password,
                    ssh_key_path=ssh_key_path,
                    private_key_string=private_key_string,
                    verify_ssl=verify_ssl,
                    ssh_port=ssh_port,
                    ssh_timeout=ssh_timeout
                ))

    def __load_config(self, config_file):
        if config_file and self.get_abs_path(config_file):
            config_file = self.get_abs_path(config_file)
            if not os.path.exists(config_file):
                raise FileNotFoundError('Please provide a config_file path that exists')
            from .atomic.loader import Loader
            config = Loader().load_technique(config_file)
            if not config.get('atomic_tests') and not isinstance(config, list):
                raise MalformedFile('Please provide one or more atomic_tests within your config_file')
            return config
        return {}

    def __parse_hosts(self, inventory):
        host_list = []
        for host in inventory.get('hosts'):
            inputs = inventory['authentication']
            host_list.append(
                self.__create_remote_host_object(
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

    def __create_remote_host_object(self, 
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

    def __parse_test_guids(self, _config_file):
        test_dict = {}
        return_list = []
        if _config_file:
            for item in _config_file['atomic_tests']:
                if item.get('guid'):
                    if item['guid'] not in test_dict:
                        test_dict[item['guid']] = []
                    if item.get('inventories') and _config_file.get('inventory'):
                        # process inventories to run commands remotely
                        for inventory in item['inventories']:
                            if _config_file['inventory'].get(inventory):
                                test_dict[item['guid']] = self.__parse_hosts(_config_file['inventory'][inventory])
        if test_dict:
            for key,val in test_dict.items():
                for item in self.__build_run_list(
                    test_guids=[key],
                    host_list=val
                    ):
                    return_list.append(item)
        return return_list

    def __build_run_list(self, techniques=None, test_guids=None, host_list=None, select_tests=False):
        __run_list = []
        self.__loaded_techniques = Loader().load_techniques()
        if test_guids:
            for key,val in self.__loaded_techniques.items():
                test_list = []
                for test in val.atomic_tests:
                    if test.auto_generated_guid in test_guids:
                        test_list.append(test)
                if test_list:
                    temp = self.__loaded_techniques[key]
                    temp.atomic_tests = test_list
                    temp.hosts = host_list
                    __run_list.append(temp)
        if techniques:
            if 'all' not in techniques:
                for technique in techniques:
                    if self.__loaded_techniques.get(technique):
                        temp = self.__loaded_techniques[technique]
                        if select_tests:
                            temp.atomic_tests = self.select_atomic_tests(
                                self.__loaded_techniques[technique]
                            )
                        temp.hosts = host_list
                        __run_list.append(temp)
            elif 'all' in techniques and not test_guids:
                for key,val in self.__loaded_techniques.items():
                    temp = self.__loaded_techniques[key]
                    if select_tests:
                            temp.atomic_tests = self.select_atomic_tests(
                                self.__loaded_techniques[key]
                            )
                    temp.hosts = host_list
                    __run_list.append(temp)
            else:
                pass
        return __run_list

    @property
    def run_list(self):
        """Returns a list of Atomic objects that will be ran.
        
        This list combines Atomics and potentially filters 
        tests defined within that Atomic object based on passed
        in parameters and config_file.

        Additionally, a list of Host objects are added to their
        defined techniques or test_guids based on config and/or
        passed in parameters.

        [
            Atomic(
                attack_technique='T1016', 
                display_name='System Network Configuration Discovery', 
                path='/Users/josh.rickard/_Swimlane2/atomic-operator/redcanaryco-atomic-red-team-22dd2fb/atomics/T1016', 
                atomic_tests=[
                    AtomicTest(
                        name='System Network Configuration Discovery', 
                        description='Identify network configuration information.\n\nUpon successful execution, ...', 
                        supported_platforms=['macos', 'linux'], 
                        auto_generated_guid='c141bbdb-7fca-4254-9fd6-f47e79447e17', 
                        executor=AtomicExecutor(
                            name='sh', 
                            command='if [ -x "$(command -v arp)" ]; then arp -a; else echo "arp is missing from ....', 
                            cleanup_command=None, 
                            elevation_required=False, steps=None
                        ), 
                        input_arguments=None, 
                        dependency_executor_name=None, 
                        dependencies=[]
                    )
                ], 
                hosts=[
                    Host(
                        hostname='192.168.1.1', 
                        username='username', 
                        password='some_passowrd!', 
                        verify_ssl=False, 
                        ssh_key_path=None, 
                        private_key_string=None, 
                        port=22, 
                        timeout=5
                    )
                ],
                supporting_files=[
                    'redcanaryco-atomic-red-team-22dd2fb/atomics/T1016/src/top-128.txt', 
                    'redcanaryco-atomic-red-team-22dd2fb/atomics/T1016/src/qakbot.bat'
                ]
            )
        ]

        Returns:
            [list]: A list of modified Atomic objects that will be used to run 
                    either remotely or locally.
        """
        __run_list = []
        if self.__config_file:
            __run_list = self.__parse_test_guids(self.__config_file)

        for item in self.__build_run_list(
            techniques=self.parse_input_lists(self.techniques) if self.techniques else [],
            test_guids=self.parse_input_lists(self.test_guids) if self.test_guids else [],
            host_list=self.__host_list,
            select_tests=self.select_tests
            ):
            __run_list.append(item)
        return __run_list

    @property
    def config(self):
        """Returns raw converted config_file passed into class

        Returns:
            [dict]: Returns the converted config_file as dictionary.
        """
        if self.__config_file:
            return self.__config_file
        else:
            return None

    def is_defined(self, guid: str):
        """Checks to see if a GUID is defined within a config file

        Args:
            guid (str): The GUID defined within a parsed config file

        Returns:
            [bool]: Returns True if GUID is defined within parsed config_file
        """
        if self.__config_file:
            for item in self.__config_file['atomic_tests']:
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
        if self.__config_file:
            for item in self.__config_file['atomic_tests']:
                if item['guid'] == guid:
                    return item.get('input_arguments', {})
        return {}
