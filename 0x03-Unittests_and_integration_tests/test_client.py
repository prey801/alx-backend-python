#!/usr/bin/env python3
"""Test suite for client.py"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class with parameterized_class"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),
            Mock(json=Mock(return_value=cls.repos_payload))
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test all repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtered repos"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

if __name__ == "__main__":
    unittest.main()
