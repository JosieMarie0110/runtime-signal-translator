def build_recommendations(scenario: dict) -> dict:
    immediate_next_steps = []
    immediate_next_steps.extend(scenario.get("technical_actions", [])[:2])
    immediate_next_steps.extend(scenario.get("operational_actions", [])[:2])

    customer_questions = [
        "Who currently owns response for this type of runtime issue?",
        "Is this workflow already operationalized across security, cloud, and engineering teams?",
        "What business-critical services could be affected if this expands?",
        "Does this expose a visibility, prioritization, or adoption gap in the current process?",
    ]

    success_plan_tie_in = (
        "Tie this scenario to success criteria around runtime visibility, incident readiness, cross-team workflow "
        "alignment, and measurable reduction in time-to-prioritize or time-to-contain."
    )

    qbr_talking_point = (
        "Highlight how runtime context helps the customer focus on real risk, reduce false urgency around lower-value "
        "findings, and improve alignment between security, SRE, DevOps, and leadership."
    )

    expansion_signal = (
        "If this scenario reveals gaps in API visibility, identity prioritization, workload protection, or cross-team "
        "operationalization, it may indicate room to expand adoption into adjacent platform capabilities."
    )

    return {
        "immediate_next_steps": immediate_next_steps,
        "customer_questions": customer_questions,
        "success_plan_tie_in": success_plan_tie_in,
        "qbr_talking_point": qbr_talking_point,
        "expansion_signal": expansion_signal,
    }
