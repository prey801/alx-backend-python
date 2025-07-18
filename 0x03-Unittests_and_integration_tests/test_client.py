#!/usr/bin/env python3
from unittest import TestCase
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
import client


class TestGithubOrgClient(TestCase):
    """
    Unit tests for GithubOrgClient.org method.
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct data 
        and get_json  once every call with correct URL.
        """
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org()

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)
