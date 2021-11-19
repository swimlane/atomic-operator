import os
from atomic_operator import AtomicOperator
from atomic_operator.base import Base
from atomic_operator.atomic.atomictest import AtomicTest, AtomicTestInput
from atomic_operator.models import Config

def test_get_abs_path():
    assert Base().get_abs_path('./data/test_atomic2.yml')

def test_parse_input_lists():
    assert isinstance(Base().parse_input_lists('test,test,test'), list)

def test_replace_command_string():
    command = r'''[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
      $parentpath = Split-Path "#{gsecdump_exe}"; $binpath = "$parentpath\gsecdump-v2b5.exe"
      IEX(IWR "https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/Public/Invoke-WebRequestVerifyHash.ps1")
      if(Invoke-WebRequestVerifyHash "#{gsecdump_url}" "$binpath" #{gsecdump_bin_hash}){
        Move-Item $binpath "#{gsecdump_exe}"
      }'''
    test_inputs_list = []
    test_inputs_list.append(
        AtomicTestInput(
            name="gsecdump_exe",
            description="Path to the Gsecdump executable",
            type="Path",
            default="PathToAtomicsFolder\\T1003\\bin\\gsecdump.exe",
            value="PathToAtomicsFolder\\path\\to\\gsecdump.exe"
        )
    )
    test_inputs_list.append(
        AtomicTestInput(
            name="gsecdump_url",
            description="Path to download Gsecdump binary file",
            type="Url",
            default="https://web.archive.org/web/20150606043951if_/http://www.truesec.se/Upload/Sakerhet/Tools/gsecdump-v2b5.exe"
        ))
    for input in test_inputs_list:
        if input.value == None:
            input.value = input.default
    new_command = Base()._replace_command_string(command, '\\temp', input_arguments=test_inputs_list)
    assert new_command == r'''[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
      $parentpath = Split-Path "\temp\path\to\gsecdump.exe"; $binpath = "$parentpath\gsecdump-v2b5.exe"
      IEX(IWR "https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/Public/Invoke-WebRequestVerifyHash.ps1")
      if(Invoke-WebRequestVerifyHash "https://web.archive.org/web/20150606043951if_/http://www.truesec.se/Upload/Sakerhet/Tools/gsecdump-v2b5.exe" "$binpath" #{gsecdump_bin_hash}){
        Move-Item $binpath "\temp\path\to\gsecdump.exe"
      }'''

def test_setting_input_arguments():
    Base.CONFIG = Config(
        atomics_path=AtomicOperator().get_atomics(),
        prompt_for_input_args = False
    )
    test_inputs_list = []
    test_inputs_list.append(
        AtomicTestInput(
            name="gsecdump_exe",
            description="Path to the Gsecdump executable",
            type="Path",
            default="PathToAtomicsFolder\\T1003\\bin\\gsecdump.exe"
        )
    )
    test_input_dict = {
        'gsecdump_url': {
            'description': "Path to download Gsecdump binary file",
            'type':"Url",
            'default': "https://web.archive.org/web/20150606043951if_/http://www.truesec.se/Upload/Sakerhet/Tools/gsecdump-v2b5.exe"
        },
        'gsecdump_exe': {
            'description': "Path to the Gsecdump executable",
            'type':"Path",
            'default': "PathToAtomicsFolder\\T1003\\bin\\gsecdump.exe"
        }
    }
    
    kwargs = {
        'gsecdump_exe': '\\some\\test\\location',
        'gsecdump_url': 'google.com'
    }
    atomic_test = AtomicTest(
        name='test',
        description='test',
        supported_platforms=['linux'],
        auto_generated_guid='96345bfc-8ae7-4b6a-80b7-223200f24ef9',
        executor={
            'command': '''#{gsecdump_exe} -a''',
            'name': 'command_prompt',
            'elevation_required' : True
        },
        input_arguments=test_input_dict
    )
    Base()._set_input_arguments(atomic_test, **kwargs)
