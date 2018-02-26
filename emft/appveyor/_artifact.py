# coding=utf-8
"""
Appveyor artifact
"""
import typing
from pathlib import Path
import elib
import humanize

from ._val import Val


class Artifact:
    """
    Appveyor artifact
    """
    file_name: str = Val(str)
    name: str = Val(str)
    type: str = Val(str)
    size: int = Val(int)
    job_id: str = Val(str)

    def __init__(self, json, job_id: str):
        json['jobId'] = job_id
        self._json = json

    def __repr__(self):
        return f'Artifact({self.file_name}), {self.type}, {humanize.naturalsize(self.size)}'

    def download(self, outfile: typing.Union[str, Path]) -> bool:
        """
        Downloads this artifact

        :param outfile: target file
        :return: success of the operation as a bool
        """
        url = f'https://ci.appveyor.com/api/buildjobs/{self.job_id}/artifacts/{self.file_name}'
        return elib.downloader.download(url, outfile)
