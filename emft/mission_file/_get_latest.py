# coding=utf-8
import elib

from emft import appveyor
from emft.context import CONTEXT


LOGGER = elib.custom_logging.get_logger('EMFT')


def _latest_artifact() -> appveyor.Artifact:
    LOGGER.debug(f'getting latest mission from Appveyor, on branch: {CONTEXT.branch}')
    latest_artifact = appveyor.get_latest_release(CONTEXT.appveyor)
    LOGGER.debug(f'latest mission found: {latest_artifact.file_name}')
    return  latest_artifact


def get_latest_miz_file_in_source_folder():
    latest_artifact = _latest_artifact()
    if latest_artifact not in CONTEXT.source_folder.iterdir():
        outfile = CONTEXT.source_folder.joinpath(latest_artifact.file_name).absolute()
        LOGGER.warning(f'downloading latest mission from Appveyor into source folder: "{outfile}"')
        latest_artifact.download(outfile)


if __name__ == '__main__':
    get_latest_miz_file_in_source_folder()
