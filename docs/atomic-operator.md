# Atomic Operator

`atomic-operator` can be used on the command line or via your own scripts. This page shows how the options available within `atomic-operator`.

## Command Line

You can access the general help for `atomic-operator` by simplying typing the following in your shell.

```
atomic-operator
```

There is currently only one command you can use. That is the `run` command. The `run` command has several mandatory and optional parameters that can be used.  You can see these by running the help for this command:

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

atomic_operator = AtomicOperator()

print(atomic_operator.run())
```