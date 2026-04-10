from data.value_messages import VALUE_MESSAGES


def build_value_translation(scenario: dict, persona: str) -> dict:
    technical_meaning = scenario["what_it_may_indicate"]
    security_meaning = scenario["security_risk"]
    operational_consequence = scenario["operational_impact"]
    business_outcome = scenario["business_impact"]

    value_story = (
        f"This signal shows why runtime context matters. For {persona}, the value is not just knowing "
        f"that something is exposed, but understanding that the behavior is active, meaningful, and "
        f"worthy of immediate attention. This helps reduce noise, improve prioritization, strengthen "
        f"cross-team coordination, and connect technical findings to real business outcomes."
    )

    if persona == "SRE":
        value_story = (
            "This signal matters because runtime anomalies often become reliability problems before teams "
            "can cleanly separate security from operations. The value is faster triage, lower on-call burden, "
            "and clearer containment decisions without losing production stability."
        )
    elif persona == "CISO":
        value_story = (
            "This signal matters because it moves the discussion from theoretical cloud risk to evidence of "
            "active behavior. That improves prioritization, supports clearer executive reporting, and helps "
            "security leaders focus resources on issues with real business consequence."
        )
    elif persona == "DevOps Lead":
        value_story = (
            "This signal matters because engineering teams need security context that fits into fast-moving "
            "delivery environments. The value is catching risky runtime behavior in a way that supports safer "
            "releases and better workflow alignment without unnecessary friction."
        )

    return {
        "technical_meaning": technical_meaning,
        "security_meaning": security_meaning,
        "operational_consequence": operational_consequence,
        "business_outcome": business_outcome,
        "value_story": value_story,
    }
