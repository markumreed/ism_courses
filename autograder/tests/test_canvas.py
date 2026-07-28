import pytest

from autograder_common.canvas import CanvasClient, CanvasError


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text="", content=b""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.content = content

    def json(self):
        return self._json_data


class FakeSession:
    def __init__(self):
        self.headers = {}
        self.get_calls = []
        self.put_calls = []
        self.get_responses = {}
        self.put_response = FakeResponse(200, json_data={"id": 1})

    def get(self, url, params=None):
        self.get_calls.append((url, params))
        for prefix, response in self.get_responses.items():
            if url.startswith(prefix):
                return response
        raise AssertionError(f"no fake response registered for GET {url}")

    def put(self, url, json=None):
        self.put_calls.append((url, json))
        return self.put_response


def make_client():
    session = FakeSession()
    client = CanvasClient("https://example.instructure.com", 10, "tok", session=session)
    return client, session


def test_find_assignment_id_matches_by_name():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        200, json_data=[{"id": 55, "name": "Lab 3: Product Pricer"}, {"id": 56, "name": "Lab 4"}]
    )

    assert client.find_assignment_id("Lab 3: Product Pricer") == 55


def test_find_assignment_id_no_match_raises():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        200, json_data=[{"id": 56, "name": "Lab 4"}]
    )

    with pytest.raises(CanvasError, match="No assignment named"):
        client.find_assignment_id("Lab 3: Product Pricer")


def test_find_assignment_id_multiple_matches_raises():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        200, json_data=[{"id": 55, "name": "Lab 3"}, {"id": 99, "name": "Lab 3"}]
    )

    with pytest.raises(CanvasError, match="Multiple assignments"):
        client.find_assignment_id("Lab 3")


def test_list_submissions_returns_json():
    client, session = make_client()
    session.get_responses[
        "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions"
    ] = FakeResponse(200, json_data=[{"user_id": 1, "user": {"name": "Jane Doe"}}])

    result = client.list_submissions(55)

    assert result == [{"user_id": 1, "user": {"name": "Jane Doe"}}]


def test_get_current_grade_returns_score():
    client, session = make_client()
    session.get_responses[
        "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions/1"
    ] = FakeResponse(200, json_data={"score": 8.5})

    assert client.get_current_grade(55, 1) == 8.5


def test_get_current_grade_none_when_ungraded():
    client, session = make_client()
    session.get_responses[
        "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions/1"
    ] = FakeResponse(200, json_data={"score": None})

    assert client.get_current_grade(55, 1) is None


def test_post_grade_sends_put_with_score_and_comment():
    client, session = make_client()

    client.post_grade(55, 1, 9, comment="Nice work")

    assert len(session.put_calls) == 1
    url, payload = session.put_calls[0]
    assert url == "https://example.instructure.com/api/v1/courses/10/assignments/55/submissions/1"
    assert payload["submission"]["posted_grade"] == 9
    assert payload["comment"]["text_comment"] == "Nice work"


def test_post_grade_failure_raises():
    client, session = make_client()
    session.put_response = FakeResponse(422, text="validation error")

    with pytest.raises(CanvasError, match="422"):
        client.post_grade(55, 1, 9)


def test_get_failure_raises():
    client, session = make_client()
    session.get_responses["https://example.instructure.com/api/v1/courses/10/assignments"] = FakeResponse(
        403, text="forbidden"
    )

    with pytest.raises(CanvasError, match="403"):
        client.find_assignment_id("Lab 3")


def test_download_attachment_writes_content(tmp_path):
    client, session = make_client()
    session.get_responses["https://files.example.com/pricer.py"] = FakeResponse(
        200, content=b"print('hello')"
    )
    dest = tmp_path / "pricer.py"

    client.download_attachment({"url": "https://files.example.com/pricer.py"}, dest)

    assert dest.read_bytes() == b"print('hello')"


def test_download_attachment_failure_raises(tmp_path):
    client, session = make_client()
    session.get_responses["https://files.example.com/pricer.py"] = FakeResponse(404, text="not found")

    with pytest.raises(CanvasError, match="404"):
        client.download_attachment(
            {"url": "https://files.example.com/pricer.py"}, tmp_path / "pricer.py"
        )
