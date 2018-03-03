# coding=utf-8

import typing
from pathlib import Path
from emiz.new_miz import NewMiz
import shutil
import ujson
from emiz.miz import ENCODING


class MissionFile(NewMiz):

    def __init__(self, path: typing.Union[Path, str]):
        NewMiz.__init__(self, path)


    # def decompose(self, output_folder: Path):
    #     if output_folder.exists():
    #         shutil.rmtree(output_folder.absolute())
    #     self.unzip()
    #     ignore = shutil.ignore_patterns('mission', 'mapResource', 'dictionary')
    #     shutil.copytree(self.temp_dir, output_folder.absolute(), ignore=ignore)
    #     self.decode()
    #     self._version = self.mission.d['version']
    #     mission_folder = output_folder.joinpath('mission')
    #     self._decompose_dict(self.mission.d, 'base_info', mission_folder)


    def __repr__(self):
        return f'MissionFile("{self.miz_path}")'
