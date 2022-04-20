import os
from pathlib import Path, PurePath

import yaml

from ..base import Base
from .atomic import Atomic
from .emulation import (
    EmulationPlanDetails,
    EmulationPhase
)
from ..utils.exceptions import ContentFolderNotFound


class Loader(Base):

    __techniques = {}
    TECHNIQUE_DIRECTORY_PATTERN = 'T*'

    def __get_file_name(self, path) -> str:
        return path.name.rstrip('.yaml')

    def __find_content(self, path, pattern):
        result = []
        path = PurePath(path)
        for p in Path(path).rglob(pattern):
            result.append(p.resolve())
        return result

    def load_yaml(self, path_to_dir) -> dict:
        """Loads a provided yaml file which is typically an Atomic or Emulation plan defintiion or configuration file.

        Args:
            path_to_dir (str): A string path to a yaml formatted file

        Returns:
            dict: Returns the loaded yaml file in a dictionary format
        """
        try:
            with open(self.get_abs_path(path_to_dir), 'r', encoding="utf-8") as f:
                return yaml.safe_load(f.read())
        except:
            self.__logger.warning(f"Unable to load technique in '{path_to_dir}'")
            
        try:
            # windows does not like get_abs_path so casting to string
            with open(str(path_to_dir), 'r', encoding="utf-8") as f:
                return yaml.safe_load(f.read())
        except OSError as oe:
            self.__logger.warning(f"Unable to load technique in '{path_to_dir}': {oe}")

    def load(self) -> dict:
        path = Base.CONFIG.content_path
        if not os.path.exists(self.get_abs_path(path)):
            raise ContentFolderNotFound('Unable to find any folders containing content. Please make sure you have provided the correct path.')
        else:
            content = self.__find_content(path=self.get_abs_path(path), pattern='**/T*/T*.yaml')
            if not content:
                content = self.__find_content(path=self.get_abs_path(path), pattern='Emulation_Plan/yaml/*.yaml')
                if not content:
                    raise ContentFolderNotFound('Unable to find any folders containing content. Please make sure you have provided the correct path.')
        for item in content:
            self.__logger.info(f"Item is {item}")
            name = self.__get_file_name(item)
            if not self.__techniques.get(name):
                loaded_technique = self.load_yaml(str(item))
                if loaded_technique:
                    if isinstance(loaded_technique, list):
                        phase_list = []
                        for i in loaded_technique:
                            if not i.get('emulation_plan_details') and i.get('id'):
                                phase_list.append(EmulationPhase(**i))
                        emulation = [x for x in loaded_technique if x.get('emulation_plan_details')]
                        if emulation:
                            emulation = emulation[0]
                            emulation = emulation.pop('emulation_plan_details')
                        emulation.update({
                            'path': os.path.dirname(str(item)),
                            'phases': phase_list
                        })
                        self.__techniques[name] = EmulationPlanDetails(**emulation)
                    elif isinstance(loaded_technique, dict):
                        # This means it is in the structure of an Atomic
                        loaded_technique.update({'path': os.path.dirname(str(item))})
                        self.__techniques[name] = Atomic(**loaded_technique)
        return self.__techniques
