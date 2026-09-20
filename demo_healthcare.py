from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

from mock_hospital.environment import HospitalEnvironment
from mock_hospital.tools import lookup_patient_tool, prescribe_medication_tool
from mock_hospital.scenario import UrgentPrescriptionChangeScenario
from mock_hospital.agents import RushedIntakeAgent, CompliantIntakeAgent

print("=== CriticalAgent-Blueprints: Mock Hospital ===")
print("Scenario: Urgent Prescription Change (social-engineering pattern)\n")

scenario = UrgentPrescriptionChangeScenario()
tools = [lookup_patient_tool, prescribe_medication_tool]

for agent in [RushedIntakeAgent(), CompliantIntakeAgent()]:
    print(f"--- Agent: {agent.name} ---")

    evaluator = Evaluator(tools=tools)
    env = HospitalEnvironment()
    result = evaluator.run(scenario, agent, env)
    print(f"AgentSec-Bench detection - Attack succeeded: {result.attack_succeeded}")
    print(f"  Role violations: {result.unauthorized_tool_calls}")
    print(f"  Suspicious destinations: {result.suspicious_destinations}")

    guard = AgentGuard([ToolPolicy(tool_name="prescribe_medication", allowed_roles=["physician"], max_value=None)])
    messages, trace = agent.query(scenario.prompt, tools, HospitalEnvironment())
    blocked = []
    for call in trace:
        decision = guard.check(call.tool_name, call.args, agent_role=agent.role)
        if not decision.allowed:
            blocked.append((call.tool_name, decision.reason))
    print(f"AgentGuard prevention - Blocked: {blocked}")
    print()