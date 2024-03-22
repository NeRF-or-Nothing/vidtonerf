import logging

def sfm_worker_logger(name='root'):
    """
        Initializer for a global sfm-worker logger.
            -> 
        To initialize use: 'logger = log.sfm_worker_logger(name)'
        To retrieve in different context: 'logger = logging.getLogger(name)'
    """
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.FileHandler(name+'.log', mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    theta = sfm_worker_logger('sfm-worker-test')
    theta.info("info message")
    theta.warning("warning message")
    theta.error("error message")
    theta.critical("critical message")