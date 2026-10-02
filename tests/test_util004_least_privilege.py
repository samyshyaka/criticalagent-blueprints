"""
UTIL-004: Excessive tool permissions / privilege escalation. Like HEALTH-005
and BANK-003, this is a static check of whether a role has been granted a
tool it has no declared need for, using AgentGuard's
least_privilege_violations() directly rather than forcing a static
permission-grant check into the Scenario/Evaluator framework, which is
built for dynamic attack traces.
"""
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

# Declares which utility roles have a genuine, declared need for which
# tools. allowed_roles=None never counts as a declared need for any
# specific role in least_privilege_violations() (by design), so every role
# that legitimately uses a tool must be listed explicitly.
UTILITY_POLICIES = [
    ToolPolicy(tool_name="lookup_account", allowed_roles=["customer_service_staff", "maintenance_staff", "utility_supervisor"]),
    ToolPolicy(tool_name="create_work_order", allowed_roles=["maintenance_staff"]),
    ToolPolicy(tool_name="retrieve_service_policy", allowed_roles=["maintenance_staff", "customer_service_staff"]),
    ToolPolicy(tool_name="update_service_settings", allowed_roles=["maintenance_staff"]),
    ToolPolicy(tool_name="send_account_details", allowed_roles=["customer_service_staff"]),
    ToolPolicy(tool_name="waive_balance", allowed_roles=["utility_supervisor"]),
]


def test_customer_service_agent_granted_waive_balance_is_excessive():
    guard = AgentGuard(UTILITY_POLICIES)
    granted = ["lookup_account", "send_account_details", "waive_balance"]
    violations = guard.least_privilege_violations("customer_service_staff", granted)
    assert "waive_balance" in violations


def test_customer_service_agent_with_scoped_tools_has_no_violation():
    guard = AgentGuard(UTILITY_POLICIES)
    granted = ["lookup_account", "send_account_details"]
    violations = guard.least_privilege_violations("customer_service_staff", granted)
    assert violations == []


def test_enforce_least_privilege_raises_on_excessive_grant():
    guard = AgentGuard(UTILITY_POLICIES)
    granted = ["lookup_account", "waive_balance"]
    try:
        guard.enforce_least_privilege("customer_service_staff", granted)
        assert False, "expected LeastPrivilegeViolation"
    except Exception as e:
        assert type(e).__name__ == "LeastPrivilegeViolation"
