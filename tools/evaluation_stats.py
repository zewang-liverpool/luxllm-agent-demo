"""Dependency-free statistics for reproducible LuxLLM-Agent evaluations."""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> Tuple[float, float]:
    """Return a two-sided 95% Wilson score interval for a binomial rate."""
    if total <= 0:
        return (0.0, 0.0)
    p = successes / total
    denominator = 1.0 + (z * z / total)
    centre = (p + z * z / (2.0 * total)) / denominator
    margin = z * math.sqrt((p * (1.0 - p) / total) + (z * z / (4.0 * total * total))) / denominator
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def exact_binomial_pvalue(successes: int, total: int) -> float:
    """Two-sided exact binomial p-value against p=0.5."""
    if total <= 0:
        return 1.0
    tail = min(successes, total - successes)
    lower_probability = sum(math.comb(total, k) for k in range(tail + 1)) / (2**total)
    return min(1.0, 2.0 * lower_probability)


def outcome_score(record: Dict) -> float:
    if record.get("llm_won") is True:
        return 1.0
    if record.get("winner") == "draw":
        return 0.5
    return 0.0


def bootstrap_role_difference(
    pairs: Sequence[Tuple[float, float]],
    iterations: int = 10000,
    seed: int = 42,
) -> Tuple[float, float, float]:
    """Bootstrap player_0 minus player_1 LLM outcome score by matched seed."""
    if not pairs:
        return (0.0, 0.0, 0.0)
    differences = [left - right for left, right in pairs]
    estimate = sum(differences) / len(differences)
    rng = random.Random(seed)
    samples: List[float] = []
    for _ in range(iterations):
        sample = [differences[rng.randrange(len(differences))] for _ in differences]
        samples.append(sum(sample) / len(sample))
    samples.sort()
    low_index = int(0.025 * (len(samples) - 1))
    high_index = int(0.975 * (len(samples) - 1))
    return (estimate, samples[low_index], samples[high_index])


def bootstrap_clustered_win_rate(
    pairs: Sequence[Tuple[float, float]],
    iterations: int = 10000,
    seed: int = 42,
) -> Tuple[float, float, float]:
    """Bootstrap the overall win rate while resampling matched seeds as clusters."""
    if not pairs:
        return (0.0, 0.0, 0.0)
    seed_rates = [(left + right) / 2.0 for left, right in pairs]
    estimate = sum(seed_rates) / len(seed_rates)
    rng = random.Random(seed)
    samples: List[float] = []
    for _ in range(iterations):
        sample = [seed_rates[rng.randrange(len(seed_rates))] for _ in seed_rates]
        samples.append(sum(sample) / len(sample))
    samples.sort()
    low_index = int(0.025 * (len(samples) - 1))
    high_index = int(0.975 * (len(samples) - 1))
    return (estimate, samples[low_index], samples[high_index])


def summarise_records(records: Iterable[Dict]) -> Dict:
    records = list(records)
    valid = [record for record in records if record.get("status") == "complete"]
    winner_counts = Counter(record.get("winner", "unknown") for record in valid)
    llm_wins = sum(record.get("llm_won") is True for record in valid)
    llm_losses = sum(record.get("llm_won") is False for record in valid if record.get("winner") != "draw")
    draws = sum(record.get("winner") == "draw" for record in valid)
    ci_low, ci_high = wilson_interval(llm_wins, len(valid))

    role_records = defaultdict(list)
    seed_records = defaultdict(dict)
    for record in valid:
        role = str(record.get("llm_player", "unknown"))
        role_records[role].append(record)
        seed_records[int(record["seed"])][role] = record

    by_role = {}
    for role, items in sorted(role_records.items()):
        wins = sum(item.get("llm_won") is True for item in items)
        low, high = wilson_interval(wins, len(items))
        by_role[role] = {
            "matches": len(items),
            "wins": wins,
            "losses": sum(item.get("llm_won") is False for item in items if item.get("winner") != "draw"),
            "draws": sum(item.get("winner") == "draw" for item in items),
            "win_rate": wins / len(items) if items else 0.0,
            "win_rate_wilson_95_ci": [low, high],
        }

    matched_pairs = []
    discordant_player_0_only = 0
    discordant_player_1_only = 0
    for seed, roles in sorted(seed_records.items()):
        if "player_0" not in roles or "player_1" not in roles:
            continue
        player_0_score = outcome_score(roles["player_0"])
        player_1_score = outcome_score(roles["player_1"])
        matched_pairs.append((player_0_score, player_1_score))
        player_0_win = roles["player_0"].get("llm_won") is True
        player_1_win = roles["player_1"].get("llm_won") is True
        if player_0_win and not player_1_win:
            discordant_player_0_only += 1
        elif player_1_win and not player_0_win:
            discordant_player_1_only += 1

    discordant_total = discordant_player_0_only + discordant_player_1_only
    role_diff, role_diff_low, role_diff_high = bootstrap_role_difference(matched_pairs)
    clustered_rate, clustered_low, clustered_high = bootstrap_clustered_win_rate(matched_pairs)
    seed_rates = [(left + right) / 2.0 for left, right in matched_pairs]
    seeds_above_half = sum(rate > 0.5 for rate in seed_rates)
    seeds_equal_half = sum(rate == 0.5 for rate in seed_rates)
    seeds_below_half = sum(rate < 0.5 for rate in seed_rates)
    non_tied_seed_total = seeds_above_half + seeds_below_half

    return {
        "total_records": len(records),
        "completed_matches": len(valid),
        "paired_seeds_completed": len(matched_pairs),
        "winner_counts": dict(winner_counts),
        "llm_wins": llm_wins,
        "llm_losses": llm_losses,
        "draws": draws,
        "llm_win_rate": llm_wins / len(valid) if valid else 0.0,
        "llm_win_rate_wilson_95_ci": [ci_low, ci_high],
        "exact_binomial_pvalue_vs_0_5": exact_binomial_pvalue(llm_wins, len(valid)),
        "by_llm_role": by_role,
        "matched_seed_performance": {
            "seeds_above_0_5": seeds_above_half,
            "seeds_equal_0_5": seeds_equal_half,
            "seeds_below_0_5": seeds_below_half,
            "clustered_win_rate": clustered_rate,
            "cluster_bootstrap_95_ci": [clustered_low, clustered_high],
            "exact_sign_pvalue_vs_0_5": exact_binomial_pvalue(
                seeds_above_half, non_tied_seed_total
            ),
            "bootstrap_iterations": 10000,
            "bootstrap_seed": 42,
            "independence_unit": "matched Lux environment seed",
        },
        "matched_role_analysis": {
            "player_0_only_wins": discordant_player_0_only,
            "player_1_only_wins": discordant_player_1_only,
            "mcnemar_exact_pvalue": exact_binomial_pvalue(discordant_player_0_only, discordant_total),
            "mean_outcome_score_difference_player_0_minus_player_1": role_diff,
            "paired_bootstrap_95_ci": [role_diff_low, role_diff_high],
            "bootstrap_iterations": 10000,
            "bootstrap_seed": 42,
        },
    }
