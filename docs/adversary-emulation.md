# Atomic Operator - Adversary Emulation Library

`atomic-operator` can be used on the command line or via your own scripts. This page shows how the options available within `atomic-operator`.

|Parameter Name|Type|Default|Description|
|--------------|----|-------|-----------|
|name|str|None|One or more adversary names|
|content_path|str|os.getcwd()|The path of Adversary Emulation Plan repository|
|check_prereqs|bool|False|Whether or not to check for prereq dependencies (prereq_comand).|
|get_prereqs|bool|False|Whether or not you want to retrieve prerequisites.|
|cleanup|bool|False|Whether or not you want to run cleanup command(s).|
|copy_source_files|bool|True|Whether or not you want to copy any related source (src, bin, etc.) files to a remote host.|
|command_timeout|int|20|Time duration for each command before timeout.|
|debug|bool|False|Whether or not you want to output details about tests being ran.|
|prompt_for_input_args|bool|False|Whether you want to prompt for input arguments for each test.|
|return_content|bool|False|Whether or not you want to return adversary emulation plan objects instead of running them.|
|config_file|str|None|A path to a conifg_file which is used to automate atomic-operator in environments.|
|config_file_only|bool|False|Whether or not you want to run tests based on the provided config_file only.|
|hosts|list|None|A list of one or more remote hosts to run a test on.|
|username|str|None|Username for authentication of remote connections.|
|password|str|None|Password for authentication of remote connections.|
|ssh_key_path|str|None|Path to a SSH Key for authentication of remote connections.|
|private_key_string|str|None|A private SSH Key string used for authentication of remote connections.|
|verify_ssl|bool|False|Whether or not to verify ssl when connecting over RDP (windows).|
|ssh_port|int|22|SSH port for authentication of remote connections.|
|ssh_timeout|int|5|SSH timeout for authentication of remote connections.|
|**kwargs|dict|None|If additional flags are passed into the run command then we will attempt to match them with defined inputs within Atomic tests and replace their value with the provided value.|

## Command Line

You can access the general help for `atomic-operator` by simplying typing the following in your shell.

```
atomic-operator
```

### Retrieving Adversary Emulation Plans

In order to use `atomic-operator` you must have one or more [Adversary Emulation Plans](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) on your local system. `atomic-operator` provides you with the ability to download the Adversary Emulation Library repository. You can do so by running the following at the command line:

```bash
atomic-operator adversary_emulation get_content
# You can specify the destination directory by using the --destination flag
atomic-operator adversary_emulation get_content --destination "/tmp/some_directory"
```

### Running Plans

In order to run a plan and it's phases you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator adversary_emulation run --content_path "/tmp/some_directory/adversary-emulation-library-3700624"
```

The `run` command has several mandatory and optional parameters that can be used.  You can see these by running the help for this command:

```bash
atomic-operator adversary_emulation run --help
```

It will return the following:

```text
NAME
    atomic-operator adversary_emulation run - The main method in which we run Adversary Emulation Plans.

SYNOPSIS
    atomic-operator adversary_emulation run ADVERSARY <flags> [ARGS]...

DESCRIPTION
    The main method in which we run Adversary Emulation Plans.

POSITIONAL ARGUMENTS
    ADVERSARY
        Type: str
        One or more defined adversary emulation plans by their names
    ARGS
FLAGS
    --content_path=CONTENT_PATH
        Default: '/Us...
        The path of Adversary Emulation Library tests. Defaults to os.getcwd().
    --check_prereqs=CHECK_PREREQS
        Default: False
        Whether or not to check for prereq dependencies (prereq_comand). Defaults to False.
    --get_prereqs=GET_PREREQS
        Default: False
        Whether or not you want to retrieve prerequisites. Defaults to False.
    --cleanup=CLEANUP
        Default: False
        Whether or not you want to run cleanup command(s). Defaults to False.
    --copy_source_files=COPY_SOURCE_FILES
        Default: True
        Whether or not you want to copy any related source (src, bin, etc.) files to a remote host. Defaults to True.
    --command_timeout=COMMAND_TIMEOUT
        Default: 20
        Timeout duration for each command. Defaults to 20.
    --debug=DEBUG
        Default: False
        Whether or not you want to output details about tests being ran. Defaults to False.
    --prompt_for_input_args=PROMPT_FOR_INPUT_ARGS
        Default: False
        Whether you want to prompt for input arguments for each test. Defaults to False.
    --return_content=RETURN_CONTENT
        Default: False
    --config_file=CONFIG_FILE
        Type: Optional[]
        Default: None
        A path to a conifg_file which is used to automate atomic-operator in environments. Default to None.
    --config_file_only=CONFIG_FILE_ONLY
        Default: False
        Whether or not you want to run tests based on the provided config_file only. Defaults to False.
    --hosts=HOSTS
        Default: []
        A list of one or more remote hosts to run a test on. Defaults to [].
    --username=USERNAME
        Type: Optional[]
        Default: None
        Username for authentication of remote connections. Defaults to None.
    --password=PASSWORD
        Type: Optional[]
        Default: None
        Password for authentication of remote connections. Defaults to None.
    --ssh_key_path=SSH_KEY_PATH
        Type: Optional[]
        Default: None
        Path to a SSH Key for authentication of remote connections. Defaults to None.
    --private_key_string=PRIVATE_KEY_STRING
        Type: Optional[]
        Default: None
        A private SSH Key string used for authentication of remote connections. Defaults to None.
    --verify_ssl=VERIFY_SSL
        Default: False
        Whether or not to verify ssl when connecting over RDP (windows). Defaults to False.
    --ssh_port=SSH_PORT
        Default: 22
        SSH port for authentication of remote connections. Defaults to 22.
    --ssh_timeout=SSH_TIMEOUT
        Default: 5
        SSH timeout for authentication of remote connections. Defaults to 5.
    Additional flags are accepted.
        If provided, keys matching inputs for a test will be replaced. Default is None.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

### Running Plans Locally

In order to run a test you must provide some additional properties (and options if desired). The main method to run plans is named `run`.

```bash
atomic-operator adversary_emulation run --content_path "/tmp/some_directory/adversary-emulation-plan-3700624"
```

### Running Plans Remotely

In order to run a plan remotely you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator adversary_emulation run --content_path "/tmp/some_directory/adversary-emulation-plan-3700624" --hosts "10.32.1.0" --username "my_username" --password "my_password"
```

> When running commands remotely against Windows hosts you may need to configure PSRemoting. See details here: [Windows Remoting](windows-remote.md)

### Running atomic-operator using a config_file

In addition to the ability to pass in parameters with `atomic-operator` you can also pass in a path to a `config_file` that contains all the atomic tests and their potential inputs. You can find more information about the [Configuration File here](atomic-operator-config.md)

## Package

In additional to using `atomic-operator` on the command line you can import it into your own scripts/code and build further automation as needed.

```python
from atomic_operator import AtomicOperator

operator = AtomicOperator()

# This will download a local copy of the adversary-emulation-library repository

print(operator.adversary_emulation.get_content('/tmp/some_directory'))

# this will run plans on your local system
operator.adversary_emulationrun(
    adversary: str='All', 
    content_path=os.getcwd(), 
    check_dependencies=False, 
    get_prereqs=False, 
    cleanup=False, 
    command_timeout=20, 
    debug=False,
    prompt_for_input_args=False,
    config_file="some_path.yaml"
    **kwargs
)
```
