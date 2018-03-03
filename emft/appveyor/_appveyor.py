# coding=utf-8
"""
Downloads latest Miz file
"""
import typing

import elib
import requests
import requests.exceptions

from emft.context import CONTEXT
from ._artifact import Artifact
from ._generic_build import GenericBuild

_LOGGER = elib.custom_logging.get_logger('EMFT')


def _req(url) -> typing.Optional[dict]:
    _LOGGER.debug(f'request: {url}')
    try:
        req = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        _LOGGER.error('request for Appveyor build history timed out')
        return

    if not req.ok:
        _LOGGER.error(f'request for Appveyor build error: {req.reason}')
        return

    return req.json()


def _get_latest_build_on_current_branch(repo) -> typing.Optional[GenericBuild]:
    """
    Reads the active branch in the current Git repository and asks for the latest
    build of the equivalent branch on Appveyor

    :param repo: Appveyor repo in the form "owner/repo"

    :return: GenericBuild
    """
    _LOGGER.debug(f'current branch: {CONTEXT.branch}')
    build_json = _req(f'https://ci.appveyor.com/api/projects/{repo}/branch/{CONTEXT.branch}')
    if not build_json:
        return
    return GenericBuild(build_json['build'])


def _get_first_job_id_with_artifacts(build: GenericBuild) -> typing.Optional[str]:
    """
    Given an Appveyor build, returns the ID of the first job that has artifacts

    :param build: Generic Build

    :return: job ID as a string
    """
    if build.status != 'success':
        _LOGGER.warning(f'Appveyor build status: {build.status}')
        return

    if not build.jobs:
        _LOGGER.error('Appveyor build has no valid job')
        return

    for job in build.jobs:
        if job['status'] == 'success' and job['artifactsCount'] > 0:
            return job['jobId']


def _get_artifacts_from_job_id(job_id: str) -> typing.Optional[typing.List[Artifact]]:
    """
    Given a job ID, returns all the artifacts of that job

    :param job_id: job ID as a string

    :return: list of Artifact objects
    """
    artifacts_json = _req(f'https://ci.appveyor.com/api/buildjobs/{job_id}/artifacts')
    if not artifacts_json:
        return
    return [Artifact(json, job_id) for json in artifacts_json]


def get_latest_release(repo) -> typing.Optional[Artifact]:
    """
    Given an Appveyor repo, returns the latest MIZ artifact

    :param repo: Appveyor repo in the form "owner/repo"

    :return: Artifact object
    """
    build = _get_latest_build_on_current_branch(repo)
    if not build:
        _LOGGER.error('it seems this branch does not exist (yet?) on Appveyor')
        return
    job_id = _get_first_job_id_with_artifacts(build)
    artifacts = _get_artifacts_from_job_id(job_id)
    for artifact in artifacts:
        if artifact.file_name.endswith('.miz'):
            return artifact

    _LOGGER.warning('no valid MIZ artifacts found')
    return None
