# Get Content

Depending on which framework you are attempting to use, you must have that projects content in order to execute said tests or plans.

## Atomics

As part of the [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) project by [RedCanary](https://redcanary.com/), you must have these [atomics](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics) on you local system.

`atomic-operator atomic_red_team` uses these defined MITRE ATT&CK Technique tests (atomics) to run tests on your local system.

## Get Atomics

`atomic-operator atomic_red_team` provides you with the ability to download the Atomic Red Team repository. You can do so by running the following at the command line:

```bash
atomic-operator atomic_red_team get_content 
# You can specify the destination directory by using the --destination flag
atomic-operator atomic_red_team get_content  --destination "/tmp/some_directory"
```

Secondarily, you can also just clone or download the Atomics to your local system. To clone this repository, you can run:

```bash
git clone https://github.com/redcanaryco/atomic-red-team.git
cd atomic-red-team
```

You can also download this repository to your local system and extract the downloaded .zip.

That's it!  Once you have one or more atomics on your local system then we can begin to use `atomic-operator atomic_red_team run` to run these tests.


## Adversary Emulation Plans

As part of the [Adversary Emulation Plans](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) project by [MITRE](https://ctid.mitre-engenuity.org/), you must have these [plans](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) on you local system.

`atomic-operator adversary_emulation` uses emulation plans and their phases (which are mapoped to MITRE ATT&CK Techniques) to emulate a malicious threat actor on your desired system.

## Get Adversary Emulation Plans

`atomic-operator adversary_emulation` provides you with the ability to download the Adversary Emulation Library repository. You can do so by running the following at the command line:

```bash
atomic-operator adversary_emulation get_content 
# You can specify the destination directory by using the --destination flag
atomic-operator adversary_emulation get_content  --destination "/tmp/some_directory"
```

Secondarily, you can also just clone or download the plans to your local system. To clone this repository, you can run:

```bash
git clone https://github.com/center-for-threat-informed-defense/adversary_emulation_library.git
cd adversary_emulation_library
```

You can also download this repository to your local system and extract the downloaded .zip.

That's it!  Once you have one or more plans on your local system then we can begin to use `atomic-operator adversary_emulation run` to run these tests.
