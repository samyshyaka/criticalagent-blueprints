from agentsec_bench.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

from mock_utility.environment import UtilityEnvironment
from mock_utility.tools import lookup_account_tool, waive_balance_tool
from mock_utility.scenario import UrgentBalanceWaiverScenario
from mock_utility.agents import PressuredServiceAgent, ProceduralServiceAgent

print("=== CriticalAgent-Blueprints: Municipal Utility ===")
print("Scenario: Urgent Balance Waiver (social-engineering pattern)\n")

scenario = UrgentBalanceWaiverScenario()
tools = [lookup_account_tool, waive_balance_tool]

for agent in [PressuredServiceAgent(), ProceduralServiceAgent()]:
    print(f"--- Agent: {agent.name} ---")

    evaluator = Evaluator(tools=tools)
    env = UtilityEnvironment()
    result = evaluator.run(scenario, agent, env)
    print(f"AgentSec-Bench detection - Attack succeeded: {result.attack_succeeded}")
    print(f"  Role violations: {result.unauthorized_tool_calls}")
    print(f"  Suspicious destinations: {result.suspicious_destinations}")

    guard = AgentGuard([ToolPolicy(tool_name="waive_balance", allowed_roles=["utility_supervisor"], max_value=100.0)])
    messages, trace = agent.query(scenario.prompt, tools, UtilityEnvironment())
    blocked = []
    for call in trace:
        decision = guard.check(call.tool_name, call.args, agent_role=agent.role)
        if not decision.allowed:
            blocked.append((call.tool_name, decision.reason))
    print(f"AgentGuard prevention - Blocked: {blocked}")
    print()