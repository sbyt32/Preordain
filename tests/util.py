# Not for Testing
# ? Python 3.10 supports using | over union, but we are using this for compatability.
from typing import Union
import json


def get_sample_data(folder: str):
    with open(f"tests/{folder}/sample_data.json") as f:
        data: Union[dict, list] = json.load(f)
    return data
