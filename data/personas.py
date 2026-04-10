PERSONAS = {
    "CISO": {
        "focus": [
            "risk prioritization",
            "breach exposure",
            "security program maturity",
            "governance",
            "executive confidence",
        ],
        "cares_about": "Whether the signal represents real risk that should be prioritized now, how it affects exposure, and how the organization demonstrates control.",
        "questions": [
            "Is this active risk or theoretical exposure?",
            "What is the business impact if this expands?",
            "What is the blast radius?",
            "How quickly can we contain and report this?",
        ],
    },
    "SOC Manager": {
        "focus": [
            "triage quality",
            "analyst efficiency",
            "signal fidelity",
            "incident response",
            "noise reduction",
        ],
        "cares_about": "Whether this signal is worth escalating, how confidently it maps to malicious activity, and whether it will improve response focus instead of creating more noise.",
        "questions": [
            "Is this behavior high-confidence enough to escalate?",
            "What evidence supports malicious activity?",
            "How should we sequence triage and containment?",
            "Is this likely to create additional alert volume?",
        ],
    },
    "Cloud Security Engineer": {
        "focus": [
            "runtime context",
            "policy coverage",
            "misconfiguration vs active risk",
            "identity exposure",
            "cloud control alignment",
        ],
        "cares_about": "How runtime evidence changes prioritization, what controls failed or are missing, and how posture and workload behavior connect.",
        "questions": [
            "What control should have caught this?",
            "Is this tied to identity, network, or workload behavior?",
            "Is this posture debt or active exploitability?",
            "What cloud-native control gaps are exposed here?",
        ],
    },
    "DevOps Lead": {
        "focus": [
            "release velocity",
            "developer workflow fit",
            "delivery safety",
            "pipeline trust",
            "application behavior",
        ],
        "cares_about": "Whether the issue is tied to changes in deployment, whether security can be integrated without slowing engineering, and how to preserve delivery confidence.",
        "questions": [
            "Did a recent deployment trigger this behavior?",
            "Is rollback or rollback avoidance the right move?",
            "Will the fix disrupt developer workflows?",
            "How can we catch this earlier without adding friction?",
        ],
    },
    "SRE": {
        "focus": [
            "service reliability",
            "incident stability",
            "blast radius",
            "MTTR",
            "on-call burden",
        ],
        "cares_about": "Whether the signal threatens uptime, reliability, or service health, and how to contain the issue without increasing downtime or operational chaos.",
        "questions": [
            "Is this affecting production stability right now?",
            "What is the blast radius across dependent services?",
            "Do we need rollback, isolation, or monitoring first?",
            "How will this affect on-call and recovery time?",
        ],
    },
    "Platform Engineer": {
        "focus": [
            "cluster health",
            "policy enforcement",
            "service dependencies",
            "runtime trust",
            "environment consistency",
        ],
        "cares_about": "How the issue affects shared platform integrity, whether policies are actually enforced, and whether one misbehaving service can impact others.",
        "questions": [
            "Is this isolated or systemic?",
            "What platform controls need tightening?",
            "Could this break shared services?",
            "Do we have enough context to remediate safely?",
        ],
    },
    "Customer Success Manager": {
        "focus": [
            "adoption",
            "value realization",
            "cross-team alignment",
            "customer outcomes",
            "renewal health",
        ],
        "cares_about": "How to turn technical findings into customer value, how to ensure stakeholders act on the insight, and how the platform becomes operationally embedded.",
        "questions": [
            "How does this tie to the customer’s stated goals?",
            "Which stakeholders need to be aligned?",
            "What success metric should we track from here?",
            "Does this reveal an adoption or workflow gap?",
        ],
    },
    "Executive / CIO": {
        "focus": [
            "business continuity",
            "organizational risk",
            "operational resilience",
            "accountability",
            "investment value",
        ],
        "cares_about": "Whether the organization can keep critical services stable, reduce operational disruption, and demonstrate that security investments are improving outcomes.",
        "questions": [
            "Does this put critical services at risk?",
            "Who owns the response?",
            "How does this affect continuity and customer trust?",
            "What does this say about our current operating model?",
        ],
    },
}
