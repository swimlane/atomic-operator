import os
import attr


# Setting frozen to True means immutability (static) values once set
@attr.s(frozen=True)
class Config:

    atomics_path          = attr.ib()
    check_dependencies    = attr.ib(default=False)
    get_prereqs           = attr.ib(default=False)
    cleanup               = attr.ib(default=False)
    command_timeout       = attr.ib(default=20)
    show_details          = attr.ib(default=False)
    prompt_for_input_args = attr.ib(default=False)

    def __attrs_post_init__(self):
        object.__setattr__(self, 'atomics_path', self.__get_abs_path(self.atomics_path))

    def __get_abs_path(self, value):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    @atomics_path.validator
    def validate_atomics_path(self, attribute, value):
        value = self.__get_abs_path(value)
        if not os.path.exists(value):
            raise ValueError('Please provide a value for atomics_path that exists')
