"""Improvement roadmap grouped by timeframe."""

from dataclasses import dataclass

from app.services.recommendations.engine import GeneratedRecommendation, PRIORITY_ORDER


ROADMAP_BUCKETS = [
    ("0-30 days", "immediate", "Immediate governance actions"),
    ("31-90 days", "short_term", "Documentation, testing, and control improvements"),
    ("3-6 months", "medium_term", "Operational governance and monitoring"),
    ("6-12 months", "long_term", "Continuous improvement and mature governance practices"),
]


@dataclass
class RoadmapPhase:
    key: str
    label: str
    description: str
    items: list[GeneratedRecommendation]


def build_roadmap(recommendations: list[GeneratedRecommendation]) -> list[RoadmapPhase]:
    phases: list[RoadmapPhase] = []
    for timeframe, key, description in ROADMAP_BUCKETS:
        items = [r for r in recommendations if r.suggested_timeframe == timeframe]
        items.sort(key=lambda r: (PRIORITY_ORDER[r.priority], r.category_name))
        if items:
            phases.append(
                RoadmapPhase(
                    key=key,
                    label=timeframe,
                    description=description,
                    items=items,
                )
            )
    return phases
