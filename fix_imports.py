import os
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

MODULE_TO_SUBPKG = {
    "types": "core", "scenario": "core", "agent": "core", "evaluator": "core",
    "environment": "core", "environment_inbox": "core", "environment_crm": "core",
    "tools_expense": "tools", "tools_refund": "tools", "tools_inbox": "tools",
    "tools_crm": "tools", "tools_admin": "tools", "tools_devops": "tools",
    "tools_workspace": "tools", "tools_vendor": "tools", "tools_reporting": "tools",
    "scenarios_expense": "scenarios", "scenarios_ambiguous": "scenarios",
    "scenarios_injection": "scenarios", "scenarios_exfiltration": "scenarios",
    "scenarios_privilege": "scenarios", "scenarios_code_execution": "scenarios",
    "scenarios_rogue": "scenarios", "scenarios_memory_poisoning": "scenarios",
    "scenarios_trust_exploitation": "scenarios",
    "fake_agent": "agents", "good_agent": "agents", "refund_agents": "agents",
    "inbox_agents": "agents", "crm_agents": "agents", "admin_agents": "agents",
    "devops_agents": "agents", "workspace_agents": "agents", "vendor_agents": "agents",
    "reporting_agents": "agents",
}

ABS_IMPORT_RE = re.compile(r'^(\s*from\s+)agentsec_bench\.([A-Za-z_][A-Za-z0-9_]*)(\s+import\s+.+)$')


def rewrite_imports_in_file(py_path):
    with open(py_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    changed = False
    new_lines = []

    for line in lines:
        m = ABS_IMPORT_RE.match(line)
        if m:
            prefix, modname, rest = m.groups()
            target_subpkg = MODULE_TO_SUBPKG.get(modname)
            if target_subpkg is None:
                new_lines.append(line)
                continue
            new_line = f"{prefix}agentsec_bench.{target_subpkg}.{modname}{rest}\n"
            if new_line.strip() != line.strip():
                changed = True
            new_lines.append(new_line)
            continue
        new_lines.append(line)

    if changed:
        with open(py_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"  rewrote imports in {os.path.relpath(py_path, REPO_ROOT)}")


def main():
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in (".venv", ".git", "__pycache__")]
        for fname in files:
            if fname.endswith(".py"):
                rewrite_imports_in_file(os.path.join(root, fname))
    print("Done.")


if __name__ == "__main__":
    main()