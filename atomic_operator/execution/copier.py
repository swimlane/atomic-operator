import os
from ..base import Base


class Copier(Base):


    def __init__(self, windows_client=None, ssh_client=None, elevation_required=False):
        self.windows_client = windows_client
        self.ssh_client = ssh_client
        self.elevation_required = elevation_required

    def join_path_regardless_of_separators(self, *paths):
        return os.path.sep.join(path.rstrip(r"\/") for path in paths)

    def __set_input_argument_values(self, input_arguments):
        for argument in input_arguments:
            argument.source = self._path_replacement(argument.default, Base.CONFIG.atomics_path)
            if self.ssh_client:
                argument.destination = self._path_replacement(argument.default, '/tmp')
            elif self.windows_client:
                argument.destination = self._path_replacement(argument.default, 'c:\\temp')

    def __copy_file_to_windows(self, source, desintation):
        try:
            command = f"New-Item -Path {os.path.dirname(desintation)} -ItemType Directory"
            if self.elevation_required:
                command = f'Start-Process PowerShell -Verb RunAs; {command}'
            output, streams, had_errors = self.windows_client.execute_ps(command)
            response = self.windows_client.copy(source, desintation)
        except:
            self.__logger.warning(f'Unable to execute copy of supporting file {source}')
            self.__logger.warning(f'Output: {output}/nStreams: {streams}/nHad Errors: {had_errors}')

    def __copy_file_to_nix(self, source, destination):
        file = destination.rsplit('/', 1)
        try:
            command = "sh -c '" + f'file="{destination}"' + ' && mkdir -p "${file%/*}" && cat > "${file}"' + "'"
            if self.elevation_required:
                command = f'sudo {command}'
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh_client.exec_command(command)
            ssh_stdin.write(open(f'{source}', 'r').read())
        except:
            self.__logger.warning(f'Unable to execute copy of supporting file {file[-1]}')
            self.__logger.warning(f'STDIN: {ssh_stdin}/nSTDOUT: {ssh_stdout}/nSTDERR: {ssh_stderr}')

    def copy_file(self, source, destination):
        if self.ssh_client:
            self.__copy_file_to_nix(source=source, destination=destination)
        elif self.windows_client:
            self.__copy_file_to_windows(source=source, destination=destination)

    def copy_directory_of_files(self, source, destination):
        return_list = []
        for dirpath, dirnames, files in os.walk(source):
            if files:
                for file in files:
                    if file.endswith('.yaml') or file.endswith('.md'):
                        continue
                    path_list = [destination]
                    for item in file.split(source)[-1].split('/'):
                        if item:
                            path_list.append(item)
                    destination_path = self.join_path_regardless_of_separators(*path_list)
                    full_path = self.join_path_regardless_of_separators(*[dirpath, file])# f"{dirpath}/{file}"
                    
                    if self.ssh_client:
                        self.__copy_file_to_nix(full_path, destination_path)
                    elif self.windows_client:
                        self.__copy_file_to_windows(full_path, destination_path)
                    return_list.append(full_path)
        return return_list

    def copy(self, input_arguments):
        if input_arguments:
            self.__set_input_argument_values(input_arguments)
            for argument in input_arguments:
                if argument.source and argument.destination:
                    if os.path.exists(argument.source):
                        if os.path.isdir(argument.source):
                            file_list = self.copy_directory_of_files(argument.source, argument.destination)
                            argument.value = argument.destination
                        else:
                            self.copy_file(argument.source, argument.destination)
                            argument.value = self._replace_command_string(
                                argument.default, 
                                path='/tmp',
                                input_arguments=input_arguments
                            )
                    else:
                        argument.value = self._replace_command_string(
                            argument.default, 
                            path='/tmp',
                            input_arguments=input_arguments
                        )
                else:
                    argument.value = self._replace_command_string(
                        argument.default, 
                        path='/tmp',
                        input_arguments=input_arguments
                    )
        return True
