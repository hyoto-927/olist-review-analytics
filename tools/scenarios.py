"""Worked examples of the Part 2 formulas with fictional inputs in BRL."""


def exposure_reduction(orders):
    """Each tuple contains seller GMV, initial probability, scenario probability."""
    return sum(gmv * (before - after) for gmv, before, after in orders)


def next_tier_gmv(current_gmv, current_peer_mean, next_peer_mean):
    """Peer groups belong to the same category and adjacent rating tiers."""
    if current_peer_mean <= 0:
        raise ValueError("The current peer mean must be positive")
    return current_gmv * next_peer_mean / current_peer_mean


if __name__ == "__main__":
    print("Illustrative inputs (BRL)")
    print(f"B | Exposure reduction: {exposure_reduction([(100, .40, .25)]):.2f}")
    print(f"A | Next-tier scenario: {next_tier_gmv(1000, 500, 600):.2f}")
