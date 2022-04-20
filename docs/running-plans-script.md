# Running Adversary Emulation Plans via scripts

In order to run emulation plans using `atomic-operator` you must have one or more [adversary emulation plans](get_content.md).

## Selecting Tests to Run

`atomic-operator` will run all phases of a known emulation plan given the name of an adversary.

```bash
atomic-operator adversary_emulation run --content-path "~/_Swimlane/adversary-emulation-library" --name fin6
```

```python
from atomic_operator import AtomicOperator

art = AtomicOperator()

print(art.adversary_emulation.run(content_path='my_local_folder/adversary-emulation-library'))
```

If you would like to specify specific tests then you must provide them as a list as input.

> Please note that techniques passed in but be separated by a `,` and __NO__ spaces.

```python
from atomic_operator import AtomicOperator

art = AtomicOperator()

print(art.adversary_emulation.run(
    name='fin6', 
    content_path='my_local_folder/adversary-emulation-library'
))
```

## Checking Dependencies

There is an optional parameter that determines if `atomic-operator` should check dependencies or not. By default we do not check dependenicies but if set to `True` we will.

```python
art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    check_dependencies=True
)
```

`check_dependencies` means we will run any defined `prereq_command` defined within each phase of an emulation plan.

## Get Prerequisities

Another optional parameter deteremines if we retrieve or run any `get_prereq_command` values defined within each phase of an emulation plan.

```python
art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    check_dependencies=True,
    get_prereq_command=True,
)
```

Setting this value to `True` means we will run that command but __only__ if `check_dependencies` is set to `True` as well. 

## Cleanup

This optional parameter is by default set to `False` but if set to `True` then we will run any `cleanup_command` values defined within each phase of an emulation plan.

```python
art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    cleanup=True
)
```

## Command Timeout

The `command_timeout` parameter tells `atomic-operator` the duration (in seconds) to run a command without exiting that process.

```python
art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    command_timeout=40
)
```

This defaults to `20` seconds but you can specify another value if needed.

## Debug

The `debug` parameter will show additional details about the emulation plan and it's phases.

```python
art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    debug=True
)
```

The default value is `False` and must be set to `True` to show this extra detail.

## Interactive Argument Inputs

The `prompt_for_input_args` parameter will enable an interactive session and prompt you to enter arguments for any Atomic test(s) that require input arguments. You can simply provide a value or select to use the `default` defined within each phase of an emulation plan.

```python
art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    prompt_for_input_args=True
)
```

The default value is `False` and must be set to `True` to prompt you for input values.

## kwargs

If you choose __not__ to set `prompt_for_input_args` to `True` then you can provide a dictionary of arguments in the `kwargs` input. This dictionary is only used for setting input argument values.  

For example, if you were running the Emulation Plan [fin6](https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin6/Emulation_Plan/yaml/FIN6.yaml#L30) then would pass in a dictionary into the kwargs argument.

If you do not want `atomic-operator` to prompt you for inputs you can simply run the following on the command line:

```python
inputs = {
    "adfind_url": "http://www.joeware.net/downloads/files/AdFind.zip"
}

art.adversary_emulation.run(
    content_path='my_local_folder/adversary-emulation-library',
    prompt_for_input_args=False,
    **inputs
)
```
