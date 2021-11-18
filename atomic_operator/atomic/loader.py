import os
from pathlib import Path, PurePath

import yaml

from ..base import Base
from .atomic import Atomic
from ..utils.exceptions import AtomicsFolderNotFound


class Loader(Base):

    __techniques = {}
    TECHNIQUE_DIRECTORY_PATTERN = 'T*'

    def __get_file_name(self, path) -> str:
        return path.name.rstrip('.yaml')

    def find_atomics(self, atomics_path, pattern='**/T*/T*.yaml') -> list:
        """Attempts to find the atomics folder within the provided atomics_path

        Args:
            atomics_path (str): A path to the atomic-red-team directory
            pattern (str, optional): Pattern used to find atomics and their required yaml files. Defaults to '**/T*/T*.yaml'.

        Returns:
            list: A list of paths of all identified atomics found in the given directory
        """
        result = []
        path = PurePath(atomics_path)
        for p in Path(path).rglob(pattern):
            result.append(p.resolve())
        return result

    def load_technique(self, path_to_dir) -> dict:
        """Loads a provided yaml file which is typically an Atomic defintiion or configuration file.

        Args:
            path_to_dir (str): A string path to a yaml formatted file

        Returns:
            dict: Returns the loaded yaml file in a dictionary format
        """
        try:
            with open(self.get_abs_path(path_to_dir), 'r', encoding="utf-8") as f:
                return yaml.safe_load(f.read())
        except:
            # windows does not like get_abs_path so casting to string
            with open(str(path_to_dir), 'r', encoding="utf-8") as f:
                return yaml.safe_load(f.read())

    def load_techniques(self) -> dict:
        """The main entrypoint when loading techniques from disk.

        Raises:
            AtomicsFolderNotFound: Thrown when unable to find the folder containing
                       Atomic tests

        Returns:
            dict: A dict with the key(s) as the Atomic technique ID and the val
                  is a list of Atomic objects.
        """
        atomics_path = Base.CONFIG.atomics_path
        if not os.path.exists(self.get_abs_path(atomics_path)):
            atomics_path = self.find_atomics(self.get_abs_path(__file__))
            if not atomics_path:
                raise AtomicsFolderNotFound('Unable to find any atomics folder')
        else:
            atomics_path = self.find_atomics(atomics_path)
            if not atomics_path:
                raise AtomicsFolderNotFound('Unable to find any atomics folder')

        for atomic_entry in atomics_path:
            technique = self.__get_file_name(atomic_entry)
            if not self.__techniques.get(technique):
                loaded_technique = self.load_technique(str(atomic_entry))
                loaded_technique.update({'path': os.path.dirname(str(atomic_entry))})
                self.__techniques[technique] = Atomic(**loaded_technique)
        return self.__techniques
