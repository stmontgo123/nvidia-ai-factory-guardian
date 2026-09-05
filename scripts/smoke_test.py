"""Command-line smoke test for all synthetic scenarios."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent import analyze
from simulator import FactorySimulator


def main() -> None:
    sim = FactorySimulator()
    for scenario in sim.scenarios:
        state = sim.state(scenario)
        result = analyze(state)
        print("=" * 78)
        print(scenario)
        print(f"SLO risk: {state.sla_risk.value}")
        print(f"Cause: {result.probable_cause}")
        for rec in result.recommendations:
            print(
                f"- {rec.title} | risk={rec.risk.value} | "
                f"approval={rec.requires_approval}"
            )


if __name__ == "__main__":
    main()
