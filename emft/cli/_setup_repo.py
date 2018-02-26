# coding=utf-8
import elib
import git.exc

from emft.exit_ import exit_


def setup_repo():
    logger = elib.custom_logging.get_logger('EMFT')
    from emft.context import CONTEXT
    try:
        CONTEXT.repo = elib.repo.Repo()
        CONTEXT.branch = CONTEXT.repo.get_current_branch()
    except git.exc.InvalidGitRepositoryError:
        logger.error('you must run this application from within a valid Git repository')
        exit_(-1, err=True)
    logger.info(f'current branch: {CONTEXT.repo.get_current_branch()}')
