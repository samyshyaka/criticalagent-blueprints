from agentsec_bench.core.evaluator import Evaluator
from community_bank.environment import BankEnvironment
from community_bank.scenario import MaliciousRetrievedPolicyScenario
from community_bank.tools import retrieve_bank_policy_tool, update_profile_tool
from community_bank.agents import CustomerServiceAgentSusceptible, CustomerServiceAgentResistant


def test_ground_truth_passes_sanity_check():
    evaluator = Evaluator(tools=[retrieve_bank_policy_tool, update_profile_tool])
    result = evaluator.check_scenario(MaliciousRetrievedPolicyScenario(), BankEnvironment)
    assert result[0] is True, result[1]


def test_susceptible_agent_triggers_attack():
    evaluator = Evaluator(tools=[retrieve_bank_policy_tool, update_profile_tool])
    result = evaluator.run(MaliciousRetrievedPolicyScenario(), CustomerServiceAgentSusceptible(), BankEnvironment())
    assert result.attack_succeeded is True
    assert result.task_completed is True


def test_resistant_agent_does_not_trigger_attack():
    evaluator = Evaluator(tools=[retrieve_bank_policy_tool, update_profile_tool])
    result = evaluator.run(MaliciousRetrievedPolicyScenario(), CustomerServiceAgentResistant(), BankEnvironment())
    assert result.attack_succeeded is False
    assert result.task_completed is True
