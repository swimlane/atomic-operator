import os
from pathlib import Path, PurePath

import yaml

from ..base import Base
from .atomic import Atomic


class Loader(Base):

    __techniques = {}
    TECHNIQUE_DIRECTORY_PATTERN = 'T*'

    def __get_file_name(self, path):
        return path.name.rstrip('.yaml')

    def find_atomics(self, atomics_path, pattern='**/T*/T*.yaml'):
        result = []
        path = PurePath(atomics_path)
        for p in Path(path).rglob(pattern):
            result.append(p.resolve())
        return result

    def load_technique(self, path_to_dir):
        with open(str(path_to_dir), 'r', encoding="utf-8") as f:
            return yaml.load(f.read(), Loader=yaml.SafeLoader)

    def load_techniques(self):
        """The main entrypoint when loading techniques from disk.

        Raises:
            Exception: Thrown when unable to find the folder containing
                       Atomic tests

        Returns:
            dict: A dict with the key(s) as the Atomic technique ID and the val
                  is a list of Atomic objects.
        """
        atomics_path = Base.CONFIG.atomics_path
        if not os.path.exists(self.get_abs_path(atomics_path)):
            atomics_path = self.find_atomics(self.get_abs_path(__file__))
            if not atomics_path:
                raise Exception('Unable to find any atomics folder')
        else:
            atomics_path = self.find_atomics(atomics_path)
            if not atomics_path:
                raise Exception('Unable to find any atomics folder')

        for atomic_entry in atomics_path:
            technique = self.__get_file_name(atomic_entry)
            if not self.__techniques.get(technique):
                loaded_technique = self.load_technique(atomic_entry)
                loaded_technique.update({'path': atomic_entry})
                self.__techniques[technique] = Atomic(**loaded_technique)
        return self.__techniques
