"""Minimal Canvas LMS API client covering only what the autograder needs:
listing submissions, downloading files, reading the current grade, and
posting a new grade + comment."""
import requests


class CanvasError(Exception):
    pass


class CanvasClient:
    def __init__(self, base_url, course_id, token, session=None):
        self.base_url = base_url.rstrip("/")
        self.course_id = course_id
        self.token = token
        self.session = session or requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _get(self, path, params=None, url=None):
        target = url or f"{self.base_url}{path}"
        resp = self.session.get(target, params=params if url is None else None)
        if resp.status_code != 200:
            raise CanvasError(f"GET {target} failed: {resp.status_code} {resp.text[:200]}")
        return resp

    def _get_json(self, path, params=None):
        return self._get(path, params=params).json()

    def _get_all_pages(self, path, params=None):
        """GET path, following Link: rel="next" pagination until exhausted.
        Returns the concatenated JSON list across all pages."""
        results = []
        resp = self._get(path, params=params)
        results.extend(resp.json())
        next_url = resp.links.get("next", {}).get("url")
        while next_url:
            resp = self._get(path=None, url=next_url)
            results.extend(resp.json())
            next_url = resp.links.get("next", {}).get("url")
        return results

    def find_assignment_id(self, assignment_name):
        """Look up a Canvas assignment_id by exact name match within the course."""
        assignments = self._get_all_pages(
            f"/api/v1/courses/{self.course_id}/assignments", params={"per_page": 100}
        )
        matches = [a for a in assignments if a["name"] == assignment_name]
        if not matches:
            raise CanvasError(
                f"No assignment named {assignment_name!r} found in course {self.course_id}"
            )
        if len(matches) > 1:
            raise CanvasError(
                f"Multiple assignments named {assignment_name!r} found; "
                f"set canvas_assignment_id explicitly in the assignment config"
            )
        return matches[0]["id"]

    def list_submissions(self, assignment_id):
        """Return the list of submission dicts for the assignment (one per
        student), each including 'user' (name) via include[]=user."""
        return self._get_all_pages(
            f"/api/v1/courses/{self.course_id}/assignments/{assignment_id}/submissions",
            params={"per_page": 100, "include[]": "user"},
        )

    def download_attachment(self, attachment, dest_path):
        """Download a Canvas file attachment dict (must have 'url') to dest_path."""
        resp = self.session.get(attachment["url"])
        if resp.status_code != 200:
            raise CanvasError(f"Download of {attachment['url']} failed: {resp.status_code}")
        dest_path.write_bytes(resp.content)

    def get_current_grade(self, assignment_id, user_id):
        data = self._get_json(
            f"/api/v1/courses/{self.course_id}/assignments/{assignment_id}/submissions/{user_id}"
        )
        return data.get("score")

    def post_grade(self, assignment_id, user_id, score, comment=None):
        url = (
            f"{self.base_url}/api/v1/courses/{self.course_id}"
            f"/assignments/{assignment_id}/submissions/{user_id}"
        )
        payload = {"submission": {"posted_grade": score}}
        if comment:
            payload["comment"] = {"text_comment": comment}
        resp = self.session.put(url, json=payload)
        if resp.status_code != 200:
            raise CanvasError(f"PUT {url} failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()
