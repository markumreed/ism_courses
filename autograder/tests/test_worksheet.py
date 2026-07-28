from autograder_common.worksheet import (
    build_worksheet,
    human_fields,
    incomplete_students,
    mechanical_fields,
    read_worksheet,
)

ASSIGNMENT_CONFIG = {
    "rubric": {
        "submission": {"points": 1, "source": "mechanical", "check": "file_present"},
        "correctness": {"points": 4, "source": "human", "prompt": "Compare output"},
        "code_quality": {"points": 2, "source": "human", "prompt": "Readable?"},
    }
}


def test_human_and_mechanical_fields_split_by_source():
    assert human_fields(ASSIGNMENT_CONFIG) == ["correctness", "code_quality"]
    assert mechanical_fields(ASSIGNMENT_CONFIG) == ["submission"]


def test_build_and_read_worksheet_round_trip(tmp_path):
    path = tmp_path / "review.csv"
    students = [
        {
            "student_key": "janedoe",
            "student_name": "Jane Doe",
            "status": "ok",
            "submission": True,
            "captured_output": "hello world",
        },
        {
            "student_key": "johnsmith",
            "student_name": "John Smith",
            "status": "fetch-failed",
        },
    ]

    build_worksheet(path, students, ASSIGNMENT_CONFIG)
    rows = read_worksheet(path)

    assert len(rows) == 2
    assert rows[0]["student_key"] == "janedoe"
    assert rows[0]["mech_submission"] == "True"
    assert rows[0]["human_correctness"] == ""
    assert rows[0]["human_code_quality"] == ""
    assert rows[0]["captured_output"] == "hello world"
    assert rows[1]["status"] == "fetch-failed"


def test_incomplete_students_flags_blank_human_fields(tmp_path):
    path = tmp_path / "review.csv"
    students = [
        {"student_key": "janedoe", "student_name": "Jane Doe", "status": "ok", "submission": True},
        {"student_key": "johnsmith", "student_name": "John Smith", "status": "ok", "submission": True},
    ]
    build_worksheet(path, students, ASSIGNMENT_CONFIG)
    rows = read_worksheet(path)
    # instructor fills in Jane's fields but not John's
    rows[0]["human_correctness"] = "4"
    rows[0]["human_code_quality"] = "2"

    result = incomplete_students(rows, ASSIGNMENT_CONFIG)

    assert result == ["johnsmith"]


def test_incomplete_students_skips_fetch_failed_rows(tmp_path):
    path = tmp_path / "review.csv"
    students = [
        {"student_key": "janedoe", "student_name": "Jane Doe", "status": "fetch-failed"},
    ]
    build_worksheet(path, students, ASSIGNMENT_CONFIG)
    rows = read_worksheet(path)

    assert incomplete_students(rows, ASSIGNMENT_CONFIG) == []
