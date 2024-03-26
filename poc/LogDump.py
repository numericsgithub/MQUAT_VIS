import json
from typing import List

import os
import gzip
import tensorflow as tf
from LogEntry import LogEntry

class LogDump:
    def __init__(self, folder_path):
        """
        Loads a log dataset
        Args:
            folder_path: the path to the folder containing the "structure.json" file
        """
        self.folder_path = folder_path
        structure_json_path = os.path.join(folder_path, "structure.json")
        if not os.path.exists(structure_json_path):
            raise Exception(f"File {structure_json_path} does not exists!")
        with open(structure_json_path, "r") as f:
            self.structure = json.load(f)
        print(json.dumps(self.structure, indent=4))
        self.entries: List[LogEntry] = []
        for entry in self.structure:
            self.entries.append(LogEntry.from_json(entry))

    def iterate_logger_content(self, logger_name):
        with gzip.open(self.get_logget_filepath(logger_name), "rb") as file:
            for tensor_bytes_str in file.read().split(b"###")[:-1]:
                yield tf.io.parse_tensor(tensor_bytes_str, tf.float32)

    def get_logget_filepath(self, logger_name):
        return os.path.join(self.folder_path, logger_name + ".gz")

