#!/usr/bin/env python3
"""Module for testing GithubOrgClient."""

import unittest
import json
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Class for Testing GithubOrgClient."""

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        client_instance = GithubOrgClient(org_name)
        client_instance.org()
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected value."""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            expected_payload = {"repos_url": "World"}
            mock_org.return_value = expected_payload
            client_instance = GithubOrgClient('test')
            result = client_instance._public_repos_url
            self.assertEqual(result, expected_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""
        mock_repos = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = mock_repos

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "hello/world"
            client_instance = GithubOrgClient('test')
            result = client_instance.public_repos()

            expected_names = [repo["name"] for repo in mock_repos]
            self.assertEqual(result, expected_names)

            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo_data, license_key, expected):
        """Test the has_license method of GithubOrgClient."""
        result = GithubOrgClient.has_license(repo_data, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment before running tests."""
        config = {
            'return_value.json.side_effect': [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock_get = cls.get_patcher.start()

    def test_public_repos(self):
        """Integration test: public_repos method."""
        client_instance = GithubOrgClient("google")

        self.assertEqual(client_instance.org, self.org_payload)
        self.assertEqual(client_instance.repos_payload, self.repos_payload)
        self.assertEqual(client_instance.public_repos(), self.expected_repos)
        self.assertEqual(client_instance.public_repos("XLICENSE"), [])
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """Integration test for public_repos method with license filtering."""
        client_instance = GithubOrgClient("google")

        self.assertEqual(client_instance.public_repos(), self.expected_repos)
        self.assertEqual(client_instance.public_repos("XLICENSE"), [])
        self.assertEqual(client_instance.public_repos("apache-2.0"), self.apache2_repos)
        self.mock_get.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests in the class run."""
        cls.get_patcher.stop()
