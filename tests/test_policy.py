from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import ActionRisk
from policy import evaluate_action


def test_bounded_reroute_is_auto_eligible():
    risk, approval = evaluate_action("reroute_traffic_15pct")
    assert risk == ActionRisk.LOW
    assert approval is False


def test_node_drain_requires_human_approval():
    risk, approval = evaluate_action("drain_gpu_node")
    assert risk == ActionRisk.HIGH
    assert approval is True


def test_cloud_burst_requires_approval():
    risk, approval = evaluate_action("cloud_burst")
    assert risk == ActionRisk.MEDIUM
    assert approval is True
