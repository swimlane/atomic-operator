# Atomics

As part of the [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) project by [RedCanary](https://redcanary.com/), you must have these [atomics](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics) on you local system.

`atomic-operator` uses these defined MITRE ATT&CK Technique tests (atomics) to run tests on your local system.

## Get Atomics

`atomic-operator` provides you with the ability to download the Atomic Red Team repository. You can do so by running the following at the command line:

```bash
atomic-operator get_atomics 
# You can specify the destination directory by using the --destination flag
atomic-operator get_atomics --destination "/tmp/some_directory"
```

Secondarily, you can also just clone or download the Atomics to your local system. To clone this repository, you can run:

```bash
git clone https://github.com/redcanaryco/atomic-red-team.git
cd atomic-red-team
```

You can also download this repository to your local system and extract the downloaded .zip.

That's it!  Once you have one or more atomics on your local system then we can begin to use `atomic-operator` to run these tests.
