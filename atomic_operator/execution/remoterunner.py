from .runner import Runner
from .statemachine import CreationState
from paramiko.ssh_exception import (
    BadAuthenticationType,
    NoValidConnectionsError, 
    AuthenticationException, 
    PasswordRequiredException
)
from pypsrp.exceptions import (
    AuthenticationError,
    WinRMTransportError,
    WSManFaultError
)


class RemoteRunner(Runner):

    def __init__(self, atomic_test, test_path, supporting_files=None):
        """A single AtomicTest object is provided and ran on the local system

        Args:
            atomic_test (AtomicTest): A single AtomicTest object.
            test_path (Atomic): A path where the AtomicTest object resides
        """
        self.test = atomic_test
        self.test_path = test_path
        self.supporting_files = supporting_files

    def execute_process(self, command, executor=None, host=None, cwd=None):
        """Main method to execute commands using state machine

        Args:
            command (str): The command to run remotely on the desired systems
            executor (str): An executor that can be passed to state machine. Defaults to None.
            host (str): A host to run remote commands on. Defaults to None.
        """
        self.state = CreationState()
        final_state = None
        try:
            finished = False
            while not finished:
                if str(self.state) == 'CreationState':
                    self.__logger.debug('Running CreationState on_event')
                    self.state = self.state.on_event(executor, command)
                if str(self.state) == 'InnvocationState':
                    self.__logger.debug('Running InnvocationState on_event')
                    self.state = self.state.invoke(host, executor, command, input_arguments=self.test.input_arguments, supporting_files=self.supporting_files, test_path=self.test_path)
                if str(self.state) == 'ParseResultsState':
                    self.__logger.debug('Running ParseResultsState on_event')
                    final_state = self.state.on_event()
                    self.__logger.info(final_state)
                    finished = True
        except NoValidConnectionsError as ec:
            self.__logger.warning(f'SSH Error: Unable to connect to {host.hostname}: {ec}')
            final_state = ec
        except AuthenticationException as ea:
            self.__logger.warning(f'SSH Error: Unable to authenticate to host {host.hostname}: {ea}')
            final_state = ea
        except BadAuthenticationType as eb:
            self.__logger.warning(f'SSH Error: Unable to use provided authentication type to {host.hostname}: {eb}')
            final_state = eb
        except PasswordRequiredException as ep:
            self.__logger.warning(f'SSH Error: Must provide a password to authenticate to {host.hostname}: {ep}')
            final_state = ep
        except AuthenticationError as ewa:
            self.__logger.warning(f'Windows Error: Unable to authenticate to host {host.hostname}: {ewa}')
            final_state = ewa
        except WinRMTransportError as ewt:
            self.__logger.warning(f'Windows Error: Error occurred during transport on host {host.hostname}: {ewt}')
            final_state = ewt
        except WSManFaultError as ewf:
            self.__logger.warning(f'Windows Error: Received WSManFault information from host {host.hostname}: {ewf}')
            final_state = ewf
        except Exception as ex:
            self.__logger.warning(f"Uknown Error: Received an unknown error from host {host.hostname}: {ex}")
            final_state = ex
        return final_state

    def run(self, host=None, executor=None):
        """The main method which runs a single AtomicTest object remotely on one remote host.
        """
        return self.execute(host_name=host.hostname, executor=executor, host=host)
