from typing import List, Iterator, Tuple


class LogEntry:
    @staticmethod
    def from_json(json_data):
        return LogEntry(json_data["name"], json_data["type"]["base"], json_data["type"]["name"], json_data["params"],
                 json_data["children"], json_data["loggers"])

    def __init__(self, name:str, base_type_name:str, type_name:str, params: dict, children: List[dict], loggers: List[dict]):
        """
        Each LogEntry represents an arithmetic expression. This can be a complete layer, the addition of the bias or multiplication of weights, but also the weights themselves.
        Args:
            name: Name of the layer/operation/variable/quantizer...
            base_type_name: base type can be "layer", "variable", "quantizer".
            type_name: a more concrete type. For a "layer" this could be "conv" or "dense".
            params: Special parameters that are important for the operation. For example, the stride of a convolutional operation.
            children: All sub expressions of this expression. So if the expression would be "a * (b + c)" there would be two children "a" and "b + c".
            loggers: All attached loggers to this expression. In most cases none or one. This list just points to a .gz file in the same directory as the structure.json
        """
        self.name = name
        self.base_type_name = base_type_name
        self.type_name = type_name
        self.params = params
        self.__children = children
        for d in self.__children:
            d:dict = d
            keys = [x for x in d.keys()]
            cur_child = d[keys[0]]
            if cur_child is not None:
                d[keys[0]] = LogEntry.from_json(cur_child)
        self.__loggers = loggers

    def get_child(self, name):
        for k, v in self.iterate_children():
            if k == name:
                return v
        raise Exception(f"Child not found {name}")

    def get_logger(self, name):
        for k, v in self.iterate_loggers():
            if k == name:
                return v
        raise Exception(f"Logger not found {name}")

    def iterate_children(self) -> Iterator[Tuple[str, object]]:
        """
        Iterates over all children. Each child has a name together with a LogEntry
        :return: An iterator over all children. Each element is a tuple with the name:str and the entry:LogEntry
        """
        result = []
        for d in self.__children:
            d: dict = d
            keys = [x for x in d.keys()]
            if d[keys[0]] is not None:
                result.append((keys[0], d[keys[0]]))
        return result

    def iterate_loggers(self) -> Iterator[Tuple[str, str]]:
        result = []
        for d in self.__loggers:
            d:dict = d
            keys = [x for x in d.keys()]
            if d[keys[0]] is not None:
                result.append((keys[0], d[keys[0]]))
        return result

