"""Experimental Poisson probabilities — original JF SOLUCIONES research code.
This module is NOT a calibrated betting recommendation system.
No private keys, client data, or bookmaker prices.
"""
from math import exp, factorial, isfinite

MODEL_VERSION = "JF_POISSON_EXPERIMENTAL_0.1"


def score_matrix(mu_home: float, mu_away: float, cap: int = 13):
    """Independent goal-count baseline. Fit rates separately with pre-kickoff data."""
    if not all(isfinite(x) and 0.15 <= x <= 4.5 for x in (mu_home, mu_away)):
        raise ValueError("invalid_goal_rates")
    hp = [exp(-mu_home) * mu_home**i / factorial(i) for i in range(cap + 1)]
    ap = [exp(-mu_away) * mu_away**j / factorial(j) for j in range(cap + 1)]
    raw = [(i, j, h*a) for i, h in enumerate(hp) for j, a in enumerate(ap)]
    total = sum(p for _, _, p in raw)
    return [(i, j, p/total) for i, j, p in raw]


def research_markets(mu_home: float, mu_away: float):
    cells = score_matrix(mu_home, mu_away)
    return {
        "home_win": sum(p for h, a, p in cells if h>a),
        "draw": sum(p for h, a, p in cells if h==a),
        "away_win": sum(p for h, a, p in cells if h<a),
        "both_score_yes": sum(p for h, a, p in cells if h>=1 and a>=1),
        "both_score_no": sum(p for h, a, p in cells if h==0 or a==0),
        "over_1_5": sum(p for h, a, p in cells if h+a>=2),
        "under_1_5": sum(p for h, a, p in cells if h+a<=1),
    }


def research_triples(legs):
    """Three distinct fixtures; joint probability withheld pending dependence tests."""
    if len(legs) != 3 or len(set(x["fixture_id"] for x in legs)) != 3:
        raise ValueError("exactly_three_distinct_fixtures_required")
    return {"legs": legs, "status": "DEPENDENCE_REVIEW_REQUIRED",
            "joint_probability": None, "recommended_bet": False}
