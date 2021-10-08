from .runner import Runner


class RemoteRunner(Runner):

    def __init__(self, atomic_test, test_path, runner):
        """A single AtomicTest object is provided and ran on the local system

        Args:
            atomic_test (AtomicTest): A single AtomicTest object.
            test_path (Atomic): A path where the AtomicTest object resides
            runner (Runner): A Runner object defined with a config file
        """
        self.test = atomic_test
        self.test_path = test_path
        self.runner = runner

    def execute_process(self, command, executor=None, host=None, cwd=None):
        """Main method to execute commands using Rudder

        Args:
            command (str): The command to run remotely on the desired systems
            executor (str): An executor that can be passed to rudder. Defaults to None.
            host (str): A host to run remote commands on. Defaults to None.
        """
        if not isinstance(host, list):
            host = [host]
        response = Rudder().execute(
            host=host,
            executor=executor,
            command=command
        )
        self.__logger.debug(response)
        if isinstance(response, dict):
            for key,val in response.items():
                return val

    def run(self):
        """The main method which runs a single AtomicTest object remotely on one or more defined hosts.
        """
        return_dict = {}
        for runner in self.runner:
            for host in runner.hosts:
                return_dict.update(
                    self.execute(
                        host_name=host.hostname, 
                        executor=runner.executor, 
                        host=host
                    )
                )
        return return_dict
