import pytest

from autograder_common.scoring import (
    ScoringError,
    compute_capstone_score,
    compute_points_score,
    compute_score,
)

POINTS_CONFIG = {
    "scoring_type": "points",
    "rubric": {
        "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
        "correctness": {"points": 4, "source": "human"},
        "code_quality": {"points": 2, "source": "human"},
    },
}

CAPSTONE_CONFIG = {
    "scoring_type": "capstone_levels",
    "rubric": {
        "code_clarity": {"source": "human"},
        "visualizations": {"source": "human"},
        "insight_quality": {"source": "human"},
        "communication": {"source": "human"},
    },
}


def test_compute_points_score_sums_mechanical_and_human():
    row = {
        "mech_submission": "True",
        "human_correctness": "4",
        "human_code_quality": "1",
    }

    assert compute_points_score(row, POINTS_CONFIG) == 6.0


def test_compute_points_score_mechanical_not_earned_scores_zero():
    row = {
        "mech_submission": "False",
        "human_correctness": "4",
        "human_code_quality": "2",
    }

    assert compute_points_score(row, POINTS_CONFIG) == 6.0


def test_compute_points_score_missing_human_field_raises():
    row = {"mech_submission": "True", "human_correctness": "4", "human_code_quality": ""}

    with pytest.raises(ScoringError, match="code_quality"):
        compute_points_score(row, POINTS_CONFIG)


def test_compute_points_score_human_value_out_of_range_raises():
    row = {"mech_submission": "True", "human_correctness": "40", "human_code_quality": "2"}

    with pytest.raises(ScoringError, match="outside 0..4"):
        compute_points_score(row, POINTS_CONFIG)


def test_compute_capstone_score_averages_levels_times_25():
    row = {
        "human_code_clarity": "excellent",
        "human_visualizations": "good",
        "human_insight_quality": "good",
        "human_communication": "excellent",
    }
    # levels: 4, 3, 3, 4 -> avg 3.5 -> 3.5 * 25 = 87.5
    assert compute_capstone_score(row, CAPSTONE_CONFIG) == 87.5


def test_compute_capstone_score_all_incomplete_is_25():
    row = {
        "human_code_clarity": "incomplete",
        "human_visualizations": "incomplete",
        "human_insight_quality": "incomplete",
        "human_communication": "incomplete",
    }
    assert compute_capstone_score(row, CAPSTONE_CONFIG) == 25.0


def test_compute_capstone_score_invalid_level_raises():
    row = {
        "human_code_clarity": "amazing",
        "human_visualizations": "good",
        "human_insight_quality": "good",
        "human_communication": "good",
    }
    with pytest.raises(ScoringError, match="code_clarity"):
        compute_capstone_score(row, CAPSTONE_CONFIG)


def test_compute_score_dispatches_points():
    row = {"mech_submission": "True", "human_correctness": "4", "human_code_quality": "2"}
    assert compute_score(row, POINTS_CONFIG) == 7.0


def test_compute_score_dispatches_capstone_levels():
    row = {
        "human_code_clarity": "good",
        "human_visualizations": "good",
        "human_insight_quality": "good",
        "human_communication": "good",
    }
    assert compute_score(row, CAPSTONE_CONFIG) == 75.0


def test_compute_score_defaults_to_points_when_scoring_type_absent():
    config = {"rubric": POINTS_CONFIG["rubric"]}
    row = {"mech_submission": "True", "human_correctness": "4", "human_code_quality": "2"}
    assert compute_score(row, config) == 7.0
