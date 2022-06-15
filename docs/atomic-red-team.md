# Atomic Operator - Atomic Red Team

`atomic-operator` can be used on the command line or via your own scripts. This page shows how the options available within `atomic-operator`.

|Parameter Name|Type|Default|Description|
|--------------|----|-------|-----------|
|techniques|list|all|One or more defined techniques by attack_technique ID.|
|test_guids|list|None|One or more Atomic test GUIDs.|
|select_tests|bool|False|Select one or more atomic tests to run when a techniques are specified.|
|content_path|str|os.getcwd()|The path of Atomic tests.|
|check_prereqs|bool|False|Whether or not to check for prereq dependencies (prereq_comand).|
|get_prereqs|bool|False|Whether or not you want to retrieve prerequisites.|
|cleanup|bool|False|Whether or not you want to run cleanup command(s).|
|copy_source_files|bool|True|Whether or not you want to copy any related source (src, bin, etc.) files to a remote host.|
|command_timeout|int|20|Time duration for each command before timeout.|
|debug|bool|False|Whether or not you want to output details about tests being ran.|
|prompt_for_input_args|bool|False|Whether you want to prompt for input arguments for each test.|
|return_content|bool|False|Whether or not you want to return atomics instead of running them.|
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

### Retrieving Atomic Tests

In order to use `atomic-operator` you must have one or more [atomic-red-team](https://github.com/redcanaryco/atomic-red-team) tests (Atomics) on your local system. `atomic-operator` provides you with the ability to download the Atomic Red Team repository. You can do so by running the following at the command line:

```bash
atomic-operator atomic_red_team get_content
# You can specify the destination directory by using the --destination flag
atomic-operator atomic_red_team get_content --destination "/tmp/some_directory"
```

### Running Tests

In order to run a test you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator atomic_red_team run --atomics-path "/tmp/some_directory/redcanaryco-atomic-red-team-3700624"
```

The `run` command has several mandatory and optional parameters that can be used.  You can see these by running the help for this command:

```bash
atomic-operator atomic_red_team run --help
```

It will return the following:

```text
NAME
    atomic-operator atomic_red_team run - The main method in which we run Atomic Red Team tests.

SYNOPSIS
    atomic-operator atomic_red_team run <flags>

DESCRIPTION
    config_file definition:
        atomic-operator's run method can be supplied with a path to a configuration file (config_file) which defines 
        specific tests and/or values for input parameters to facilitate automation of said tests.
        An example of this config_file can be seen below:

            inventory:
              windows1:
                executor: powershell # or cmd
                input:
                  username: username
                  password: some_passowrd!
                  verify_ssl: false
                hosts:
                  - 192.168.1.1
                  - 10.32.1.1
                  # etc
              linux1:
                executor: ssh
                authentication:
                  username: username
                  password: some_passowrd!
                  #ssk_key_path:
                  port: 22
                  timeout: 5
                hosts:
                  - 192.168.1.1
                  - 10.32.100.1
                  # etc.
            atomic_tests:
              - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
                input_arguments:
                  output_file:
                    value: custom_output.txt
                  input_file:
                    value: custom_input.txt
                inventories:
                  - windows1
              - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
                input_arguments:
                  second_arg:
                    value: SWAPPPED argument
                inventories:
                  - windows1
                  - linux1
              - guid: 32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2
                inventories:
                  - linux1

FLAGS
    --techniques=TECHNIQUES
        One or more defined techniques by attack_technique ID. Defaults to 'All'.
    --test_guids=TEST_GUIDS
        One or more Atomic test GUIDs. Defaults to None.
    --content_path=ATOMICS_PATH
        The path of Atomic tests. Defaults to os.getcwd().
    --check_dependencies=CHECK_DEPENDENCIES
        Whether or not to check for dependencies. Defaults to False.
    --get_prereqs=GET_PREREQS
        Whether or not you want to retrieve prerequisites. Defaults to False.
    --cleanup=CLEANUP
        Whether or not you want to run cleanup command(s). Defaults to False.
    --command_timeout=COMMAND_TIMEOUT
        Timeout duration for each command. Defaults to 20.
    --debug=DEBUG
        Whether or not you want to output details about tests being ran. Defaults to False.
    --prompt_for_input_args=PROMPT_FOR_INPUT_ARGS
        Whether you want to prompt for input arguments for each test. Defaults to False.
    --config_file=CONFIG_FILE
        A path to a conifg_file which is used to automate atomic-operator in environments. Default to None.
    Additional flags are accepted.
        If provided, keys matching inputs for a test will be replaced. Default is None.
```

### Running Tests Locally

In order to run a test you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator run --atomics-path "/tmp/some_directory/redcanaryco-atomic-red-team-3700624"
```

You can select individual tests when you provide one or more specific techniques. For example running the following on the command line:

```bash
atomic-operator run --techniques T1564.001 --select_tests
```

Will prompt the user with a selection list of tests associated with that technique. A user can select one or more tests by using the space bar to highlight the desired test:

```text
 Select Test(s) for Technique T1564.001 (Hide Artifacts: Hidden Files and Directories)

 * Create a hidden file in a hidden directory (61a782e5-9a19-40b5-8ba4-69a4b9f3d7be)
   Mac Hidden file (cddb9098-3b47-4e01-9d3b-6f5f323288a9)
   Create Windows System File with Attrib (f70974c8-c094-4574-b542-2c545af95a32)
   Create Windows Hidden File with Attrib (dadb792e-4358-4d8d-9207-b771faa0daa5)
   Hidden files (3b7015f2-3144-4205-b799-b05580621379)
   Hide a Directory (b115ecaf-3b24-4ed2-aefe-2fcb9db913d3)
   Show all hidden files (9a1ec7da-b892-449f-ad68-67066d04380c)
```

### Running Tests Remotely

In order to run a test remotely you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator run --atomics-path "/tmp/some_directory/redcanaryco-atomic-red-team-3700624" --hosts "10.32.1.0" --username "my_username" --password "my_password"
```

> When running commands remotely against Windows hosts you may need to configure PSRemoting. See details here: [Windows Remoting](windows-remote.md)

### Running atomic-operator using a config_file

In addition to the ability to pass in parameters with `atomic-operator` you can also pass in a path to a `config_file` that contains all the atomic tests and their potential inputs. You can find more information about the [Configuration File here](atomic-operator-config.md)

## Package

In additional to using `atomic-operator` on the command line you can import it into your own scripts/code and build further automation as needed.

```python
from atomic_operator import AtomicOperator

operator = AtomicOperator()

# This will download a local copy of the atomic-red-team repository

print(operator.atomic_red_team.get_content('/tmp/some_directory'))

# this will run tests on your local system
operator.atomic_red_team.run(
    technique: str='All', 
    test_guids: list=[],
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
