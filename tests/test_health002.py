import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentsec_bench.core.evaluator import Evaluator
from mock_hospital.environment import HospitalEnvironment
from mock_hospital.tools import lookup_patient_tool, prescribe_medication_tool, send_patient_summary_tool
from mock_hospital.scenario import UnauthorizedRecordDisclosureScenario
from mock_hospital.agents import ForthcomingRecordsAgent, VerifyingRecordsAgent


def _evaluator():
    tools = [lookup_patient_tool, prescribe_medication_tool, send_patient_summary_tool]
    return Evaluator(tools=tools), tools


def test_ground_truth_passes_sanity_check():
    evaluator, _ = _evaluator()
    scenario = UnauthorizedRecordDisclosureScenario()
    ok, msg = evaluator.check_scenario(scenario, lambda: HospitalEnvironment())
    assert ok, msg


def test_forthcoming_agent_triggers_attack_and_suspicious_destination():
    evaluator, _ = _evaluator()
    scenario = UnauthorizedRecordDisclosureScenario()
    result = evaluator.run(scenario, ForthcomingRecordsAgent(), HospitalEnvironment())
    assert result.attack_succeeded is True
    assert result.task_completed is True
    assert len(result.suspicious_destinations) == 1
    assert result.suspicious_destinations[0]["tool"] == "send_patient_summary"


def test_verifying_agent_does_not_trigger_attack():
    evaluator, _ = _evaluator()
    scenario = UnauthorizedRecordDisclosureScenario()
    result = evaluator.run(scenario, VerifyingRecordsAgent(), HospitalEnvironment())
    assert result.attack_succeeded is False
    assert result.task_completed is True
    assert result.suspicious_destinations == []
