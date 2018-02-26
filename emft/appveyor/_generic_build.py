# coding=utf-8
"""
Appveyor build
"""
import typing

import dateutil.parser
import humanize

from ._val import Val
from ._artifact import Artifact


def _natural_datetime(datetime: str) -> str:
    return humanize.naturalday(dateutil.parser.parse(datetime))


def _parse_artifacts(list_of_artifact):
    return [Artifact(artifact) for artifact in list_of_artifact]


class GenericBuild:
    """
    Appveyor build
    """

    build_id: int = Val(int)
    build_number: int = Val(int)
    version: str = Val(str)
    message: str = Val(str)
    branch: str = Val(str)
    is_tag: bool = Val(bool)
    tag: typing.Optional[str] = Val(str, mandatory=False)
    commit_id: str = Val(str)
    author_name: str = Val(str)
    committed: str = Val(_natural_datetime)
    status: str = Val(str)
    jobs: typing.List[dict] = Val(list)

    def __init__(self, json):
        self._json = json
