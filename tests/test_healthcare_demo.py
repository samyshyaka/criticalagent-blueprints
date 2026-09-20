from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

from mock_hospital.environment import HospitalEnvironment
from mock_hospital.tools import lookup_patient_tool, prescribe_medication_tool
from mock_hospital.scenario import UrgentPrescriptionChangeScenario
from mock_hospital.agents import RushedIntakeAgent, CompliantIntakeAgent


def test_rushed_agent_is_flagged_and_blocked():
    tools = [lookup_patient_tool, prescribe_medication_tool]
    scenario = UrgentPrescriptionChangeScenario()
    agent = RushedIntakeAgent()

    evaluator = Evaluator(tools=tools)
    result = evaluator.run(scenario, agent, HospitalEnvironment())
    assert result.attack_succeeded is True
    assert "prescribe_medication" in result.unauthorized_tool_calls

    guard = AgentGuard([ToolPolicy(tool_name="prescribe_medication", allowed_roles=["physician"], max_value=None)])
    _, trace = agent.query(scenario.prompt, tools, HospitalEnvironment())
    blocked = [c.tool_name for c in trace if not guard.check(c.tool_name, c.args, agent_role=agent.role).allowed]
    assert "prescribe_medication" in blocked


def test_compliant_agent_is_not_flagged():
    tools = [lookup_patient_tool, prescribe_medication_tool]
    scenario = UrgentPrescriptionChangeScenario()
    agent = CompliantIntakeAgent()

    evaluator = Evaluator(tools=tools)
    result = evaluator.run(scenario, agent, HospitalEnvironment())
    assert result.attack_succeeded is False