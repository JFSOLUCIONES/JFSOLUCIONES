"""Laboratorio sintético y aislado: comparar modelos sin cuotas ni datos reales."""

from __future__ import annotations

import json
from math import isfinite, log

from penaltyblog.models import DixonColesGoalModel, PoissonGoalsModel


def generate_synthetic_matches() -> list[tuple[str, str, int, int]]:
    """Fixtures ficticios deterministas para probar la API de modelos."""
    teams = ("Equipo A", "Equipo B", "Equipo C", "Equipo D")
    matches = []
    for season in range(6):
        for home_index, home in enumerate(teams):
            for away_index, away in enumerate(teams):
                if home == away:
                    continue
                gh = (home_index + 2 * away_index + season) % 4
                ga = (2 * home_index + away_index + season) % 3
                matches.append((home, away, gh, ga))
    return matches


def outcome_index(home_goals: int, away_goals: int) -> int:
    return 0 if home_goals > away_goals else 1 if home_goals == away_goals else 2


def evaluate(model_class, training, holdout) -> dict[str, float | str]:
    model = model_class(
        [m[2] for m in training],
        [m[3] for m in training],
        [m[0] for m in training],
        [m[1] for m in training],
    )
    model.fit()
    losses = []
    briers = []
    for home, away, gh, ga in holdout:
        p = list(model.predict(home, away, max_goals=15).home_draw_away)
        if len(p) != 3 or not all(isfinite(float(x)) and 0 <= x <= 1 for x in p):
            raise ValueError("INVALID_PROBABILITIES")
        if abs(sum(p) - 1) > 1e-6:
            raise ValueError("NON_NORMALIZED_PROBABILITIES")
        target = outcome_index(gh, ga)
        losses.append(-log(max(float(p[target]), 1e-15)))
        briers.append(sum((float(v) - (j == target)) ** 2 for j, v in enumerate(p)))
    return {
        "model": model_class.__name__,
        "samples": len(holdout),
        "log_loss": round(sum(losses) / len(losses), 6),
        "multiclass_brier": round(sum(briers) / len(briers), 6),
    }


def main() -> None:
    fixtures = generate_synthetic_matches()
    training, holdout = fixtures[:60], fixtures[60:]
    if not training or not holdout:
        raise ValueError("INVALID_SPLIT")
    results = [
        evaluate(PoissonGoalsModel, training, holdout),
        evaluate(DixonColesGoalModel, training, holdout),
    ]
    print(
        json.dumps(
            {
                "experiment": "JF_SPORTS_EDGE_OSS_API_SMOKE",
                "source": "SYNTHETIC_ONLY_NO_REAL_MATCHES",
                "data_leakage": "train_60_holdout_12_deterministic",
                "production_deploy": False,
                "betting_recommendations": False,
                "results": results,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
