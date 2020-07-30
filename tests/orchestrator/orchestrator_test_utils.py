import json
from typing import Callable, Iterator, Any, Dict
from jsonschema import validate

from azure.durable_functions.models import DurableOrchestrationContext
from azure.durable_functions.orchestrator import Orchestrator
from .schemas.OrchetrationStateSchema import schema


def assert_orchestration_state_equals(expected, result):
    assert_attribute_equal(expected, result, "isDone")
    assert_actions_are_equal(expected, result)
    assert_attribute_equal(expected, result, "output")
    assert_attribute_equal(expected, result, "error")
    assert_attribute_equal(expected, result, "customStatus")


def assert_attribute_equal(expected, result, attribute):
    if attribute in expected:
        assert result.get(attribute) == expected.get(attribute)
    else:
        assert attribute not in result


def assert_actions_are_equal(expected, result):
    expected_actions = expected.get("actions")
    result_actions = result.get("actions")
    assert len(expected_actions) == len(result_actions)
    for index in range(len(expected_actions)):
        assert len(expected_actions[index]) == len(result_actions[index])
        for action_index in range(len(expected_actions[index])):
            expected_action = expected_actions[index][action_index]
            result_action = result_actions[index][action_index]
            assert_action_is_equal(expected_action, result_action)


def assert_action_is_equal(expected_action, result_action):
    assert_attribute_equal(expected_action, result_action, "functionName")
    assert_attribute_equal(expected_action, result_action, "input")
    assert_attribute_equal(expected_action, result_action, "actionType")


def get_orchestration_state_result(
        context_builder,
        activity_func: Callable[[DurableOrchestrationContext], Iterator[Any]],
        export_to_json: bool = False):
    context_as_string = context_builder.to_json_string()
    orchestrator = Orchestrator(activity_func)
    result_of_handle = orchestrator.handle(
        DurableOrchestrationContext.from_json(context_as_string))
    result = json.loads(result_of_handle)
    produce_reusable_testing_json(context_as_string, result_of_handle)
    return result

def produce_reusable_testing_json(context: str, result):
    context = json.loads(context)
    result = json.loads(result)

    json_tester = {
        "orchestrator_name": context["instanceId"],
        "orchestrator_input": context["input"],
        "history": context["history"],
        "extension_actions": result["actions"],
        "required_features": ""
    }
    err_key = "error"
    output_key = "output"
    if "error" in result.keys():
        json_tester["error_message"] = result[err_key]
    elif output_key in result.keys():
        json_tester["orchestrator_output"] = result[output_key]


def assert_valid_schema(orchestration_state):
    validation_results = validate(instance=orchestration_state, schema=schema)
    assert validation_results is None


def assert_dict_are_equal(expected: Dict[Any, Any], result: Dict[Any, Any]):
    assert len(expected.keys()) == len(result.keys())
    for key in expected.keys():
        assert expected[key] == result[key]
    for key in result.keys():
        assert result[key] == expected[key]
