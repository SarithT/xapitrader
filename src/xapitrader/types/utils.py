from typing import NamedTuple
import inspect

def unpack_dict_to(response_dict: dict, struct: NamedTuple):
    mapping = {}
    tuple_params = [p for p in inspect.signature(struct).parameters.values()]
    for k, v in response_dict.items():
        for p in tuple_params:
            if p.annotation in [str, int, float, bool]:
                if k == p.name:
                    mapping[k] = v
            else:
                nested_mapping = unpack_dict_to(response_dict, p.annotation)
                mapping[p.name] = p.annotation(**nested_mapping)
    return mapping

def unpack_to(response_dict: dict, struct: NamedTuple):
    return struct(**unpack_dict_to(response_dict, struct))