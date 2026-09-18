from agentsec_bench.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

from mock_utility.environment import UtilityEnvironment
from mock_utility.tools import lookup_account_tool, waive_balance_tool
from mock_utility.scenario import UrgentBalanceWaiverScenario
from mock_utility.agents import PressuredServiceAgent, ProceduralServiceAgent


def test_pressured_agent_is_flagged_and_blocked():
    tools = [lookup_account_tool, waive_balance_tool]
    scenario = UrgentBalanceWaiverScenario()
    agent = PressuredServiceAgent()

    evaluator = Evaluator(tools=tools)
    result = evaluator.run(scenario, agent, UtilityEnvironment())
    assert result.attack_succeeded is True
    assert "waive_balance" in result.unauthorized_tool_calls

    guard = AgentGuard([ToolPolicy(tool_name="waive_balance", allowed_roles=["utility_supervisor"], max_value=100.0)])
    _, trace = agent.query(scenario.prompt, tools, UtilityEnvironment())
    blocked = [c.tool_name for c in trace if not guard.check(c.tool_name, c.args, agent_role=agent.role).allowed]
    assert "waive_balance" in blocked


def test_procedural_agent_is_not_flagged():
    tools = [lookup_account_tool, waive_balance_tool]
    scenario = UrgentBalanceWaiverScenario()
    agent = ProceduralServiceAgent()

    evaluator = Evaluator(tools=tools)
    result = evaluator.run(scenario, agent, UtilityEnvironment())
    assert result.attack_succeeded is False