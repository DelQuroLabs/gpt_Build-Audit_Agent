# Human escalation (after audit 3 still FAILs)

Do not start audit 4. Review the final Auditor report, the current complete artifact snapshot, and the decision requested. Choose one path and record it in your project log:

1. **Clarify or change the spec.** Make the decision, update the acceptance criteria, assign a new `task_id`, and start a fresh revision-0 task.
2. **Split the task.** Divide the GPT into smaller, independently reviewable builds with new IDs and explicit interfaces.
3. **Overrule a finding.** Record the finding ID, rationale, owner, accepted risk, and review date. Never call it fixed.
4. **Remove a capability.** If the issue is an Action, Knowledge source, or platform assumption, reduce scope and restart the relevant build.
5. **Stop or defer.** Do not publish the GPT until the issue is resolved.

A PASS never replaces testing the actual configured GPT, reviewing Knowledge and Action data flows, or getting human release approval.
