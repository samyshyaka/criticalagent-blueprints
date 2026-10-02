"""
BANK-003: Excessive tool permissions / privilege escalation. Like HEALTH-005,
this is a static check of whether a role has been granted a tool it has no
declared need for, using AgentGuard's least_privilege_violations() directly
rather than forcing a static permission-grant check into the Scenario/
Evaluator framework, which is built for dynamic attack traces.
"""
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

# Declares which bank roles have a genuine, declared need for which tools.
# allowed_roles=None never counts as a declared need for any specific role
# in least_privilege_violations() (by design), so every role that
# legitimately uses a tool must be listed explicitly.
BANK_POLICIES = [
    ToolPolicy(tool_name="lookup_account", allowed_roles=["customer_service_staff", "loan_officer", "fraud_analyst", "bank_officer"]),
    ToolPolicy(tool_name="calculate_loan", allowed_roles=["loan_officer"]),
    ToolPolicy(tool_name="update_profile", allowed_roles=["customer_service_staff"]),
    ToolPolicy(tool_name="send_account_statement", allowed_roles=["customer_service_staff"]),
    ToolPolicy(tool_name="retrieve_bank_policy", allowed_roles=["customer_service_staff", "loan_officer"]),
    ToolPolicy(tool_name="transfer_funds", allowed_roles=["bank_officer"]),
]


def test_loan_officer_granted_transfer_funds_is_excessive():
    guard = AgentGuard(BANK_POLICIES)
    granted = ["lookup_account", "calculate_loan", "transfer_funds"]
    violations = guard.least_privilege_violations("loan_officer", granted)
    assert "transfer_funds" in violations


def test_loan_officer_with_scoped_tools_has_no_violation():
    guard = AgentGuard(BANK_POLICIES)
    granted = ["lookup_account", "calculate_loan"]
    violations = guard.least_privilege_violations("loan_officer", granted)
    assert violations == []


def test_enforce_least_privilege_raises_on_excessive_grant():
    guard = AgentGuard(BANK_POLICIES)
    granted = ["lookup_account", "transfer_funds"]
    try:
        guard.enforce_least_privilege("loan_officer", granted)
        assert False, "expected LeastPrivilegeViolation"
    except Exception as e:
        assert type(e).__name__ == "LeastPrivilegeViolation"
