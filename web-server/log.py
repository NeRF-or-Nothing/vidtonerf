import logging

def web_server_logger(name='root'):
    """
        Initializer for a global web-server logger.
            -> 
        To initialize use: 'logger = log.web_server_logger(name)'
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
    theta = web_server_logger('web-server-test')
    theta.info("info message")
    theta.warning("warning message")
    theta.error("error message")
    theta.critical("critical message")