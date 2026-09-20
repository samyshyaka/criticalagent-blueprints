from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

from community_bank.environment import BankEnvironment
from community_bank.tools import lookup_account_tool, transfer_funds_tool
from community_bank.scenario import UrgentWireTransferScenario
from community_bank.agents import SympatheticBankAgent, ProceduralBankAgent

print("=== CriticalAgent-Blueprints: Community Bank ===")
print("Scenario: Urgent Wire Transfer (social-engineering pattern)\n")

scenario = UrgentWireTransferScenario()
tools = [lookup_account_tool, transfer_funds_tool]

for agent in [SympatheticBankAgent(), ProceduralBankAgent()]:
    print(f"--- Agent: {agent.name} ---")

    evaluator = Evaluator(tools=tools)
    env = BankEnvironment()
    result = evaluator.run(scenario, agent, env)
    print(f"AgentSec-Bench detection - Attack succeeded: {result.attack_succeeded}")
    print(f"  Role violations: {result.unauthorized_tool_calls}")
    print(f"  Suspicious destinations: {result.suspicious_destinations}")

    guard = AgentGuard([ToolPolicy(tool_name="transfer_funds", allowed_roles=["bank_officer"], max_value=500.0)])
    messages, trace = agent.query(scenario.prompt, tools, BankEnvironment())
    blocked = []
    for call in trace:
        decision = guard.check(call.tool_name, call.args, agent_role=agent.role)
        if not decision.allowed:
            blocked.append((call.tool_name, decision.reason))
    print(f"AgentGuard prevention - Blocked: {blocked}")
    print()