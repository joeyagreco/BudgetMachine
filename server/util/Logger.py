import errno
import json
import logging
import os
import uuid
from datetime import datetime
from typing import List


class Logger:

    @classmethod
    def __mkdir(cls, path):
        """
        http://stackoverflow.com/a/600612/190597 (tzot)
        https://stackoverflow.com/questions/20666764/python-logging-how-to-ensure-logfile-directory-is-created
        """
        try:
            os.makedirs(path, exist_ok=True)
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

    @classmethod
    def __getFileName(cls, name: str):
        logFolderPath = os.getenv("LOG_FILE_PATH")
        now = datetime.now()
        dateFolderPath = f"{name}//{now.year}//{now.month}//{now.day}//"
        fullPath = logFolderPath + dateFolderPath
        cls.__mkdir(fullPath)
        return f"{fullPath}{now.hour}-{now.minute}-{now.strftime('%S')}.log"

    @classmethod
    def log(cls, name: str, data: List):
        """
        Logs the given data to a new file and saves it.
        """
        with open(cls.__getFileName(name), "w") as f:
            for d in data:
                f.write(f"{str(d)}\n\n")
