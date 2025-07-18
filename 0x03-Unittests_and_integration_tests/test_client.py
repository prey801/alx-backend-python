#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://some_url"
            client = GithubOrgClient("test_org")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos with license filtering"""
        payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://some_url"
            client = GithubOrgClient("test_org")
            self.assertEqual(
                client.public_repos(license="apache-2.0"),
                ["repo1", "repo3"]
            )


if __name__ == '__main__':
    unittest.main()
