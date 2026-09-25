# Human escalation — after audit 3 still FAIL

Do not start audit 4. Review the Auditor's root causes, the source snapshot, and the decision requested. Choose one path:

1. **Clarify or change the spec:** make the human decision, update acceptance criteria, assign a new `task_id`, and start a fresh revision-0 task.
2. **Split the task:** break it into smaller independently reviewable tasks with new IDs and explicit interfaces.
3. **Overrule a finding:** record the finding ID, rationale, owner, and accepted risk. Do not silently label it fixed.
4. **Stop or defer:** leave the patch unapplied until the unresolved issue is resolved.

A PASS from the GPT does not replace applying the patch, running project CI, or human release review.