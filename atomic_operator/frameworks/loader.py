import os


from .atomic import Atomic
from ..base import Base
from .emulation import (
    EmulationPhase,
    EmulationPlanDetails
)
from ..utils.exceptions import ContentFolderNotFound


class Loader(Base):

    _techniques = {}
    TECHNIQUE_DIRECTORY_PATTERN = 'T*'

    def load(self) -> dict:
        path = Base.CONFIG.content_path
        if not os.path.exists(self.get_abs_path(path)):
            raise ContentFolderNotFound('Unable to find any folders containing content. Please make sure you have provided the correct path.')
        else:
            content = self._find_content(path=self.get_abs_path(path), pattern='**/T*/T*.yaml')
            if not content:
                content = self._find_content(path=self.get_abs_path(path), pattern='Emulation_Plan/yaml/*.yaml')
                if not content:
                    raise ContentFolderNotFound('Unable to find any folders containing content. Please make sure you have provided the correct path.')
        for item in content:
            self.__logger.debug(f"Item is {item}")
            name = self._get_file_name(item)
            if not self._techniques.get(name):
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
                        self._techniques[name] = EmulationPlanDetails(**emulation)
                    elif isinstance(loaded_technique, dict):
                        # This means it is in the structure of an Atomic
                        loaded_technique.update({'path': os.path.dirname(str(item))})
                        self._techniques[name] = Atomic(**loaded_technique)
        return self._techniques
