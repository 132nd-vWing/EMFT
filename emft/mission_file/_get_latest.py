# coding=utf-8
import typing
from pathlib import Path

import elib
import natsort

from emft import appveyor
from emft.context import CONTEXT
from ._mission_file import MissionFile

LOGGER = elib.custom_logging.get_logger('EMFT')


def _latest_artifact() -> typing.Optional[appveyor.Artifact]:
    LOGGER.debug(f'getting latest mission from Appveyor, on branch: {CONTEXT.branch}')
    latest_artifact = appveyor.get_latest_release(CONTEXT.appveyor)
    if not latest_artifact:
        LOGGER.error('failed to retrieve latest mission from Appveyor')
        return

    LOGGER.debug(f'latest mission found: {latest_artifact.file_name}')
    return latest_artifact


def _get_latest_miz_in_source_folder() -> typing.Optional[MissionFile]:
    available_mission = set()
    for mission_file in CONTEXT.source_folder.iterdir():
        if mission_file.name.endswith('.miz'):
            mission_file = mission_file.absolute()
            available_mission.add(mission_file)
    if available_mission:
        return MissionFile(natsort.natsorted(available_mission, reverse=True)[0].absolute())

    LOGGER.warning(f'there is no mission file (yet?) in "{CONTEXT.source_folder}"')
    return None


def get_latest_miz_file_in_source_folder() -> typing.Optional[MissionFile]:
    latest_artifact = _latest_artifact()
    if not latest_artifact:
        return _get_latest_miz_in_source_folder()
    mission_path = CONTEXT.source_folder.joinpath(latest_artifact.file_name).absolute()
    if not mission_path.exists():
        LOGGER.warning(f'downloading latest mission from Appveyor into source folder: "{mission_path}"')
        latest_artifact.download(mission_path)
    return MissionFile(mission_path)
