from agentsec_bench.core.evaluator import Evaluator
from mock_hospital.environment import HospitalEnvironment
from mock_hospital.scenario import MaliciousRetrievedPolicyScenario
from mock_hospital.tools import retrieve_policy_tool, update_record_tool
from mock_hospital.agents import ClinicalInfoAgentSusceptible, ClinicalInfoAgentResistant


def test_ground_truth_passes_sanity_check():
    evaluator = Evaluator(tools=[retrieve_policy_tool, update_record_tool])
    result = evaluator.check_scenario(MaliciousRetrievedPolicyScenario(), HospitalEnvironment)
    assert result[0] is True, result[1]


def test_susceptible_agent_triggers_attack():
    evaluator = Evaluator(tools=[retrieve_policy_tool, update_record_tool])
    result = evaluator.run(MaliciousRetrievedPolicyScenario(), ClinicalInfoAgentSusceptible(), HospitalEnvironment())
    assert result.attack_succeeded is True
    assert result.task_completed is True


def test_resistant_agent_does_not_trigger_attack():
    evaluator = Evaluator(tools=[retrieve_policy_tool, update_record_tool])
    result = evaluator.run(MaliciousRetrievedPolicyScenario(), ClinicalInfoAgentResistant(), HospitalEnvironment())
    assert result.attack_succeeded is False
    assert result.task_completed is True
