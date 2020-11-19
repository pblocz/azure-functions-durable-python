import logging

import azure.functions as func
import azure.durable_functions as df
from ..shared_code.MyClasses import SerializableClass # TODO: this import is highlight 'red' in VSCode, but works at runtime
import json

def orchestrator_function(context: df.DurableOrchestrationContext):
    """This function provides the core function chaining orchestration logic

    Parameters
    ----------
    context: DurableOrchestrationContext
        This context has the past history and the durable orchestration API's to
        create orchestrations

    Returns
    -------
    int
        The number contained in the SerializableClass input object
    """
    input_: SerializableClass = context.get_input()
    path1: str = input_.show_path()

    # The custom class is also correctly serialized when calling an activity
    obj = SerializableClass("container/with/hack")
    path2 = yield context.call_activity("DurableActivityWithHack", json.loads(SerializableClass.to_json(obj)))  # The json.loads is used ot not modify the code for SerializableClass, otherwise anohter function can be added to the class
    return path1, path2

main = df.Orchestrator.create(orchestrator_function)