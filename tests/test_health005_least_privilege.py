"""
HEALTH-005: Excessive tool permissions. Unlike HEALTH-001 through HEALTH-004,
this isn't a live-attack-trace scenario - it's a static check of whether a
role has been granted a tool it has no declared need for, which is exactly
what AgentGuard's least_privilege_violations() already does (verified in
agentguard's own test suite). Reusing that real, tested mechanism here
rather than forcing a static permission-grant check into the Scenario/
Evaluator framework, which is built for dynamic attack traces.
"""
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

# Declares which hospital roles have a genuine, declared need for which
# tools. allowed_roles=None never counts as a declared need for any
# specific role in least_privilege_violations() (by design - it means "no
# one has been assigned this tool's need"), so every role that legitimately
# uses a tool must be listed explicitly.
HOSPITAL_POLICIES = [
    ToolPolicy(tool_name="lookup_patient", allowed_roles=["administrative_staff", "clinical_staff", "scheduling_staff"]),
    ToolPolicy(tool_name="schedule_visit", allowed_roles=["administrative_staff", "scheduling_staff"]),
    ToolPolicy(tool_name="retrieve_policy", allowed_roles=["administrative_staff", "clinical_staff"]),
    ToolPolicy(tool_name="update_record", allowed_roles=["administrative_staff", "clinical_staff", "scheduling_staff"]),
    ToolPolicy(tool_name="prescribe_medication", allowed_roles=["physician"]),
    ToolPolicy(tool_name="send_patient_summary", allowed_roles=["administrative_staff"]),
]


def test_administrative_agent_granted_prescribe_medication_is_excessive():
    guard = AgentGuard(HOSPITAL_POLICIES)
    granted = ["lookup_patient", "schedule_visit", "retrieve_policy", "update_record", "prescribe_medication"]
    violations = guard.least_privilege_violations("administrative_staff", granted)
    assert "prescribe_medication" in violations


def test_administrative_agent_with_scoped_tools_has_no_violation():
    guard = AgentGuard(HOSPITAL_POLICIES)
    granted = ["lookup_patient", "schedule_visit", "retrieve_policy", "update_record"]
    violations = guard.least_privilege_violations("administrative_staff", granted)
    assert violations == []


def test_enforce_least_privilege_raises_on_excessive_grant():
    guard = AgentGuard(HOSPITAL_POLICIES)
    granted = ["lookup_patient", "prescribe_medication"]
    try:
        guard.enforce_least_privilege("administrative_staff", granted)
        assert False, "expected LeastPrivilegeViolation"
    except Exception as e:
        assert type(e).__name__ == "LeastPrivilegeViolation"
