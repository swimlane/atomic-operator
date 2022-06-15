from .base import Base


class AtomicOperator(Base):

    """Main class used to run Atomic Red Team tests or Adversary Emulation Plans.

    atomic-operator is used to run Atomic Red Team tests or Adversary Emulation Plans both locally and remotely.
    These tests (atomics) are predefined tests to mock or emulate a specific technique.

    config_file definition:
            atomic-operator's run method can be supplied with a path to a configuration file (config_file) which defines 
            specific tests and/or values for input parameters to facilitate automation of said tests.
            An example of this config_file can be seen below:

                inventory:
                  linux1:
                    executor: ssh
                    authentication:
                      username: root
                      password: ***REMOVED***
                      #ssk_key_path:
                      port: 22
                      timeout: 5
                    hosts:
                      # - 192.168.1.1
                      - 10.32.100.199
                      # etc.
                atomic_tests:
                  - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
                    input_arguments:
                      output_file:
                        value: custom_output.txt
                      input_file:
                        value: custom_input.txt
                  - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
                    input_arguments:
                      second_arg:
                        value: SWAPPPED argument
                  - guid: 32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2
                    inventories:
                      - linux1
                adversary_emulation:
                  - name: fin6
                    input_arguments:
                      output_file:
                        value: custom_output.txt
                      input_file:
                        value: custom_input.txt
                    inventories:
                      - windows1
    """

    def help(self, method=None):
        from fire.trace import FireTrace
        from fire.helptext import HelpText
        obj = AtomicOperator if not method else getattr(self, method)
        return HelpText(self, trace=FireTrace(obj))

    @property
    def art(self):
        """Redirect entry point to run Atomic Red Team tests
        """
        return self.atomic_red_team

    @property
    def atomic_red_team(self):
        """Main entry point to run test from the Adversary Emulation Library

        https://github.com/center-for-threat-informed-defense/adversary_emulation_library

        Raises:
            NotImplemented: _description_
        """
        from .atomic_red_team import AtomicRedTeam
        return AtomicRedTeam()

    @property
    def adversary_emulation(self):
        """Main entry point to run test from the Adversary Emulation Library

        https://github.com/center-for-threat-informed-defense/adversary_emulation_library

        Raises:
            NotImplemented: _description_
        """
        from .adversary_emulation import AdversaryEmulationLibrary
        return AdversaryEmulationLibrary()
