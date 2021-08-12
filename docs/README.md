# atomic-operator

This python package is used to execute Atomic Red Team tests (Atomics) across multiple operating system environments.

## Features

* Support local execution of Atomic Red Teams tests on Windows, macOS, and Linux systems
* Can prompt for input arguments but not required

## Installation

You can install **atomic-operator** on OS X, Linux, or Windows. You can also install it directly from the source. To install, see the commands under the relevant operating system heading, below.

### Prerequisites

The following libraries are required and installed by atomic-operator:

```
pyyaml==5.4.1
fire==0.3.1
```

### macOS, Linux and Windows:

```bash
pip install atomic-operator
```

### Installing from source

```bash
git clone https://github.com/swimlane/atomic-operator.git
cd atomic-operator
python setup.py install
```


## Usage example (command line)

You can run `atomic-operator` from the command line or within your own Python scripts. To use `atomic-operator` at the command line simply enter the following in your terminal:

```bash
atomic-operator --help
```

In order to run a test you must provide some additional properties (and options if desired). The main method to run tests is named `run`.

```bash
# This will run ALL tests compatiable with your local operating system
atomic-operator run --atomics-path "~/atomic-red-team-master"
```

### Additionall paramters

You can see additional parameters by running the following command:

```bash
atomic-operator run -- --help
```

You should see a similar output to the following:

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


## Usage example (scripts)

To use **atomic-operator** you must instantiate an **AtomicOperator** object.

```python
from atomic_operator import AtomicOperator

operator = AtomicOperator()

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

## Running the tests

Explain how to run the automated tests for this system

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/swimlane/atomic-operator/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
