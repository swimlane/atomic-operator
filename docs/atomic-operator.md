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
    The main method in which we run Atomic Red Team tests.

FLAGS
    --technique=TECHNIQUE
        One or more defined techniques by attack_technique ID. Defaults to 'All'.
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
    --show_details=SHOW_DETAILS
        Whether or not you want to output details about tests being ran. Defaults to False.
    --prompt_for_input_args=PROMPT_FOR_INPUT_ARGS
        Whether you want to prompt for input arguments for each test. Defaults to False.
    Additional flags are accepted.
        If provided, keys matching inputs for a test will be replaced. Default is None.
```

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
    atomics_path=os.getcwd(), 
    check_dependencies=False, 
    get_prereqs=False, 
    cleanup=False, 
    command_timeout=20, 
    show_details=False,
    prompt_for_input_args=False,
    **kwargs
)
```
