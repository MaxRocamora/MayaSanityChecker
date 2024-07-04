# ----------------------------------------------------------------------------------------
# Maya Sanity Checker / Maximiliano Rocamora
# https://github.com/MaxRocamora/SanityChecker
# ----------------------------------------------------------------------------------------
import logging

# Additional Message types
DONE_LEVEL = 55
DONE_LEVEL_NAME = 'DONE'
HINT_LEVEL = 57
HINT_LEVEL_NAME = 'HINT'  # yellow
PROCESS_LEVEL = 65
PROCESS_LEVEL_NAME = 'PROCESS'  # cyan


def sanity_stream_logger(name: str):
    """Create a logger with additional message types."""
    log = logging.getLogger(name)
    log.propagate = False

    # Done level is a custom level for when a check is completed
    logging.addLevelName(DONE_LEVEL, DONE_LEVEL_NAME)

    # Process level is a custom level for when a check is in progress
    logging.addLevelName(PROCESS_LEVEL, PROCESS_LEVEL_NAME)

    # Hint level is a custom level to show a check hint text
    logging.addLevelName(HINT_LEVEL, HINT_LEVEL_NAME)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(name + ' - %(levelname)-7s | %(message)s')
    stream_handler.setFormatter(formatter)

    if len(log.handlers) == 0:
        log.addHandler(stream_handler)

    def log_for_level_done(message, *args, **kwargs):
        if log.isEnabledFor(DONE_LEVEL):
            log._log(DONE_LEVEL, message, args, **kwargs)

    def log_for_level_process(message, *args, **kwargs):
        if log.isEnabledFor(PROCESS_LEVEL):
            log._log(PROCESS_LEVEL, message, args, **kwargs)

    def log_for_level_hint(message, *args, **kwargs):
        if log.isEnabledFor(HINT_LEVEL):
            log._log(HINT_LEVEL, message, args, **kwargs)

    setattr(log, DONE_LEVEL_NAME, DONE_LEVEL)
    setattr(logging.getLoggerClass(), DONE_LEVEL_NAME, log_for_level_done)
    setattr(log, 'done', log_for_level_done)

    setattr(log, PROCESS_LEVEL_NAME, PROCESS_LEVEL)
    setattr(logging.getLoggerClass(), PROCESS_LEVEL_NAME, log_for_level_process)
    setattr(log, 'process', log_for_level_process)

    setattr(log, HINT_LEVEL_NAME, HINT_LEVEL)
    setattr(logging.getLoggerClass(), HINT_LEVEL_NAME, log_for_level_hint)
    setattr(log, 'hint', log_for_level_hint)

    log.setLevel(logging.DEBUG)
    return log


if __name__ == '__main__':
    log = sanity_stream_logger('test')
    log.info('test info')
    log.warning('test warning')
    log.error('test error')
    log.critical('test critical')
    log.debug('test debug')
    log.hint('test hint')
    log.process('test process')
    log.done('test done')
