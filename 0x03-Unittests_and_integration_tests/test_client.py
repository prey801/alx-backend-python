#!/usr/bin/env python3
"""GithubOrgClient module."""

import requests
from utils import get_json


class GithubOrgClient:
    """Client for interacting with GitHub organization API."""

    def __init__(self, org_name: str):
        """Initialize with organization name."""
        self.org_name = org_name

    def org(self):
        """Fetch organization information from GitHub."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
