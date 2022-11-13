import logging
import logging.config


class Logs:
    @staticmethod
    def log(text: str) -> None:
        dictLogConfig = {
            "version": 1,
            "handlers": {
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "formatter": "myFormatter",
                    "filename": "config.log"
                }
            },
            "loggers": {
                "Logs": {
                    "handlers": ["fileHandler"],
                    "level": "ERROR"
                }
            },
            "formatters": {
                "myFormatter": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s"
                }
            },

        }
        logging.config.dictConfig(dictLogConfig)
        logger = logging.getLogger("Logs")
        logger.error(text)
