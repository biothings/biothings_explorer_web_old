import os, time, datetime
import logging
import inspect


def get_logger(logger_name, log_folder=None, timestamp="%Y%m%d", level=logging.DEBUG):
    """
    Configure a logger object from logger_name and return (logger, logfile)
    """
    from config import LOG_FILE_ROOT
    # if doesn't specify a log folder, use the default one in config
    if not log_folder:
        log_folder = LOG_FILE_ROOT
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    if timestamp:
        logfile = os.path.join(log_folder, '%s_%s.log' % (logger_name, time.strftime(timestamp, datetime.datetime.now().timetuple())))
    else:
        logfile = os.path.join(log_folder, '%s.log' % logger_name)
    fmt = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(name)s - %(levelname)s -- %(message)s', datefmt="%H:%M:%S")
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    fh = logging.FileHandler(logfile)
    fh.setFormatter(fmt)
    fh.name = "logfile"
    logger.addHandler(fh)
    return (logger, logfile)
