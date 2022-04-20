# atomic-operator

![](atomic-operator-logo.svg)

This python package is used to execute either of the following frameworks across multiple operating system environments:

* [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
* [Adversary Emulation Plans](https://github.com/center-for-threat-informed-defense/adversary_emulation_library)


> ([What's new?](CHANGELOG.md))

## Why?

`atomic-operator` enables security professionals to test their detection and defensive capabilities against prescribed techniques within the Atomic Red Team project or emulation plans with the Adversary Emulation Library project. By utilizing a testing framework such as `atomic-operator`, you can identify both your defensive capabilities as well as gaps in defensive coverage.

Additionally, `atomic-operator` can be used in many other situations like:

- Generating alerts to test products
- Testing EDR and other security tools
- Identifying way to perform defensive evasion from an adversary perspective
- Plus more.

## Features

* Support local and remote execution on Windows, macOS, and Linux systems of these frameworks:
    * Atomic Red Teams tests
    * Adversary Emulation Library plans
* Supports running atomics against `iaas:aws`
* Can prompt for input arguments but not required
* Assist with downloading the atomic-red-team or the adversary-emulation-library repositories
* Can be automated further based on a configuration file
* A command-line and importable Python package
* Select specific tests when one or more techniques are specified
* Plus more

## Getting Started

`atomic-operator` is a Python-only package hosted on [PyPi](https://pypi.org/project/atomic-operator/) and works with Python 3.6 and greater.

If you are wanting a PowerShell version, please checkout [Invoke-AtomicRedTeam](https://github.com/redcanaryco/invoke-atomicredteam).

```bash
pip install atomic-operator
```

The next steps will guide you through setting up and running `atomic-operator`.

* Atomic Red Team 
    * [Get Content](get_content.md)
    * [atomic-red-team](atomic-red-team.md) Understand the options availble in `atomic-operator atomic_red_team`
    * [Running Test on Command Line](running-tests-command-line.md) or [Running Tests within a Script](running-tests-script.md)
* Adversary Emulation Library
    * [Get Content](get_content.md)
    * [adversary-emulation](adversary-emulation.md) Understand the options availble in `atomic-operator adversary_emulation`
    * [Running Plans on Command Line](running-plans-command-line.md) or [Running Plans within a Script](running-plans-script.md)
* [Running Tests via Configuration File](atomic-operator-config.md)

## Installation

You can install **atomic-operator** on OS X, Linux, or Windows. You can also install it directly from the source. To install, see the commands under the relevant operating system heading, below.

### Prerequisites

The following libraries are required and installed by atomic-operator:

```
pyyaml==5.4.1
fire==0.4.0
requests==2.26.0
attrs==21.2.0
pypsrp==0.5.0
paramiko>=2.10.1
pick==1.2.0
pydantic>=1.9.0
```

### macOS, Linux and Windows:

```bash
pip install atomic-operator
```

### macOS using M1 processor

```bash
git clone https://github.com/swimlane/atomic-operator.git
cd atomic-operator

# Satisfy ModuleNotFoundError: No module named 'setuptools_rust'
brew install rust
pip3 install --upgrade pip
pip3 install setuptools_rust

# Back to our regularly scheduled programming . . .  
pip install -r requirements.txt
python setup.py install
```

### Installing from source

```bash
git clone https://github.com/swimlane/atomic-operator.git
cd atomic-operator
pip install -r requirements.txt
python setup.py install
```

## Usage example (command line)

You can run `atomic-operator` from the command line or within your own Python scripts. To use `atomic-operator` at the command line simply enter the following in your terminal:

```bash
atomic-operator --help
atomic-operator atomic_red_team run -- --help
atomic-operator art run -- --help
atomic-operator adversary_emulation run -- --help
```

> Please note that to see details about the run command run `atomic-operator run -- --help` and NOT `atomic-operator run --help`

### Retrieving Atomic Tests

In order to use `atomic-operator atomic_red_team` you must have one or more [atomic-red-team](https://github.com/redcanaryco/atomic-red-team) tests (Atomics) on your local system. In order to use `atomic-operator adversary_emulation` you must have one or more [adversary-emulation-library-plans](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) on your local system.

`atomic-operator` provides you with the ability to download either the Atomic Red Team repository or the Adversary Emulation Library repository. You can do so by running the following at the command line:

```bash
atomic-operator atomic_red_team get_content 
atomic-operator adversary_emulation get_content
# You can specify the destination directory by using the --destination flag
atomic-operator atomic_red_team get_content --destination "/tmp/some_directory"
atomic-operator adversary_emulation get_content --destination "/tmp/some_directory"
```

## Getting Help

Please create an [issue](https://github.com/swimlane/atomic-operator/pulls) if you have questions or run into any issues.

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

## Shoutout

- Thanks to [keithmccammon](https://github.com/keithmccammon) for helping identify issues with macOS M1 based proccesssor and providing a fix
