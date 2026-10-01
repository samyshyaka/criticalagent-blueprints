import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentsec_bench.core.evaluator import Evaluator
from community_bank.tools import lookup_account_tool, transfer_funds_tool, send_account_statement_tool
from community_bank.scenario import UnauthorizedStatementDisclosureScenario
from community_bank.agents import DisclosingBankAgent, VerifyingBankAgent
from community_bank.environment import BankEnvironment


def _evaluator():
    tools = [lookup_account_tool, transfer_funds_tool, send_account_statement_tool]
    return Evaluator(tools=tools), tools


def test_ground_truth_passes_sanity_check():
    evaluator, _ = _evaluator()
    scenario = UnauthorizedStatementDisclosureScenario()
    ok, msg = evaluator.check_scenario(scenario, lambda: BankEnvironment())
    assert ok, msg


def test_disclosing_agent_triggers_attack_and_suspicious_destination():
    evaluator, _ = _evaluator()
    scenario = UnauthorizedStatementDisclosureScenario()
    result = evaluator.run(scenario, DisclosingBankAgent(), BankEnvironment())
    assert result.attack_succeeded is True
    assert result.task_completed is True
    assert len(result.suspicious_destinations) == 1
    assert result.suspicious_destinations[0]["tool"] == "send_account_statement"


def test_verifying_agent_does_not_trigger_attack():
    evaluator, _ = _evaluator()
    scenario = UnauthorizedStatementDisclosureScenario()
    result = evaluator.run(scenario, VerifyingBankAgent(), BankEnvironment())
    assert result.attack_succeeded is False
    assert result.task_completed is True
    assert result.suspicious_destinations == []
