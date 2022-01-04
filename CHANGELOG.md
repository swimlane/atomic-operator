# CHANGELOG

## 0.7.0 - 2022-01-04

    * Updated argument handling in get_atomics Retrieving Atomic Tests with specified destination in /opt throws unexpected keyword argument error #28
    * Updated error catching and logging within state machine class when copying source files to remote system Logging and troubleshooting question #32
    * Updated ConfigParser from instance variables to local method bound variables Using a second AtomicOperator instance executes the tests of the first instance too #33
    * Added the ability to select specific tests for one or more provided techniques
    * Updated documentation

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
