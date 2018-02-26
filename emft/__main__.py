# coding=utf-8
"""
Main entry-point
"""


def main():
    """
    Main entry point
    """
    import elib
    LOGGER = elib.custom_logging.get_logger('EMFT', use_click_handler=True, log_to_file=True)
    elib.custom_logging.set_root_logger(LOGGER)
    from emft.cli import cli
    cli()


if __name__ == '__main__':
    main()
