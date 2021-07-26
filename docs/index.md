# atomic-operator

Current Version: v0.0.1 ([What's new?](release-notes.md)).

`atomic-operator` is a Python package is used to execute Atomic Red Team tests (Atomics) across multiple operating system environments.

The main goal of `atomic-operator` is to assist with testing your security defenses using defined `Atomics`.

## Getting Started

`atomic-operator` is a Python-only package hosted on [PyPi]() and works with Python 3.6 and greater.

If you are wanting a PowerShell version, please checkout [Invoke-AtomicRedTeam](https://github.com/redcanaryco/invoke-atomicredteam).


```bash
pip install atomic-operator
```

The next steps will guide you through setting up and running `atomic-operator`.

* [Get Atomics](atomics.md) Install / clone Atomic Red Team repository
* [atomic-operator](atomic-operator.md) Understand the options availble in atomic-operator
* [Running Test on Command Line](running-tests-command-line.md) or [Running Tests within a Script](running-tests-script.md)

## Why?

`atomic-operator` was built to assist organizations and security professionals with testing their defenses against MITRE ATT&CK Techniques defined by Atomic Red Team. These techniques are common TTPs used by malicious actors and thus `atomic-operator` helps organizations assess their defensive capabilities against these TTPs.


## Getting Help

Please create an [issue](https://github.com/swimlane/atomic-operator/pulls) if you have questions or run into any issues.
