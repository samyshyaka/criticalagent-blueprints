from agentsec_bench.core.evaluator import Evaluator
from mock_utility.environment import UtilityEnvironment
from mock_utility.scenario import MaliciousRetrievedPolicyScenario
from mock_utility.tools import retrieve_service_policy_tool, update_service_settings_tool
from mock_utility.agents import WorkOrderAgentSusceptible, WorkOrderAgentResistant


def test_ground_truth_passes_sanity_check():
    evaluator = Evaluator(tools=[retrieve_service_policy_tool, update_service_settings_tool])
    result = evaluator.check_scenario(MaliciousRetrievedPolicyScenario(), UtilityEnvironment)
    assert result[0] is True, result[1]


def test_susceptible_agent_triggers_attack():
    evaluator = Evaluator(tools=[retrieve_service_policy_tool, update_service_settings_tool])
    result = evaluator.run(MaliciousRetrievedPolicyScenario(), WorkOrderAgentSusceptible(), UtilityEnvironment())
    assert result.attack_succeeded is True
    assert result.task_completed is True


def test_resistant_agent_does_not_trigger_attack():
    evaluator = Evaluator(tools=[retrieve_service_policy_tool, update_service_settings_tool])
    result = evaluator.run(MaliciousRetrievedPolicyScenario(), WorkOrderAgentResistant(), UtilityEnvironment())
    assert result.attack_succeeded is False
    assert result.task_completed is True
