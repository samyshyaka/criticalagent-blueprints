from agentsec_bench.core.evaluator import Evaluator
from mock_hospital.environment import HospitalEnvironment
from mock_hospital.scenario import SchedulingRequestInjectionScenario
from mock_hospital.tools import schedule_visit_tool, update_record_tool
from mock_hospital.agents import SchedulingAgentSusceptible, SchedulingAgentResistant


def test_ground_truth_passes_sanity_check():
    evaluator = Evaluator(tools=[schedule_visit_tool, update_record_tool])
    result = evaluator.check_scenario(SchedulingRequestInjectionScenario(), HospitalEnvironment)
    assert result[0] is True, result[1]


def test_susceptible_agent_triggers_attack():
    evaluator = Evaluator(tools=[schedule_visit_tool, update_record_tool])
    result = evaluator.run(SchedulingRequestInjectionScenario(), SchedulingAgentSusceptible(), HospitalEnvironment())
    assert result.attack_succeeded is True
    assert result.task_completed is True


def test_resistant_agent_does_not_trigger_attack():
    evaluator = Evaluator(tools=[schedule_visit_tool, update_record_tool])
    result = evaluator.run(SchedulingRequestInjectionScenario(), SchedulingAgentResistant(), HospitalEnvironment())
    assert result.attack_succeeded is False
    assert result.task_completed is True
