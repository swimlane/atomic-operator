# Atomic Operator

`atomic-operator` can be used on the command line or via your own scripts. This page shows how the options available within `atomic-operator`.

## Command Line

You can access the general help for `atomic-operator` by simplying typing the following in your shell.

```
atomic-operator
```

### Retrieving Atomic Tests

In order to use `atomic-operator` you must have one or more [atomic-red-team](https://github.com/redcanaryco/atomic-red-team) tests (Atomics) on your local system. `atomic-operator` provides you with the ability to download the Atomic Red Team repository. You can do so by running the following at the command line:

```bash
atomic-operator get_atomics 
# You can specify the destination directory by using the --destination flag
atomic-operator get_atomics --destination "/tmp/some_directory"
```

### Running Tests

In order to run a test you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator run --atomics-path "/tmp/some_directory/redcanaryco-atomic-red-team-3700624"
```

The `run` command has several mandatory and optional parameters that can be used.  You can see these by running the help for this command:

```bash
atomic-operator run -- --help
```

It will return the following:

```text
NAME
    atomic-operator run - The main method in which we run Atomic Red Team tests.

SYNOPSIS
    atomic-operator run <flags>

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
    --atomics_path=ATOMICS_PATH
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

### Running atomic-operator using a config_file

In addition to the ability to pass in parameters with `atomic-operator` you can also pass in a path to a `config_file` that contains all the atomic tests and their potential inputs. You can find more information about the [Configuration File here](atomic-operator-config.md)

## Package

In additional to using `atomic-operator` on the command line you can import it into your own scripts/code and build further automation as needed.

```python
from atomic_operator import AtomicOperator

operator = AtomicOperator()

# This will download a local copy of the atomic-red-team repository

print(operator.get_atomics('/tmp/some_directory'))

# this will run tests on your local system
operator.run(
    technique: str='All', 
    test_guids: list=[],
    atomics_path=os.getcwd(), 
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
