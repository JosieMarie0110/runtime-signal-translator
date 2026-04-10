import streamlit as st

st.set_page_config(
    page_title="Runtime Signal Translator",
    page_icon="🛰️",
    layout="wide",
)

# =========================================================
# DATA
# =========================================================
CATEGORY_ORDER = [
    "Container Runtime",
    "Kubernetes Behavior",
    "API Security",
    "Identity / Access",
    "Cloud Exposure",
    "DevOps / CI-CD Context",
]

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
        "priority": "Prioritize material risk, blast radius, and executive visibility.",
        "team_view": "Sees this as a leadership-level risk prioritization decision, not just a technical anomaly.",
        "message_style": "Frame in terms of exposure, urgency, and business consequence.",
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
        "priority": "Validate confidence quickly and reduce wasted analyst effort.",
        "team_view": "Views this through the lens of triage quality, detection fidelity, and escalation sequencing.",
        "message_style": "Frame around analyst efficiency, response quality, and confidence in the signal.",
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
        "priority": "Connect the signal to a control gap, failed guardrail, or runtime protection weakness.",
        "team_view": "Sees this as a runtime-informed cloud security problem that should map back to controls and posture.",
        "message_style": "Frame around control coverage, exploitability, and operational hardening.",
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
        "priority": "Protect delivery reliability without adding unnecessary developer friction.",
        "team_view": "Interprets this through release timing, pipeline trust, and application behavior changes.",
        "message_style": "Frame around safer releases, engineering fit, and workflow-friendly remediation.",
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
        "priority": "Protect production stability while containing the issue with the least operational disruption.",
        "team_view": "Sees this as both a security signal and a possible reliability incident.",
        "message_style": "Frame around uptime, blast radius, recovery time, and on-call burden.",
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
        "priority": "Determine whether the issue is isolated or reveals a broader platform weakness.",
        "team_view": "Sees this as a shared environment trust and consistency problem.",
        "message_style": "Frame around platform controls, dependency safety, and environment-wide impact.",
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
        "priority": "Translate the signal into value, action, and measurable customer outcomes.",
        "team_view": "Sees this as an opportunity to improve alignment, adoption, and platform operationalization.",
        "message_style": "Frame around outcomes, stakeholder coordination, and success-plan follow-through.",
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
        "priority": "Understand continuity risk, accountability, and whether operations remain resilient.",
        "team_view": "Interprets this through continuity, resilience, and executive accountability.",
        "message_style": "Frame around service continuity, trust, ownership, and investment value.",
    },
}

SCENARIOS = [
    # =====================================================
    # CONTAINER RUNTIME
    # =====================================================
    {
        "id": "container_unknown_egress",
        "title": "Container Communicating with Unknown External IP",
        "category": "Container Runtime",
        "environment": "Kubernetes",
        "cloud": "AWS",
        "signal": "Outbound traffic from a running container to an untrusted external IP not seen in normal service behavior.",
        "what_it_may_indicate": "Possible command-and-control communication, unauthorized egress, compromised workload behavior, or an early-stage exfiltration path.",
        "security_risk": "A workload may be compromised and actively communicating outside expected boundaries.",
        "operational_impact": "Response urgency increases because the issue touches both workload integrity and runtime network behavior.",
        "business_impact": "Raises breach exposure, increases incident response cost, and may affect confidence in production workload security.",
        "severity": "High",
        "affected_personas": ["SOC Manager", "Cloud Security Engineer", "SRE", "CISO"],
        "technical_actions": [
            "Inspect running processes inside the workload",
            "Validate image integrity and deployment source",
            "Review egress controls and network policy coverage",
            "Correlate with recent deployment or configuration changes",
        ],
        "operational_actions": [
            "Assign incident ownership across security and platform teams",
            "Document blast radius and impacted workloads",
            "Review whether alert routing and response playbooks are in place",
        ],
        "csm_angle": "Use this scenario to discuss runtime visibility, cross-team response readiness, and the maturity of workload protection workflows.",
        "persona_messages": {
            "SRE": "This matters because a runtime anomaly in a production workload can create both security risk and service instability. The goal is to contain the issue quickly while preserving uptime and reducing on-call burden.",
            "CISO": "This signal matters because it moves the conversation from theoretical exposure to evidence of suspicious runtime behavior, which is far more relevant for prioritization and risk reporting.",
            "DevOps Lead": "This is important because it may trace back to deployment changes, image provenance, or environment drift, and needs to be investigated without slowing the team unnecessarily.",
            "SOC Manager": "This is a high-priority signal because it suggests real malicious behavior rather than a static misconfiguration, which helps the team focus on response.",
            "Cloud Security Engineer": "This is the kind of runtime signal that should be mapped back to control coverage, egress policy, and workload protection gaps.",
            "Platform Engineer": "This may point to a broader policy enforcement or environment trust problem if similar workloads can communicate unexpectedly.",
            "Customer Success Manager": "This is a good opportunity to connect runtime visibility to customer value, especially around prioritization and response readiness.",
            "Executive / CIO": "This matters if it increases the likelihood of operational disruption or weakens confidence in cloud production controls.",
        },
    },
    {
        "id": "unexpected_process_execution",
        "title": "Unexpected Process Execution in Running Container",
        "category": "Container Runtime",
        "environment": "Containerized Workload",
        "cloud": "Multi-cloud",
        "signal": "A running container launches a process not associated with the known application baseline.",
        "what_it_may_indicate": "Container drift, malicious tooling, cryptomining activity, or unauthorized execution introduced after deployment.",
        "security_risk": "Runtime deviation suggests the workload may no longer match its trusted build state.",
        "operational_impact": "Can degrade performance, increase resource consumption, and complicate triage across platform and security teams.",
        "business_impact": "Undermines confidence in workload integrity and can drive outages, cloud cost growth, or delayed customer-facing services.",
        "severity": "High",
        "affected_personas": ["SRE", "Cloud Security Engineer", "Platform Engineer", "CISO"],
        "technical_actions": [
            "Capture process details and parent-child relationship",
            "Check image provenance and runtime drift indicators",
            "Assess CPU and memory impact on the host or cluster",
            "Review whether execution controls are defined for the workload",
        ],
        "operational_actions": [
            "Validate if the issue maps to a known deployment or maintenance action",
            "Escalate to both security and platform engineering",
            "Track operational impact to uptime or resource health",
        ],
        "csm_angle": "This supports conversations about runtime integrity, containment readiness, and protecting production trust without creating tool noise.",
        "persona_messages": {
            "SRE": "This is not just a security event. It may also signal a workload that is consuming resources abnormally and increasing the likelihood of service degradation.",
            "Platform Engineer": "Unexpected process execution can point to drift between approved workload behavior and production reality, which makes policy enforcement and trust harder.",
            "CISO": "This is evidence of runtime behavior that may justify immediate escalation because it suggests active deviation from expected controls.",
            "Cloud Security Engineer": "This should trigger a check of execution controls, image trust, and whether runtime policy is enforcing expected behavior.",
            "Customer Success Manager": "This scenario helps frame runtime integrity in a way customers can tie to operational trust and platform value.",
            "Executive / CIO": "Unexpected workload behavior matters if it affects service stability, cost, or confidence in production controls.",
            "SOC Manager": "The question is whether this is a clean escalation candidate and what evidence supports malicious execution versus benign drift.",
            "DevOps Lead": "This may require validating deployment history and whether the behavior stems from a recent release or unauthorized change.",
        },
    },

    # =====================================================
    # KUBERNETES BEHAVIOR
    # =====================================================
    {
        "id": "privileged_pod_created",
        "title": "Privileged Pod Created in Production Namespace",
        "category": "Kubernetes Behavior",
        "environment": "Kubernetes Cluster",
        "cloud": "AWS",
        "signal": "A new pod in a production namespace is deployed with privileged mode and elevated host access.",
        "what_it_may_indicate": "An overly permissive deployment, policy bypass, emergency engineering workaround, or a higher-risk path to node-level compromise.",
        "security_risk": "Privileged execution increases the chance that a compromised workload could impact the host or adjacent workloads.",
        "operational_impact": "Requires fast validation because it may expose shared cluster trust and complicate safe remediation.",
        "business_impact": "Weakens confidence in production guardrails and may increase exposure during an incident or audit review.",
        "severity": "High",
        "affected_personas": ["Platform Engineer", "Cloud Security Engineer", "CISO", "DevOps Lead"],
        "technical_actions": [
            "Inspect pod security context and admission history",
            "Validate whether policy enforcement should have blocked this deployment",
            "Review RBAC, service account, and namespace-level controls",
            "Confirm whether hostPath, privileged mode, or CAP_SYS_ADMIN access is present",
        ],
        "operational_actions": [
            "Determine whether the deployment was authorized or emergency-driven",
            "Coordinate with platform and engineering owners before remediation",
            "Assess whether similar privileges exist in adjacent namespaces",
        ],
        "csm_angle": "Use this to talk about workload hardening, policy adoption, and how customers operationalize Kubernetes guardrails over time.",
        "persona_messages": {
            "Platform Engineer": "This matters because one privileged workload can challenge trust across the cluster if enforcement is inconsistent.",
            "Cloud Security Engineer": "This should be tied directly to missing or bypassed pod security controls.",
            "DevOps Lead": "The key question is whether this was a necessary exception or a workflow gap that engineering normalized.",
            "CISO": "This is important because it shows a concrete breakdown between intended policy and actual production behavior.",
            "Customer Success Manager": "This can be positioned as a guardrail adoption and operationalization discussion, not just a one-off finding.",
            "Executive / CIO": "This matters if production protections are easier to bypass than leadership expects.",
            "SOC Manager": "The signal may not be malicious by itself, but it clearly deserves validation because of the potential blast radius.",
            "SRE": "A risky workload configuration in production can quickly become both a security and stability concern.",
        },
    },
    {
        "id": "crashloop_sensitive_workload",
        "title": "Sensitive Workload Entering CrashLoopBackOff After Change",
        "category": "Kubernetes Behavior",
        "environment": "Kubernetes",
        "cloud": "Multi-cloud",
        "signal": "A business-critical workload repeatedly crashes after a recent deployment or configuration update.",
        "what_it_may_indicate": "Release regression, bad secret injection, incompatible dependency change, or a security control interacting poorly with application behavior.",
        "security_risk": "The signal may reflect instability rather than attack, but it can expose weak change controls and unsafe recovery decisions.",
        "operational_impact": "Directly affects service reliability, increases on-call burden, and may create pressure for rushed rollback decisions.",
        "business_impact": "Can cause customer-facing degradation, delayed releases, and reduced trust in both platform stability and deployment hygiene.",
        "severity": "High",
        "affected_personas": ["SRE", "DevOps Lead", "Platform Engineer", "Executive / CIO"],
        "technical_actions": [
            "Compare current pod spec and config against the last known healthy version",
            "Inspect crash logs, events, and readiness or liveness probe failures",
            "Validate secret mounts, config maps, and recent image changes",
            "Check whether policy or admission changes correlate to the timing",
        ],
        "operational_actions": [
            "Determine whether rollback or isolation is the safest next move",
            "Coordinate response across app, platform, and security owners",
            "Track customer-facing impact and incident status clearly",
        ],
        "csm_angle": "Use this to show how runtime visibility supports safer operations, faster prioritization, and stronger customer confidence during production issues.",
        "persona_messages": {
            "SRE": "This is a reliability issue first, but runtime context helps identify whether the root cause is application, platform, or a control interaction.",
            "DevOps Lead": "The key is preserving delivery confidence while figuring out whether the change itself created the instability.",
            "Platform Engineer": "This matters because repeated workload failure in a shared environment can reveal a broader platform control or dependency issue.",
            "Executive / CIO": "This is important if it affects critical service continuity or reveals recurring operational weakness.",
            "Customer Success Manager": "This can be translated into value around faster diagnosis, safer rollout decisions, and better cross-team alignment.",
            "SOC Manager": "Even when it is not malicious, the right response path depends on quickly separating attack suspicion from operational regression.",
            "CISO": "This is relevant if weak change control or control drift is creating avoidable production risk.",
            "Cloud Security Engineer": "This may expose where security controls and workload behavior are not well aligned operationally.",
        },
    },

    # =====================================================
    # API SECURITY
    # =====================================================
    {
        "id": "api_token_abuse_pattern",
        "title": "API Token Used from Unusual Source Pattern",
        "category": "API Security",
        "environment": "Public API",
        "cloud": "AWS",
        "signal": "An API token is making requests from new geographies, unknown IP ranges, or request patterns inconsistent with its baseline.",
        "what_it_may_indicate": "Credential leakage, automation abuse, partner misuse, scripted access, or an exposed token being replayed externally.",
        "security_risk": "A valid credential may be in the wrong hands, which makes the activity harder to distinguish from legitimate use.",
        "operational_impact": "Requires quick validation because response may affect customers, integrations, or revenue-generating workflows.",
        "business_impact": "Can lead to unauthorized access, partner friction, customer trust issues, and pressure on support and security teams.",
        "severity": "High",
        "affected_personas": ["SOC Manager", "Cloud Security Engineer", "Customer Success Manager", "Executive / CIO"],
        "technical_actions": [
            "Review request history for the token across IP, geography, and endpoint usage",
            "Validate token scope, age, and associated account owner",
            "Check for rate anomalies, error patterns, and access to sensitive endpoints",
            "Assess whether token rotation or scope reduction is required",
        ],
        "operational_actions": [
            "Coordinate with API owners and customer-facing teams before disruptive action",
            "Decide whether the event warrants incident handling or controlled customer outreach",
            "Track whether the pattern affects one identity or a broader access model",
        ],
        "csm_angle": "This supports conversations around secure adoption, token hygiene, and how customers operationalize API access safely at scale.",
        "persona_messages": {
            "SOC Manager": "This is valuable because it may be a higher-confidence misuse signal tied to a real credential rather than generic scanning noise.",
            "Cloud Security Engineer": "The priority is deciding whether this is identity abuse, poor token governance, or partner workflow drift.",
            "Customer Success Manager": "This can be translated into customer value around safer API adoption and stronger operational practices.",
            "Executive / CIO": "This matters if valid access paths are easier to abuse than the organization assumes.",
            "DevOps Lead": "The concern is protecting integrations without overreacting in a way that breaks engineering or customer workflows.",
            "SRE": "This becomes an operational problem if mitigation affects critical services or increases production instability.",
            "CISO": "A live credential used outside expected boundaries is much more material than a theoretical exposure finding.",
            "Platform Engineer": "The broader question is whether platform controls and identity governance are strong enough to contain this pattern.",
        },
    },
    {
        "id": "sensitive_api_enumeration",
        "title": "High-Volume Enumeration Against Sensitive API Endpoints",
        "category": "API Security",
        "environment": "Customer-Facing API",
        "cloud": "Azure",
        "signal": "Repeated requests target authentication, user lookup, or object retrieval endpoints in a way that suggests probing or enumeration.",
        "what_it_may_indicate": "Reconnaissance, scripted abuse, broken object level authorization testing, or adversary-driven discovery of accessible records.",
        "security_risk": "Can precede data exposure, account abuse, or exploitation of authorization weaknesses.",
        "operational_impact": "Security and engineering teams may need to tighten controls without harming legitimate customer traffic.",
        "business_impact": "Increases risk of exposure events, customer trust loss, and urgent executive attention if sensitive data access is possible.",
        "severity": "Critical",
        "affected_personas": ["SOC Manager", "CISO", "DevOps Lead", "Executive / CIO"],
        "technical_actions": [
            "Inspect endpoint patterns, status codes, and object access sequence",
            "Validate rate limiting, WAF rules, and authz enforcement around targeted APIs",
            "Determine whether the activity maps to a known client, test job, or malicious automation",
            "Assess whether sensitive records were actually accessed or only probed",
        ],
        "operational_actions": [
            "Align engineering, security, and customer-facing stakeholders on containment options",
            "Decide what customer or leadership communication is needed based on confirmed impact",
            "Track whether the behavior is isolated to one tenant or broadly distributed",
        ],
        "csm_angle": "Use this to discuss value around API visibility, prioritization, and helping customers move from reactive concern to operational response maturity.",
        "persona_messages": {
            "CISO": "This is material because probing against sensitive APIs may be an early indicator of a path toward exposure or abuse.",
            "SOC Manager": "This is worth prioritizing when the request pattern is coherent enough to suggest intent, not just random internet noise.",
            "DevOps Lead": "The challenge is raising protections without creating unnecessary friction for valid API consumers.",
            "Executive / CIO": "This matters if customer-facing access paths appear easier to enumerate than expected.",
            "Customer Success Manager": "This is a good scenario for tying product value to real risk prioritization and customer operating model improvement.",
            "SRE": "If containment is too aggressive, it can become a service stability issue, so the response path needs precision.",
            "Cloud Security Engineer": "This should map directly to authz coverage, API hardening, and whether runtime evidence confirms exploitability.",
            "Platform Engineer": "The broader concern is whether shared API protections are consistently enforced across services.",
        },
    },

    # =====================================================
    # IDENTITY / ACCESS
    # =====================================================
    {
        "id": "iam_role_assumption_spike",
        "title": "Unexpected IAM Role Assumption from New Execution Path",
        "category": "Identity / Access",
        "environment": "Cloud IAM",
        "cloud": "AWS",
        "signal": "A sensitive IAM role is being assumed by a workload, user, or automation path that is new or inconsistent with prior behavior.",
        "what_it_may_indicate": "Privilege misuse, stolen credentials, automation drift, mis-scoped permissions, or compromised workload identity.",
        "security_risk": "Identity misuse increases the risk of lateral movement, sensitive access, and difficult-to-detect malicious behavior.",
        "operational_impact": "Requires rapid investigation because response may affect automation, production workflows, and downstream service access.",
        "business_impact": "Raises concern about privileged access control, audit readiness, and the organization’s ability to contain sensitive actions.",
        "severity": "Critical",
        "affected_personas": ["Cloud Security Engineer", "CISO", "SOC Manager", "Executive / CIO"],
        "technical_actions": [
            "Review role assumption logs, source identity, and session context",
            "Validate whether trust policy and permission scope match intended use",
            "Inspect recent infrastructure or pipeline changes tied to the new path",
            "Determine whether downstream sensitive actions occurred after assumption",
        ],
        "operational_actions": [
            "Coordinate with IAM, platform, and service owners before revoking access",
            "Assess whether the behavior is isolated or part of a wider privilege pattern",
            "Prepare leadership-ready framing if the role has material business impact",
        ],
        "csm_angle": "This helps position identity visibility and prioritization as business value, especially when customers care about privileged access and control maturity.",
        "persona_messages": {
            "Cloud Security Engineer": "This matters because runtime-aware identity signals often show where access controls are technically valid but operationally unsafe.",
            "CISO": "Unexpected privileged identity use is highly material because it can quickly escalate from suspicious access to real exposure.",
            "SOC Manager": "This is a strong escalation candidate when the role is sensitive and the source pattern is genuinely new.",
            "Executive / CIO": "This matters if privileged paths are less controlled in practice than leadership expects.",
            "Customer Success Manager": "This can be translated into value around identity prioritization, operational readiness, and control maturity.",
            "DevOps Lead": "The question is whether the access change was engineering-driven, automation-related, or truly unauthorized.",
            "SRE": "Containment decisions must balance security urgency against the risk of breaking production dependencies.",
            "Platform Engineer": "This may expose inconsistent trust relationships across shared systems and automation.",
        },
    },
    {
        "id": "service_account_overreach",
        "title": "Service Account Accessing Resources Outside Expected Scope",
        "category": "Identity / Access",
        "environment": "Kubernetes / Cloud IAM",
        "cloud": "GCP",
        "signal": "A service account is observed accessing resources or APIs outside its normal workload pattern or intended ownership boundary.",
        "what_it_may_indicate": "Overprivileged identity, workload impersonation, token misuse, or drift between intended least privilege and actual behavior.",
        "security_risk": "Can enable silent access expansion across services and make containment more complex once abuse begins.",
        "operational_impact": "Remediation may affect application behavior, platform dependencies, and automation flows that rely on the identity.",
        "business_impact": "Creates audit and exposure concerns while reducing confidence that identity boundaries are truly enforced.",
        "severity": "High",
        "affected_personas": ["Platform Engineer", "Cloud Security Engineer", "Customer Success Manager", "CISO"],
        "technical_actions": [
            "Review the service account’s permission scope and recent token use",
            "Validate whether the access path matches workload design intent",
            "Inspect cluster-to-cloud identity mappings or workload identity configuration",
            "Check whether similar overreach exists across related service accounts",
        ],
        "operational_actions": [
            "Coordinate remediation timing with application and platform owners",
            "Determine whether scope reduction can be done safely without outage risk",
            "Document whether the issue reflects one identity or a broader governance gap",
        ],
        "csm_angle": "Use this to discuss least-privilege maturity, cross-team ownership, and how customers translate identity findings into repeatable action.",
        "persona_messages": {
            "Platform Engineer": "This matters because one overprivileged service identity can undermine trust across shared platform boundaries.",
            "Cloud Security Engineer": "The main question is whether this is harmless over-permissioning or a runtime path that is already being exercised unsafely.",
            "CISO": "This is important because it highlights where the operating model says least privilege exists but the environment says otherwise.",
            "Customer Success Manager": "This is a strong value conversation around operationalizing identity hygiene, not just detecting it.",
            "Executive / CIO": "This matters if foundational access controls are broader in practice than intended.",
            "SOC Manager": "This may deserve escalation when access to sensitive resources is involved or the behavior clearly exceeds baseline.",
            "DevOps Lead": "Fixing it well means reducing access safely without disrupting delivery or service reliability.",
            "SRE": "Any identity change needs to be weighed against production dependency risk before action is taken.",
        },
    },

    # =====================================================
    # CLOUD EXPOSURE
    # =====================================================
    {
        "id": "public_storage_with_runtime_access",
        "title": "Publicly Exposed Storage Resource Accessed by Runtime Workload",
        "category": "Cloud Exposure",
        "environment": "Cloud Storage",
        "cloud": "AWS",
        "signal": "A publicly reachable storage resource is linked to active workload behavior or is being accessed by a runtime component in production.",
        "what_it_may_indicate": "Misconfigured storage exposure, weak access boundaries, unsafe artifact retrieval, or an easier path for data access than intended.",
        "security_risk": "Exposure becomes more urgent when it is not only public in theory but also actively tied to workload behavior or sensitive data paths.",
        "operational_impact": "Requires coordination across cloud, app, and platform teams because remediation can affect dependencies and production workflows.",
        "business_impact": "Increases concern around data protection, customer trust, audit posture, and how quickly teams can correct risky cloud configurations.",
        "severity": "High",
        "affected_personas": ["Cloud Security Engineer", "CISO", "Customer Success Manager", "Executive / CIO"],
        "technical_actions": [
            "Validate storage ACLs, bucket policy, and actual object exposure scope",
            "Determine whether runtime workloads depend on the exposed path",
            "Assess whether sensitive data, artifacts, or configs are accessible",
            "Review access logging for unusual reads or external interaction",
        ],
        "operational_actions": [
            "Coordinate remediation with application and data owners before restricting access",
            "Decide whether this is posture debt or immediate operational risk",
            "Prepare concise leadership framing if regulated or customer-impacting data is involved",
        ],
        "csm_angle": "This supports outcome-based conversations around reducing real cloud risk, improving prioritization, and proving the platform helps teams act on the right exposures.",
        "persona_messages": {
            "Cloud Security Engineer": "This matters most when posture findings are clearly tied to live workload behavior and practical exploitability.",
            "CISO": "A public cloud exposure tied to active production use is far more material than dormant misconfiguration debt.",
            "Customer Success Manager": "This is a strong example of turning a technical issue into measurable risk reduction and workflow alignment value.",
            "Executive / CIO": "This matters if exposed cloud resources undermine confidence in data protection and operational control.",
            "SRE": "The concern is fixing the exposure without breaking the workload path that currently depends on it.",
            "DevOps Lead": "The question is whether the exposure was an intentional shortcut in delivery or a blind spot in engineering controls.",
            "SOC Manager": "This deserves prioritization if the exposure is active and there is evidence it is reachable or already being used unexpectedly.",
            "Platform Engineer": "This can reveal inconsistent cloud hygiene patterns across teams and environments.",
        },
    },
    {
        "id": "internet_exposed_admin_service",
        "title": "Administrative Service Exposed to Internet with Weak Access Path",
        "category": "Cloud Exposure",
        "environment": "Cloud Compute / Admin Interface",
        "cloud": "Azure",
        "signal": "An administrative or internal service is reachable externally and protected only by weak network or identity controls.",
        "what_it_may_indicate": "Mis-scoped security groups, temporary access changes left in place, inadequate segmentation, or risky admin convenience patterns.",
        "security_risk": "Administrative paths exposed externally create a higher-probability route for unauthorized access, abuse, or escalation.",
        "operational_impact": "Remediation must be fast but careful because the service may still support critical admin or operational workflows.",
        "business_impact": "Can trigger significant executive concern because it suggests preventable exposure of high-value control paths.",
        "severity": "Critical",
        "affected_personas": ["CISO", "Executive / CIO", "Cloud Security Engineer", "Platform Engineer"],
        "technical_actions": [
            "Validate actual external reachability and auth requirements",
            "Review firewall rules, security groups, and ingress history",
            "Determine whether the service supports sensitive administrative functions",
            "Assess whether compensating controls like MFA, VPN, or IP restrictions are in place",
        ],
        "operational_actions": [
            "Coordinate safe restriction of access with service owners immediately",
            "Determine whether the exposure was intentional, temporary, or unknown",
            "Prepare incident-style communication if business-critical administration is at risk",
        ],
        "csm_angle": "This is useful for framing risk reduction, control maturity, and why customers invest in visibility that helps prioritize dangerous exposure over background noise.",
        "persona_messages": {
            "CISO": "This is material because exposed admin paths tend to combine high value with preventable control weakness.",
            "Executive / CIO": "This matters because it directly challenges assumptions about how well critical systems are protected.",
            "Cloud Security Engineer": "This should map quickly to segmentation, identity protection, and whether access design is aligned to intended use.",
            "Platform Engineer": "The concern is closing the gap safely without breaking operational access or emergency workflows.",
            "Customer Success Manager": "This can be translated into customer value around prioritizing what actually matters and operationalizing remediation faster.",
            "SOC Manager": "This may merit escalation even before malicious activity is seen because the exposure itself is highly consequential.",
            "DevOps Lead": "The question is whether delivery or admin convenience created a risky path that now needs a safer workflow replacement.",
            "SRE": "Any containment must preserve essential service operations while reducing the exposed attack surface quickly.",
        },
    },

    # =====================================================
    # DEVOPS / CI-CD CONTEXT
    # =====================================================
    {
        "id": "pipeline_secret_exposure",
        "title": "Pipeline Job Exposes Sensitive Secret in Build Context",
        "category": "DevOps / CI-CD Context",
        "environment": "CI/CD Pipeline",
        "cloud": "GitHub Actions / Multi-cloud",
        "signal": "A build or deployment job surfaces a secret in logs, environment variables, artifact paths, or an insecure step configuration.",
        "what_it_may_indicate": "Unsafe secret handling, poor pipeline hygiene, accidental leakage, or an engineering workflow that creates reusable exposure paths.",
        "security_risk": "Leaked build secrets can enable unauthorized access to registries, cloud resources, or downstream deployment systems.",
        "operational_impact": "Requires coordinated remediation because secret rotation, pipeline changes, and release timing all matter.",
        "business_impact": "Can delay releases, weaken trust in delivery controls, and increase concern around software supply chain resilience.",
        "severity": "High",
        "affected_personas": ["DevOps Lead", "Cloud Security Engineer", "CISO", "Customer Success Manager"],
        "technical_actions": [
            "Identify where the secret was exposed and whether it was persisted",
            "Rotate affected credentials and validate downstream blast radius",
            "Review pipeline steps, masking controls, and artifact retention behavior",
            "Determine whether similar secret handling patterns exist elsewhere",
        ],
        "operational_actions": [
            "Coordinate rotation with engineering and platform owners to avoid breaking releases",
            "Decide whether delivery should pause until exposure risk is reduced",
            "Document the workflow gap and ownership for durable remediation",
        ],
        "csm_angle": "Use this to discuss secure delivery maturity, workflow alignment, and how the platform helps customers prioritize what is operationally meaningful.",
        "persona_messages": {
            "DevOps Lead": "This matters because bad secret handling in CI/CD threatens both release confidence and engineering trust in the pipeline.",
            "Cloud Security Engineer": "This should map directly to secret management maturity and where automation is bypassing safer patterns.",
            "CISO": "Pipeline secret exposure is important because it can rapidly turn into broader privileged access risk.",
            "Customer Success Manager": "This is a good value story around safer workflows, operationalization, and measurable reduction in avoidable delivery risk.",
            "Executive / CIO": "This matters if the delivery system itself is creating security debt that slows the business.",
            "SOC Manager": "The signal is stronger when the secret is real, reusable, and connected to high-value access paths.",
            "SRE": "Containment has to account for the risk of disrupting active release or recovery workflows.",
            "Platform Engineer": "This can reveal systemic issues in build standards and shared pipeline templates.",
        },
    },
    {
        "id": "unsigned_image_deployed",
        "title": "Unsigned or Unverified Image Promoted to Production",
        "category": "DevOps / CI-CD Context",
        "environment": "Container Supply Chain",
        "cloud": "Multi-cloud",
        "signal": "A production deployment references an image that lacks expected signature verification, provenance validation, or trusted registry assurance.",
        "what_it_may_indicate": "Supply chain control gap, workflow bypass, weak promotion controls, or insufficient enforcement of trusted artifact policies.",
        "security_risk": "Weak image trust raises the chance that unreviewed or tampered software reaches production environments.",
        "operational_impact": "Response may require balancing security assurance with release continuity and business pressure to keep deployments moving.",
        "business_impact": "Undermines confidence in software delivery governance and can amplify concern about production integrity and audit readiness.",
        "severity": "High",
        "affected_personas": ["DevOps Lead", "Platform Engineer", "CISO", "Executive / CIO"],
        "technical_actions": [
            "Validate image source, registry trust, and attestation or signature status",
            "Review promotion pipeline logs and enforcement points for policy bypass",
            "Determine whether the image differs materially from approved build artifacts",
            "Check whether similar unsigned images have reached adjacent environments",
        ],
        "operational_actions": [
            "Coordinate with engineering and release owners on whether rollback is necessary",
            "Assess whether this is a one-off exception or a repeatable workflow weakness",
            "Document control ownership and leadership-ready remediation framing",
        ],
        "csm_angle": "This is strong for conversations around secure software delivery, operational trust, and expanding adoption into supply chain and policy workflows.",
        "persona_messages": {
            "DevOps Lead": "This matters because release speed loses value if production trust in the artifact path starts to erode.",
            "Platform Engineer": "The concern is whether the platform is actually enforcing trusted promotion rules consistently.",
            "CISO": "This is material because it shows where software assurance policy may exist on paper but fail in production reality.",
            "Executive / CIO": "This matters if the organization cannot confidently prove what software is running in production.",
            "Customer Success Manager": "This can be translated into value around safer delivery, workflow maturity, and stronger operational trust.",
            "Cloud Security Engineer": "This should map to artifact trust, registry governance, and runtime implications of weak build integrity.",
            "SOC Manager": "This is less about immediate malicious proof and more about a serious control weakness that deserves prioritization.",
            "SRE": "Any response needs to weigh the integrity concern against the operational impact of rollback or deployment interruption.",
        },
    },
]

# =========================================================
# HELPERS
# =========================================================
def get_scenarios_by_category(category: str) -> list[dict]:
    return [scenario for scenario in SCENARIOS if scenario["category"] == category]


def summarize_scenario(scenario: dict) -> dict:
    return {
        "title": scenario["title"],
        "category": scenario["category"],
        "environment": scenario["environment"],
        "cloud": scenario["cloud"],
        "severity": scenario["severity"],
    }


def build_value_translation(scenario: dict, persona: str) -> dict:
    technical_meaning = scenario["what_it_may_indicate"]
    security_meaning = scenario["security_risk"]
    operational_consequence = scenario["operational_impact"]
    business_outcome = scenario["business_impact"]

    value_story = (
        f"This signal shows why runtime context matters. For {persona}, the value is not just knowing "
        f"that something is exposed, but understanding that the behavior is active, meaningful, and worthy "
        f"of immediate attention."
    )

    if persona == "SRE":
        value_story = (
            "For SRE, the value is faster triage, lower on-call burden, and clearer containment decisions without losing production stability."
        )
    elif persona == "CISO":
        value_story = (
            "For the CISO, the value is moving from theoretical cloud exposure to evidence of active behavior that deserves executive prioritization."
        )
    elif persona == "DevOps Lead":
        value_story = (
            "For DevOps, the value is understanding risky runtime behavior in a way that supports safer releases and better engineering fit."
        )
    elif persona == "Customer Success Manager":
        value_story = (
            "For Customer Success, the value is turning a runtime event into a customer outcome conversation around adoption, workflow alignment, and measurable platform value."
        )
    elif persona == "SOC Manager":
        value_story = (
            "For the SOC Manager, the value is sharper prioritization, better escalation quality, and less wasted analyst effort on lower-signal findings."
        )
    elif persona == "Cloud Security Engineer":
        value_story = (
            "For Cloud Security, the value is connecting runtime evidence to the exact control gap, identity issue, or posture weakness that needs to be fixed."
        )
    elif persona == "Platform Engineer":
        value_story = (
            "For Platform Engineering, the value is seeing whether the issue is isolated or reflects a broader enforcement and environment trust problem."
        )
    elif persona == "Executive / CIO":
        value_story = (
            "For leadership, the value is understanding whether this issue affects continuity, operational resilience, and confidence in security investments."
        )

    return {
        "technical_meaning": technical_meaning,
        "security_meaning": security_meaning,
        "operational_consequence": operational_consequence,
        "business_outcome": business_outcome,
        "value_story": value_story,
    }


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
        "Tie this scenario to success criteria around runtime visibility, incident readiness, cross-team workflow alignment, and measurable reduction in time-to-prioritize or time-to-contain."
    )

    qbr_talking_point = (
        "Highlight how runtime context helps the customer focus on real risk, reduce false urgency around lower-value findings, and improve alignment between security, SRE, DevOps, and leadership."
    )

    expansion_signal = (
        "If this scenario reveals gaps in API visibility, identity prioritization, workload protection, or cross-team operationalization, it may indicate room to expand adoption into adjacent platform capabilities."
    )

    return {
        "immediate_next_steps": immediate_next_steps,
        "customer_questions": customer_questions,
        "success_plan_tie_in": success_plan_tie_in,
        "qbr_talking_point": qbr_talking_point,
        "expansion_signal": expansion_signal,
    }


def build_persona_view(scenario: dict, persona_name: str) -> dict:
    persona = PERSONAS[persona_name]
    scenario_message = scenario["persona_messages"].get(
        persona_name,
        "This runtime signal matters because it affects visibility, prioritization, and coordinated response."
    )

    first_priority_map = {
        "CISO": "Confirm materiality, blast radius, and whether immediate executive awareness is needed.",
        "SOC Manager": "Validate signal confidence and decide whether to escalate or continue triage.",
        "Cloud Security Engineer": "Map the behavior to the missing or failed cloud control first.",
        "DevOps Lead": "Check whether this correlates to a recent release, pipeline change, or engineering action.",
        "SRE": "Determine whether production stability is currently at risk and what containment causes the least disruption.",
        "Platform Engineer": "Assess whether the issue is isolated to one workload or reflects a broader platform weakness.",
        "Customer Success Manager": "Translate the issue into an adoption, value, and stakeholder-alignment conversation.",
        "Executive / CIO": "Understand whether continuity, customer trust, or business resilience is meaningfully impacted.",
    }

    return {
        "focus": ", ".join([item.title() for item in persona["focus"]]),
        "cares_about": persona["cares_about"],
        "questions": persona["questions"],
        "primary_concern": persona["priority"],
        "team_interpretation": persona["team_view"],
        "first_priority": first_priority_map.get(
            persona_name,
            "Prioritize the most important stakeholder-relevant risk first."
        ),
        "message_framing": persona["message_style"],
        "persona_message": scenario_message,
    }


def render_card(
    title: str,
    body: str,
    border_class: str = "border-run",
    min_height: int | None = None,
):
    min_height_style = f"min-height:{min_height}px;" if min_height else ""
    st.markdown(
        f"""
        <div class="card {border_class}" style="{min_height_style}">
            <div class="card-title">{title}</div>
            <div class="body-text">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_list_card(
    title: str,
    items: list[str],
    border_class: str = "border-run",
    min_height: int | None = None,
):
    min_height_style = f"min-height:{min_height}px;" if min_height else ""
    body = "".join([f"<li>{item}</li>" for item in items])
    st.markdown(
        f"""
        <div class="card {border_class}" style="{min_height_style}">
            <div class="card-title">{title}</div>
            <div class="body-text">
                <ul>{body}</ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def severity_class(level: str) -> str:
    mapping = {
        "Low": "sev-low",
        "Medium": "sev-medium",
        "High": "sev-high",
        "Critical": "sev-critical",
    }
    return mapping.get(level, "sev-medium")


def get_valid_scenario(selected_title: str, scenarios: list[dict]) -> dict | None:
    if not scenarios:
        return None

    match = next((item for item in scenarios if item["title"] == selected_title), None)
    if match:
        return match

    return scenarios[0]


# =========================================================
# STYLES
# =========================================================
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    div[data-testid="stAppViewContainer"] > .main {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }

    section.main > div {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }

    :root {
        --bg: #f4f4f4;
        --text: #202020;
        --muted: #5e5e66;
        --blue: #6ea8ff;
        --purple: #c48bf2;
        --coral: #ff8f7a;
        --mint: #87d7c4;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1320px;
        padding-top: 0rem !important;
        padding-bottom: 2rem;
        margin-top: 0rem !important;
    }

    [data-testid="stSidebar"] {
        background: #efefef;
        border-right: 1px solid rgba(0,0,0,0.05);
    }

    [data-testid="stSidebar"] * {
        color: #202020 !important;
    }

    .hero {
        background: transparent;
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 24px;
        padding: 1.4rem 1.5rem;
        margin-top: 0rem !important;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }

    .hero:before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 24px;
        padding: 1px;
        background: linear-gradient(90deg, var(--blue), var(--purple), var(--coral));
        -webkit-mask:
          linear-gradient(#fff 0 0) content-box,
          linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
                mask-composite: exclude;
        pointer-events: none;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: #212121;
        margin-bottom: 0.15rem;
        text-align: center;
    }

    .hero-sub {
        font-size: 0.98rem;
        line-height: 1.55;
        color: #4d4d55;
        text-align: center;
        max-width: 760px;
        margin: 0 auto;
    }

    .metric-box {
        background: rgba(255,255,255,0.24);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.8rem;
        min-height: 92px;
    }

    .metric-label {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #6a6a74;
        margin-bottom: 0.22rem;
        font-weight: 700;
    }

    .metric-value {
        font-size: 1rem;
        font-weight: 600;
        color: #202020;
    }

    .card {
        background: rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 1rem 1rem 0.95rem 1rem;
        margin-bottom: 1rem;
        height: 100%;
        box-sizing: border-box;
    }

    .card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #202020;
        margin-bottom: 0.55rem;
    }

    .body-text {
        font-size: 0.97rem;
        color: #2e2e33;
        line-height: 1.6;
    }

    .stack-section {
        margin-bottom: 0.9rem;
    }

    .stack-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.28rem;
    }

    .stack-build { color: var(--blue); }
    .stack-run { color: var(--purple); }
    .stack-protect { color: var(--coral); }
    .stack-mint { color: var(--mint); }

    .border-build {
        border: 1px solid rgba(110, 168, 255, 0.55);
    }

    .border-run {
        border: 1px solid rgba(196, 139, 242, 0.55);
    }

    .border-protect {
        border: 1px solid rgba(255, 143, 122, 0.55);
    }

    .scenario-focus-card {
        position: relative;
        border-radius: 24px;
        padding: 1.2rem 1.25rem 1.1rem 1.25rem;
        margin-bottom: 1rem;
        background: rgba(255,255,255,0.12);
        overflow: hidden;
    }

    .scenario-focus-card:before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 24px;
        padding: 1.4px;
        background: linear-gradient(90deg, var(--blue), var(--purple), var(--coral));
        -webkit-mask:
          linear-gradient(#fff 0 0) content-box,
          linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
                mask-composite: exclude;
        pointer-events: none;
    }

    .scenario-eyebrow {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        color: var(--purple);
        margin-bottom: 0.4rem;
    }

    .scenario-title {
        font-size: 1.55rem;
        line-height: 1.23;
        font-weight: 700;
        color: #202020;
        margin-bottom: 0.9rem;
    }

    .security-risk-inline {
        border-top: 1px solid rgba(0,0,0,0.06);
        padding-top: 0.75rem;
    }

    .section-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.1rem;
        margin-bottom: 0.35rem;
    }

    .heading-build { color: var(--blue); }
    .heading-run { color: var(--purple); }
    .heading-protect { color: var(--coral); }
    .heading-mint { color: var(--mint); }

    .pill {
        display: inline-block;
        padding: 0.34rem 0.66rem;
        border-radius: 999px;
        margin: 0.18rem 0.28rem 0.1rem 0;
        font-size: 0.76rem;
        font-weight: 600;
        background: rgba(255,255,255,0.48);
        border: 1px solid rgba(0,0,0,0.08);
        color: #2b2b31;
    }

    .sev-low,
    .sev-medium,
    .sev-high,
    .sev-critical {
        background: rgba(255,255,255,0.48);
        font-weight: 700;
    }

    .sev-low {
        border: 1px solid rgba(135, 215, 196, 0.85);
        color: #2b7564;
    }

    .sev-medium {
        border: 1px solid rgba(196, 139, 242, 0.85);
        color: #7d49a7;
    }

    .sev-high {
        border: 1px solid rgba(255, 143, 122, 0.85);
        color: #b95945;
    }

    .sev-critical {
        border: 1px solid rgba(110, 168, 255, 0.85);
        color: #4475c9;
    }

    .context-wrap {
        background: rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 0.85rem 1rem 0.7rem 1rem;
        margin-bottom: 1rem;
    }

    .context-wrap.build {
        border: 1px solid rgba(110, 168, 255, 0.48);
    }

    .context-wrap.run {
        border: 1px solid rgba(196, 139, 242, 0.48);
    }

    .context-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }

    .context-label.build { color: var(--blue); }
    .context-label.run { color: var(--purple); }

    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.65) !important;
        border: 1px solid rgba(0,0,0,0.10) !important;
        border-radius: 12px !important;
        color: #202020 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        margin-top: 0.2rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.28);
        border-radius: 12px;
        padding: 0.58rem 0.98rem;
        color: #000000 !important;
        border: 1px solid rgba(0,0,0,0.05);
        font-weight: 700 !important;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(255,255,255,0.62) !important;
        border: 1px solid rgba(196, 139, 242, 0.45) !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }

    ul {
        margin-top: 0.25rem;
        padding-left: 1.2rem;
    }

    li {
        margin-bottom: 0.35rem;
        color: #2f2f35;
    }

    .stMarkdown p {
        color: #2f2f35;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Runtime Signal Translator")
st.sidebar.caption("Cloud runtime risk → operational meaning → business value")

category = st.sidebar.selectbox(
    "Category",
    CATEGORY_ORDER,
    index=0,
)

category_scenarios = get_scenarios_by_category(category)

if not category_scenarios:
    st.sidebar.warning("No scenarios found for this category.")
    st.stop()

scenario_titles = [item["title"] for item in category_scenarios]

selected_title = st.sidebar.selectbox(
    "Scenario",
    scenario_titles,
    key="runtime_scenario_select",
)

selected_scenario = get_valid_scenario(selected_title, category_scenarios)

if selected_scenario is None:
    st.error("No valid scenario could be loaded.")
    st.stop()

persona_names = list(PERSONAS.keys())
default_persona_index = persona_names.index("SRE") if "SRE" in persona_names else 0

# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Runtime Signal Translator</div>
        <div class="hero-sub">
            Translate runtime cloud signals into technical meaning, security risk, operational impact,
            executive value, and customer success follow-up.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SUMMARY
# =========================================================
summary = summarize_scenario(selected_scenario)
sev_class = severity_class(summary["severity"])

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Severity</div>
            <div class="metric-value"><span class="pill {sev_class}">{summary["severity"]}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Environment</div>
            <div class="metric-value">{summary["environment"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_c:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Cloud</div>
            <div class="metric-value">{summary["cloud"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_d:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Category</div>
            <div class="metric-value">{summary["category"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["Scenario Explorer", "Persona Lens", "Value Translation", "CSM Action Plan"]
)

with tab1:
    st.markdown(
        f"""
        <div class="scenario-focus-card">
            <div class="scenario-eyebrow">Focused Scenario</div>
            <div class="scenario-title">{selected_scenario["title"]}</div>
            <div class="security-risk-inline">
                <div class="section-label heading-protect">Security Risk</div>
                <div class="body-text">{selected_scenario["security_risk"]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        render_card(
            "Runtime Signal",
            selected_scenario["signal"],
            "border-build",
            min_height=190,
        )
    with row1_col2:
        render_card(
            "What It May Indicate",
            selected_scenario["what_it_may_indicate"],
            "border-run",
            min_height=190,
        )

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        render_list_card(
            "Technical Actions",
            selected_scenario["technical_actions"],
            "border-build",
            min_height=260,
        )
    with row2_col2:
        render_list_card(
            "Operational Actions",
            selected_scenario["operational_actions"],
            "border-run",
            min_height=260,
        )

    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        render_card(
            "Business Impact",
            selected_scenario["business_impact"],
            "border-protect",
            min_height=180,
        )
    with row3_col2:
        render_card(
            "Operational Impact",
            selected_scenario["operational_impact"],
            "border-run",
            min_height=180,
        )

with tab2:
    st.markdown(
        """
        <div class="context-wrap run">
            <div class="context-label run">Persona Context</div>
        """,
        unsafe_allow_html=True,
    )
    selected_persona = st.selectbox(
        "Persona Context",
        persona_names,
        index=default_persona_index,
        label_visibility="collapsed",
        key="persona_tab_select",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    persona_view = build_persona_view(selected_scenario, selected_persona)

    combined_top = f"""
    <div class="stack-section">
        <div class="stack-label stack-run">Persona Focus</div>
        <div>{persona_view["focus"]}</div>
    </div>
    <div class="stack-section">
        <div class="stack-label stack-build">What This Persona Cares About</div>
        <div>{persona_view["cares_about"]}</div>
    </div>
    <div class="stack-section">
        <div class="stack-label stack-protect">Primary Concern</div>
        <div>{persona_view["primary_concern"]}</div>
    </div>
    """
    render_card("Persona Overview", combined_top, "border-run")

    combined_middle = f"""
    <div class="stack-section">
        <div class="stack-label stack-build">Team Interpretation</div>
        <div>{persona_view["team_interpretation"]}</div>
    </div>
    <div class="stack-section">
        <div class="stack-label stack-mint">What They Prioritize First</div>
        <div>{persona_view["first_priority"]}</div>
    </div>
    """
    render_card("Team Context", combined_middle, "border-build")

    render_card("Suggested Message Framing", persona_view["message_framing"], "border-protect")
    render_list_card("Questions They Might Ask", persona_view["questions"], "border-run")
    render_card(f"How to Explain This to a {selected_persona}", persona_view["persona_message"], "border-build")

with tab3:
    st.markdown(
        """
        <div class="context-wrap build">
            <div class="context-label build">Value Translation Context</div>
        """,
        unsafe_allow_html=True,
    )
    selected_persona_for_value = st.selectbox(
        "Value Translation Context",
        persona_names,
        index=default_persona_index,
        label_visibility="collapsed",
        key="value_translation_select",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    translation = build_value_translation(selected_scenario, selected_persona_for_value)

    c1, c2 = st.columns(2)
    with c1:
        render_card(
            "Technical Meaning",
            translation["technical_meaning"],
            "border-build",
            min_height=200,
        )
        render_card(
            "Security Meaning",
            translation["security_meaning"],
            "border-run",
            min_height=210,
        )
    with c2:
        render_card(
            "Operational Consequence",
            translation["operational_consequence"],
            "border-run",
            min_height=200,
        )
        render_card(
            "Business Outcome",
            translation["business_outcome"],
            "border-protect",
            min_height=210,
        )

    render_card("Value Story", translation["value_story"], "border-build")

with tab4:
    recommendations = build_recommendations(selected_scenario)

    top_left, top_right = st.columns(2)
    with top_left:
        render_list_card(
            "Immediate Next Steps",
            recommendations["immediate_next_steps"],
            "border-build",
            min_height=260,
        )
    with top_right:
        render_list_card(
            "Customer Follow-Up Questions",
            recommendations["customer_questions"],
            "border-run",
            min_height=260,
        )

    mid_left, mid_right = st.columns(2)
    with mid_left:
        render_card(
            "Success Plan Tie-In",
            recommendations["success_plan_tie_in"],
            "border-run",
            min_height=160,
        )
    with mid_right:
        render_card(
            "QBR Talking Point",
            recommendations["qbr_talking_point"],
            "border-protect",
            min_height=160,
        )

    bot_left, bot_right = st.columns(2)
    with bot_left:
        render_card(
            "Expansion Signal",
            recommendations["expansion_signal"],
            "border-build",
            min_height=160,
        )
    with bot_right:
        render_card(
            "CSM Angle",
            selected_scenario["csm_angle"],
            "border-protect",
            min_height=160,
        )
