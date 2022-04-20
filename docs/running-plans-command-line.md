# Running Adversary Emulation Plans

In order to run emulation plans using `atomic-operator` you must have one or more [adversary emulation plans](get_content.md).

## Selecting Adversary Plan to Run

`atomic-operator` will run all phases of a known emulation plan given the name of an adversary.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6
```

## Checking Dependencies

There is an optional parameter that determines if `atomic-operator` should check dependencies or not. By default we do not check dependenicies but if set to `True` we will.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6 --check_dependicies True
```

Checking of dependencies means we will run any defined `prereq_command` defined within each phase of the emulation plan. 

## Get Prerequisities

Another optional parameter deteremines if we retrieve or run any `get_prereq_command` values defined within each phase of a emulation plan.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6 --get_prereq_command
```

## Cleanup

This optional parameter is by default set to `False` but if set to `True` then we will run any `cleanup_command` values defined within an Atomic test.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/ adversary-emulation-library" --name fin6 --cleanup True
```

## Command Timeout

The `command_timeout` parameter tells `atomic-operator` the duration (in seconds) to run a command without exiting that process.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6 --command_timeout 40
```

This defaults to `20` seconds but you can specify another value if needed.

## Debug

The `debug` parameter will show additional details about the Emulation Plans and details within a phase (e.g. descriptions, etc.).

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6 --debug
```

The default value is `False` and must be set to `True` to show this extra detail.

## Interactive Argument Inputs

The `prompt_for_input_args` parameter will enable an interactive session and prompt you to enter arguments for any Emulation Plan that require input arguments. You can simply provide a value or select to use the `default` defined within the emulation plan.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6 --prompt_for_input_args
```

## kwargs

If you choose __not__ to set `prompt_for_input_args` to `True` then you can provide a dictionary of arguments in the `kwargs` input. This dictionary is only used for setting input argument values.  

For example, if you were running the Emulation Plan [fin6](https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin6/Emulation_Plan/yaml/FIN6.yaml#L30) then would pass in a dictionary into the kwargs argument.

### Additional Input Arguments from Command Line

If you do not want `atomic-operator` to prompt you for inputs you can simply run the following on the command line:

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6 --kwargs '{"adfind_url": "http://www.joeware.net/downloads/files/AdFind.zip"}'
```
