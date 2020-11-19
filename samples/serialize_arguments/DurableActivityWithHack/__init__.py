import json
import logging
import azure.functions as func
from ..shared_code.MyClasses import SerializableClass

def main(value, outputBlob: func.Out[str]):
    """Activity function performing a specific step in the chain

    Parameters
    ----------
    value : SerializableClass
        Name of the item to be hello'ed at

    Returns
    -------
    str
        Returns the path string
    """
    logging.warning(f"Activity Triggered: {value}")

    outputBlob.set("Hello World!")

    value = SerializableClass.from_json(json.dumps(value))
    return value.path

