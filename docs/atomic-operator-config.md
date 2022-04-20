# Configuration

One feature of `atomic-operator` is the ability to automate running of Atomics or Emulation Plans even further via a configuration file. The configuration file supports many different layouts for configuration but the major features are:

* Define one or more Atomic tests by GUID or Emulation Plans by adversary name
  * You can provide values for any defined input arguments for an Atomic test
  * You can assign an Atomic test to one or more `inventory` objects
* Define none, one, or more `inventory` objects
  * An inventory is a collection of authentication properties as well as hosts associated with said authentication credentials

With this structure you can create an inventory group of 1 or 100 hosts using a set of credentials and tell `atomic-operator` to run 1 or more tests with defined inputs against those hosts - infinitely flexible.

Below is an example of all of these features implemented in a configuration file.

```yaml
inventory:
  windows1:
    executor: powershell # or cmd
    authentication:
      username: username
      password: some_passowrd!
      verify_ssl: false
    hosts:
      - 192.168.1.1
      - 10.32.1.1
      # etc
  linux1:
    executor: ssh
    authentication:
      username: username
      password: some_passowrd!
      #ssk_key_path:
      port: 22
      timeout: 5
    hosts:
      - 192.168.1.1
      - 10.32.100.1
      # etc.
adversary_emulation:
  - name: APT29
    input_arguments:
      output_file:
        value: custom_output.txt
      input_file:
        value: custom_input.txt
    inventories:
      - windows1
atomic_tests:
  - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
    input_arguments:
      output_file:
        value: custom_output.txt
      input_file:
        value: custom_input.txt
    inventories:
      - windows1
  - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
    input_arguments:
      second_arg:
        value: SWAPPPED argument
    inventories:
      - windows1
      - linux1
  - guid: c141bbdb-7fca-4254-9fd6-f47e79447e17
    inventories:
      - linux1
```

At the basic level of the configuration file you can simply just have one that defines a set of Atomic tests you want to run like so:

```yaml
atomic_tests:
  - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
  - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
  - guid: c141bbdb-7fca-4254-9fd6-f47e79447e17
```

Or you can define adversaries by their name.

```yaml
adversary_emulation:
  - name: fin6
  - name: APT29
```

You can also specify input variable values for one or more of them:

```yaml
atomic_tests:
  - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
    input_arguments:
      output_file:
        value: custom_output.txt
      input_file:
        value: custom_input.txt
  - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
  - guid: c141bbdb-7fca-4254-9fd6-f47e79447e17
adversary_emulation:
  - name: APT29
    input_arguments:
      output_file:
        value: custom_output.txt
      input_file:
        value: custom_input.txt
```

But if you want to run them remotely then you must add in `inventory` objects with the correct credentials and one or more hosts:

```yaml
inventory:
  windows1:
    executor: powershell # or cmd
    authentication:
      username: username
      password: some_passowrd!
      verify_ssl: false
    hosts:
      - 192.168.1.1
      - 10.32.1.1
atomic_tests:
  - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
    input_arguments:
      output_file:
        value: custom_output.txt
      input_file:
        value: custom_input.txt
    inventories:
      - windows1
  - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
  - guid: c141bbdb-7fca-4254-9fd6-f47e79447e17
adversary_emulation:
  - name: APT29
    input_arguments:
      output_file:
        value: custom_output.txt
      input_file:
        value: custom_input.txt
    inventories:
      - windows1
```
