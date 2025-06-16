import os
import json
import sys
import pytest

# Ensure the project root is on the import path so tests can find the module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from roi_analyzer import load_specs, compute_roi, rank_channels


def test_load_specs():
    path = os.path.join(os.path.dirname(__file__), 'channel_specs.json')
    specs = load_specs(path)
    assert isinstance(specs, list)
    assert len(specs) == 3
    assert specs[0]['channel'] == 'A'


def test_compute_roi():
    spec = {'channel': 'X', 'cost': 100, 'revenue': 250}
    roi = compute_roi(spec)
    assert roi == pytest.approx(1.5)

    zero_cost = {'channel': 'Free', 'cost': 0, 'revenue': 10}
    assert compute_roi(zero_cost) == float('inf')


def test_rank_channels():
    path = os.path.join(os.path.dirname(__file__), 'channel_specs.json')
    specs = load_specs(path)
    ranked = rank_channels(specs)
    # Expect channel C with highest ROI, then A, then B
    assert [c['channel'] for c in ranked] == ['C', 'A', 'B']
    # Each item should include computed ROI
    assert 'roi' in ranked[0]

