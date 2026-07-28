#!/usr/bin/env python3
"""
pega_case_client.py

Small client wrapper around the Pega Platform Constellation/DX REST API
for common case-management operations: creating cases, retrieving case
status, and adding case-level comments/attachments metadata.

This is a sample/reference client illustrating typical integration
patterns used to automate Pega case operations from external systems.
"""

import json
import urllib.request
import urllib.error


class PegaCaseClient:
    def __init__(self, base_url, access_token):
        """
        base_url: e.g. https://mypegaenv.example.com/prweb/api/v1
        access_token: OAuth2 bearer token obtained via the Pega OAuth endpoint
        """
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token

    def _request(self, method, path, body=None):
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Pega API error {exc.code}: {exc.read().decode('utf-8')}") from exc

    def create_case(self, case_type_id, content=None):
        """Create a new case of the given case type."""
        body = {"caseTypeID": case_type_id, "content": content or {}}
        return self._request("POST", "/cases", body)

    def get_case(self, case_id):
        """Retrieve the current status and details of a case."""
        return self._request("GET", f"/cases/{case_id}")

    def add_comment(self, case_id, comment_text):
        """Add a comment to an existing case."""
        body = {"message": comment_text}
        return self._request("POST", f"/cases/{case_id}/comments", body)

    def perform_action(self, case_id, action_id, content=None):
        """Perform a flow action (e.g. Approve, Reject) on a case."""
        body = {"content": content or {}}
        return self._request("POST", f"/cases/{case_id}/actions/{action_id}", body)


if __name__ == "__main__":
    # Example usage (replace with real environment values)
    client = PegaCaseClient(
        base_url="https://mypegaenv.example.com/prweb/api/v1",
        access_token="<oauth-access-token>",
    )
    new_case = client.create_case("MyOrg-MyApp-Work-ServiceRequest")
    print(f"Created case: {new_case.get('ID')}")
