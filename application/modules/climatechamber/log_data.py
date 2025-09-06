import logging
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path

class LoggerSetup:

    def __init__(self, name, log_file_path, terminal=False, level=logging.INFO ):

        log_path = Path(log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)


        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.hasHandlers():
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            handler = TimedRotatingFileHandler(
                filename=log_file_path,
                when='midnight',
                interval=1,
                backupCount=30,
                encoding='utf-8'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            if terminal:
                terminal_logger = logging.StreamHandler()
                terminal_logger.setLevel(level)
                terminal_logger.setFormatter(formatter)
                self.logger.addHandler(terminal_logger)


    def get_logger(self):
        
        return self.logger
    


if __name__ == '__main__':

    test_logger = LoggerSetup('test', './logs', True)
