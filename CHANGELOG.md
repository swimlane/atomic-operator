# CHANGELOG

## [0.9.0](https://github.com/swimlane/atomic-operator/compare/0.8.5...0.9.0) (2023-03-06)


### ⚠ BREAKING CHANGES

* Adding support for atomic-operator-runner to separate responsibilities from this package to the executioner in the runner package.
* Adding poetry support for the entire project going forward. This may be a BREAKING CHANGE!

### Features

* Added new parameter to accept input_arguments from command line and config file ([831d9cb](https://github.com/swimlane/atomic-operator/commit/831d9cb179c335261c8c900a95f6a45a14595e40))
* Adding poetry support for the entire project going forward. This may be a BREAKING CHANGE! ([cbfce67](https://github.com/swimlane/atomic-operator/commit/cbfce678f488c52844ebf4d5798267186c008ae8))
* Adding support for atomic-operator-runner to separate responsibilities from this package to the executioner in the runner package. ([c9484e4](https://github.com/swimlane/atomic-operator/commit/c9484e492f2254b065f7a6d6912340451a2d90e7))
* Adding the ability to search all atomics based on a keyword or string. Fixes [#59](https://github.com/swimlane/atomic-operator/issues/59) ([aad5165](https://github.com/swimlane/atomic-operator/commit/aad5165db5370f8f34310c2514f9e9fe400933e3))


### Bug Fixes

* Fixing variable replacement for powershell commands instead of command_prompt. Fixed [#58](https://github.com/swimlane/atomic-operator/issues/58) ([c4dbb69](https://github.com/swimlane/atomic-operator/commit/c4dbb69b5fb7bbdfd47ddf96a1036648f2c4ba1e))
* Resolving issues with passing multiple test_guids and creating the appropriate run list. Fixes [#57](https://github.com/swimlane/atomic-operator/issues/57) ([d669086](https://github.com/swimlane/atomic-operator/commit/d669086482e66d1b6943d4b8d413c0325913f2b7))
* Update imports ([a5dd297](https://github.com/swimlane/atomic-operator/commit/a5dd297c106e9cf699d8dcff4d21223cdf41d6e2))
* Updated tests to match new schema ([0c7767a](https://github.com/swimlane/atomic-operator/commit/0c7767aea1e12ca14df01f404c8d8c894a8b0990))
* Updating meta and moved attributes to init in package root ([df2d93d](https://github.com/swimlane/atomic-operator/commit/df2d93d7321b5abd6496fb4e443586b85263b698))


### Documentation

* Update README ([c6e89d0](https://github.com/swimlane/atomic-operator/commit/c6e89d0bac7a3c84a080d73f4296ece48f33c102))
* Updated README ([0eff976](https://github.com/swimlane/atomic-operator/commit/0eff9763b3fde9ebe27f3436f3806e87d24b254d))

## 0.8.4 - 2022-03-25

    * Updated formatting of executor for AWS and local runners
    * Updated documentation
    * Added formatting constants to base class to improve updating of windows variables on command line runners

## 0.7.0 - 2022-01-04

    * Updated argument handling in get_atomics Retrieving Atomic Tests with specified destination in /opt throws unexpected keyword argument error #28
    * Updated error catching and logging within state machine class when copying source files to remote system Logging and troubleshooting question #32
    * Updated ConfigParser from instance variables to local method bound variables Using a second AtomicOperator instance executes the tests of the first instance too #33
    * Added the ability to select specific tests for one or more provided techniques
    * Updated documentation
    * Added new Copier class to handle file transfer for remote connections
    * Removed gathering of supporting_files and passing around with object
    * Added new config_file_only parameter to only run the defined configuration within a configuration file
    * Updated documentation around installation on macOS systems with M1 processors

## 0.6.0 - 2021-12-17

    * Updated documentation
    * Added better handling of help

## 0.5.1 - 2021-11-18

    * Updating handling of passing --help to the run command
    * Updated docs to reflect change

## 0.5.0 - 2021-11-18

    * Updated handling of versioning
    * Updated CI to handle versioning of docs and deployment on release
    * Added better handling of extracting zip file
    * Added safer loading of yaml files
    * Update docs
    * Improved logging across the board and implemented a debug switch

## 0.4.0 - 2021-11-15

    * Added support for transferring files during remote execution
    * Refactored config handling
    * Updated docs and githubpages

## 0.2.0 - 2021-10-05

    * Added support for remote execution of atomic-tests
    * Added support for executing iaas:aws tests
    * Added configuration support
    * Plus many other features

## 0.0.1 - 2021-07-26

* Initial release
