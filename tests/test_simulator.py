from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent import analyze
from simulator import FactorySimulator


def test_gpu_failure_has_high_risk_and_spare_capacity_elsewhere():
    sim = FactorySimulator()
    state = sim.state(FactorySimulator.GPU_FAILURE)
    assert state.sla_risk.value == "HIGH"
    assert state.clusters[0].gpu_utilization_pct > 85
    assert state.clusters[1].gpu_utilization_pct < 40


def test_gpu_failure_analysis_predicts_ttft_improvement():
    sim = FactorySimulator()
    state = sim.state(FactorySimulator.GPU_FAILURE)
    result = analyze(state)
    assert result.predicted_ttft_ms < state.weighted_ttft_ms
    assert any(r.action_id == "drain_gpu_node" for r in result.recommendations)


def test_baseline_is_low_risk():
    sim = FactorySimulator()
    state = sim.state(FactorySimulator.BASELINE)
    assert state.sla_risk.value == "LOW"
