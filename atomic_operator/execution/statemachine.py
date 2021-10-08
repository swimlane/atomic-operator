
from pypsrp.client import Client

from .runner import Runner
from ..base import Base



class State:
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__


class CreationState(State):
    """
    The state which is used to modify commands
    """

    def powershell(self, event):
        command = None
        if event:
            if '\n' in event or '\r' in event:
                if '\n' in event:
                    command = event.replace('\n', '; ')
                if '\r' in event:
                    if command:
                        command = command.replace('\r', '; ')
                    else:
                        command = event.replace('\r', '; ')
            return InnvocationState()

    def cmd(self):
        return InnvocationState()

    def ssh(self):
        return InnvocationState()

    def on_event(self, command_type, command):
        if command_type == 'powershell':
            return self.powershell(command)
        elif command_type == 'cmd':
            return self.cmd()
        elif command_type == 'ssh':
            return self.ssh()
        elif command_type == 'sh':
            return self.ssh()
        return self


class InnvocationState(State, Base):
    """
    The state which indicates the invocation of a command
    """

    __win_client = None

    def __handle_windows_errors(self, stream):
        return_list = []
        for item in stream.error:
            return_list.append({
                'type': 'error',
                'value': str(item)
            })
        for item in stream.debug:
            return_list.append({
                'type': 'debug',
                'value': str(item)
            })
        for item in stream.information:
            return_list.append({
                'type': 'information',
                'value': str(item)
            })
        for item in stream.verbose:
            return_list.append({
                'type': 'verbose',
                'value': str(item)
            })
        for item in stream.warning:
            return_list.append({
                'type': 'warning',
                'value': str(item)
            })
        return return_list

    def __create_win_client(self, hostinfo):
        self.__win_client = Client(
            hostinfo.hostname,
            username=hostinfo.username,
            password=hostinfo.password,
            ssl=hostinfo.verify_ssl
        )

    def __invoke_cmd(self, command):
        if not self.__win_client:
            self.__create_win_client(self.hostinfo)
        stdout, stderr, rc = self.__win_client.execute_cmd(command)
        # NOTE: rc (return code of process) should equal 0 but we are not adding logic here this is handled int he ParseResultsState class
        if stderr:
            self.__logger.error('{host} responded with the following message(s): {message}'.format(
                host=self.hostinfo.hostname,
                message=stderr
            ))
        return ParseResultsState(
            command=command,
            return_code=rc,
            output=stdout,
            error=stderr
        )

    def __invoke_powershell(self, command):
        if not self.__win_client:
            self.__create_win_client(self.hostinfo)
        output, streams, had_errors = self.__win_client.execute_ps(command)
        if not output:
            output = self.__handle_windows_errors(streams)
        if had_errors:
            self.__logger.error('{host} responded with the following message(s): {message}'.format(
                host=self.hostinfo.hostname,
                message=self.__handle_windows_errors(streams)
            ))
        return ParseResultsState(
            command=command, 
            return_code=had_errors, 
            output=output, 
            error=self.__handle_windows_errors(streams)
        )

    def __invoke_ssh(self,command):
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.hostinfo.ssh_key_path:
            ssh.connect(
                self.hostinfo.hostname,
                port=self.hostinfo.port,
                username=self.hostinfo.username,
                key_filename=self.hostinfo.ssh_key_path
            )
        elif self.hostinfo.private_key_string:
            ssh.connect(
                self.hostinfo.hostname,
                port=self.hostinfo.port,
                username=self.hostinfo.username,
                pkey=self.hostinfo.private_key_string
            )
        elif self.hostinfo.password:
            ssh.connect(
                self.hostinfo.hostname,
                port=self.hostinfo.port,
                username=self.hostinfo.username,
                password=self.hostinfo.password,
                timeout=self.hostinfo.timeout
            )
        else:
            raise AttributeError('Please provide either a ssh_key_path or a password')
        out = None
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        return_code = ssh_stdout.channel.recv_exit_status()
        out = ssh_stdout.read()
        err = ssh_stderr.read()
        ssh_stdin.flush()
        ssh.close()
        return ParseResultsState(
            command=command, 
            return_code=return_code,
            output=out, 
            error=err
        )

    def invoke(self, hostinfo, command_type, command):
        self.hostinfo = hostinfo
        if command_type == 'powershell':
            result = self.__invoke_powershell(command)
        elif command_type == 'cmd':
            result = self.__invoke_cmd(command)
        elif command_type == 'ssh':
            result = self.__invoke_ssh(command)
        return result


class ParseResultsState(State, Runner):
    """
    The state which is used to parse the results
    """

    def __init__(self, command=None, return_code=None, output=None, error=None):
        self.result = {}
        self.print_process_output(
                command=command, 
                return_code=return_code, 
                output=output,
                errors=error
            )
        if output:
            self.result.update({'output': self.__parse(output)})
        if error:
            self.result.update({'error': self.__parse(error)})

    def __parse(self, results):
        if isinstance(results, bytes):
            results = results.decode("utf-8").strip()
        return results

    def on_event(self):
        return self.result
