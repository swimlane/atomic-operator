# CHANGELOG

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

## 0.5.0 - 2021-11-19

    * Updated and expanded tests
    * Added CI to build docs and deploy to pypi
    * Updated localrunner to support windows based on changes made previously

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
