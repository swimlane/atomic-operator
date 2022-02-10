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
from requests.exceptions import RequestException


class RemoteRunner(Runner):

    def __init__(self, atomic_test, test_path):
        """A single AtomicTest object is provided and ran on the local system

        Args:
            atomic_test (AtomicTest): A single AtomicTest object.
            test_path (Atomic): A path where the AtomicTest object resides
        """
        self.test = atomic_test
        self.test_path = test_path

    def execute_process(self, command, executor=None, host=None, cwd=None, elevation_required=False):
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
                    self.state = self.state.invoke(host, executor, command, input_arguments=self.test.input_arguments, elevation_required=elevation_required)
                if str(self.state) == 'ParseResultsState':
                    self.__logger.debug('Running ParseResultsState on_event')
                    final_state = self.state.on_event()
                    self.__logger.info(final_state)
                    finished = True
        except NoValidConnectionsError as ec:
            error_string = f'SSH Error - Unable to connect to {host.hostname} - Received {type(ec).__name__}'
            self.__logger.debug(f'Full stack trace: {ec}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except AuthenticationException as ea:
            error_string = f'SSH Error - Unable to authenticate to host - {host.hostname} - Received {type(ea).__name__}'
            self.__logger.debug(f'Full stack trace: {ea}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except BadAuthenticationType as eb:
            error_string = f'SSH Error - Unable to use provided authentication type to host - {host.hostname} - Received {type(eb).__name__}'
            self.__logger.debug(f'Full stack trace: {eb}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except PasswordRequiredException as ep:
            error_string = f'SSH Error - Must provide a password to authenticate to host - {host.hostname} - Received {type(ep).__name__}'
            self.__logger.debug(f'Full stack trace: {ep}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except AuthenticationError as ewa:
            error_string = f'Windows Error - Unable to authenticate to host - {host.hostname} - Received {type(ewa).__name__}'
            self.__logger.debug(f'Full stack trace: {ewa}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except WinRMTransportError as ewt:
            error_string = f'Windows Error - Error occurred during transport on host - {host.hostname} - Received {type(ewt).__name__}'
            self.__logger.debug(f'Full stack trace: {ewt}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except WSManFaultError as ewf:
            error_string = f'Windows Error - Received WSManFault information from host - {host.hostname} - Received {type(ewf).__name__}'
            self.__logger.debug(f'Full stack trace: {ewf}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except RequestException as re:
            error_string = f'Request Exception - Connection Error to the configured host - {host.hostname} - Received {type(re).__name__}'
            self.__logger.debug(f'Full stack trace: {re}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        except Exception as ex:
            error_string = f'Uknown Error - Received an unknown error from host - {host.hostname} - Received {type(ex).__name__}'
            self.__logger.debug(f'Full stack trace: {ex}')
            self.__logger.warning(error_string)
            return {'error': error_string}
        return final_state

    def start(self, host=None, executor=None):
        """The main method which runs a single AtomicTest object remotely on one remote host.
        """
        return self.execute(host_name=host.hostname, executor=executor, host=host)
