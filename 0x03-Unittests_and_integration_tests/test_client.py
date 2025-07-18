#!/usr/bin/env python3
"""Unit tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
import parameterized
import requests
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    def test_public_repos_url(self):
        """Test the _public_repos_url property."""
        expected_url = "https://api.github.com/orgs/test-org/repos"
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("test-org")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method."""
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos_payload
        test_url = "https://api.github.com/orgs/test-org/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            return_value=test_url
        ) as mock_public_url:
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(test_url)
            mock_public_url.assert_called_once()
            # Ensure it does not call the method again
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once()
            mock_public_url.assert_called_once()

    @parameterized.parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized.parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            unittest.mock.MagicMock(
                json=lambda: cls.org_payload
            ),
            unittest.mock.MagicMock(
                json=lambda: cls.repos_payload
            ),
        ]
        cls.client = GithubOrgClient("google")

    @classmethod
    def tearDownClass(cls):
        """Tear down class fixtures."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method."""
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method with a license."""
        apache2_repos_names = [repo["name"] for repo in self.apache2_repos]
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"),
            apache2_repos_names,
        )