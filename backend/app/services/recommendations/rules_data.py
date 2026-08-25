"""Recommendation rule content keyed by recommendation_key."""

from dataclasses import dataclass

from app.db.seed_data import QUESTION_SEED


@dataclass(frozen=True)
class RuleContent:
    recommendation: str
    why_it_matters: str
    suggested_action: str
    responsible_role: str


CATEGORY_ROLES: dict[str, str] = {
    "accountability": "AI Governance Lead",
    "human_oversight": "Human Oversight Manager",
    "privacy": "Privacy Officer",
    "fairness": "AI Ethics Lead",
    "transparency": "Product Owner",
    "security": "Chief Information Security Officer",
    "risk_management": "AI Risk Manager",
    "lifecycle": "MLOps Lead",
    "affected_people": "Compliance Officer",
}


# Custom rule text for high-impact controls (spec examples and critical items)
RULE_OVERRIDES: dict[str, RuleContent] = {
    "ho_human_involved": RuleContent(
        recommendation="Establish documented human-review procedures before the system is used for consequential decisions.",
        why_it_matters="Consequential AI decisions require meaningful human involvement to prevent unchecked automated harm.",
        suggested_action="Define which decisions require human review, assign reviewers, and document the review process before deployment.",
        responsible_role="Human Oversight Manager",
    ),
    "ho_override": RuleContent(
        recommendation="Implement the ability for authorized humans to override AI recommendations.",
        why_it_matters="Human override authority preserves accountability and reduces risk of harmful automated outcomes.",
        suggested_action="Build override capability into workflows, train staff on when to override, and log all overrides.",
        responsible_role="Human Oversight Manager",
    ),
    "fair_bias_testing": RuleContent(
        recommendation="Conduct documented fairness and bias testing using relevant population groups before deployment.",
        why_it_matters="Untested systems may produce discriminatory outcomes that harm individuals and expose the organization to risk.",
        suggested_action="Identify relevant demographic groups, design fairness test cases, document results, and define remediation steps.",
        responsible_role="AI Ethics Lead",
    ),
    "rm_impact_assessment": RuleContent(
        recommendation="Complete a formal AI impact assessment before deployment or expanded use.",
        why_it_matters="Impact assessments identify stakeholders, harms, and mitigation needs before the system affects people.",
        suggested_action="Conduct an AI impact assessment documenting affected parties, potential harms, and required controls.",
        responsible_role="AI Risk Manager",
    ),
    "rm_approval": RuleContent(
        recommendation="Establish a formal approval process requiring explicit authorization before consequential deployment.",
        why_it_matters="Formal approval ensures leadership visibility and accountability for high-impact AI use.",
        suggested_action="Define approval criteria, required documentation, and sign-off roles for deployment decisions.",
        responsible_role="AI Governance Lead",
    ),
    "ap_challenge": RuleContent(
        recommendation="Establish a process allowing people to challenge AI-assisted decisions.",
        why_it_matters="Affected individuals must have a meaningful path to contest outcomes influenced by AI.",
        suggested_action="Publish challenge procedures, assign review staff, and define response timelines.",
        responsible_role="Compliance Officer",
    ),
    "ap_human_review": RuleContent(
        recommendation="Enable human review of AI-influenced decisions upon request.",
        why_it_matters="Human review provides recourse when automated processes produce adverse or incorrect outcomes.",
        suggested_action="Define request procedures, assign reviewers, and document review outcomes.",
        responsible_role="Compliance Officer",
    ),
    "acc_owner": RuleContent(
        recommendation="Designate a clearly identified owner accountable for the AI system's governance.",
        why_it_matters="Without clear ownership, governance responsibilities are diffused and controls are unlikely to be maintained.",
        suggested_action="Assign a named system owner, document their responsibilities, and communicate the assignment to stakeholders.",
        responsible_role="AI Governance Lead",
    ),
    "acc_policy": RuleContent(
        recommendation="Develop and adopt an AI governance policy defining organizational expectations for responsible AI use.",
        why_it_matters="A governance policy sets the foundation for consistent, accountable AI practices across the organization.",
        suggested_action="Draft an AI governance policy covering roles, risk management, and oversight requirements; obtain leadership approval.",
        responsible_role="AI Governance Lead",
    ),
    "priv_risk_assessment": RuleContent(
        recommendation="Conduct a privacy risk assessment for the AI system and document identified risks and mitigations.",
        why_it_matters="Privacy risks in AI systems can cause regulatory, reputational, and individual harm if not identified early.",
        suggested_action="Perform a privacy impact assessment, document data flows, and define mitigation controls.",
        responsible_role="Privacy Officer",
    ),
    "sec_incident_response": RuleContent(
        recommendation="Define and test a process for responding to AI-related security incidents.",
        why_it_matters="Without incident response procedures, security events may escalate and cause extended harm.",
        suggested_action="Create an AI security incident playbook, assign roles, and conduct a tabletop exercise.",
        responsible_role="Chief Information Security Officer",
    ),
}


def _default_rule(
    key: str,
    question_text: str,
    governance_objective: str | None,
    category_code: str,
) -> RuleContent:
    objective = governance_objective or question_text.rstrip("?")
    role = CATEGORY_ROLES.get(category_code, "AI Governance Lead")
    return RuleContent(
        recommendation=f"Implement controls to achieve the following governance objective: {objective}",
        why_it_matters=f"Addressing this gap strengthens {objective.lower()} and reduces governance risk.",
        suggested_action=f"Review current practices, define required controls, assign ownership, and set a target completion date.",
        responsible_role=role,
    )


def get_rule_content(
    recommendation_key: str,
    question_text: str,
    governance_objective: str | None,
    category_code: str,
) -> RuleContent:
    if recommendation_key in RULE_OVERRIDES:
        return RULE_OVERRIDES[recommendation_key]
    return _default_rule(recommendation_key, question_text, governance_objective, category_code)


def all_recommendation_keys() -> set[str]:
    keys: set[str] = set()
    for questions in QUESTION_SEED.values():
        for q in questions:
            keys.add(q["recommendation_key"])
    return keys
