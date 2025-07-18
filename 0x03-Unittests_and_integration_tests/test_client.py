#!/usr/bin/env python3
"""GitHub API client."""

from utils import get_json, memoize


class GithubOrgClient:
    """Client for GitHub organization operations."""

    def __init__(self, org_name: str):
        self.org_name = org_name

    @memoize
    def org(self):
        """Get organization details."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self):
        """Get the URL to the public repositories of the organization."""
        return self.org.get("repos_url")
