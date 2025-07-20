#!/usr/bin/env python3
"""
Unittests for client module.

This module contains unit tests for:
- GithubOrgClient.org
- GithubOrgClient.public_repos
- GithubOrgClient.has_license
- GithubOrgClient._public_repos_url

It also contains an integration test suite for public_repos().
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for methods of GithubOrgClient.
    """

    @parameterized.expand([
        ("google", {
            'login': 'google',
            'id': 1342004,
            'node_id': 'MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=',
            'url': 'https://api.github.com/orgs/google',
            'repos_url': 'https://api.github.com/orgs/google/repos',
            'events_url': 'https://api.github.com/orgs/google/events',
            'hooks_url': 'https://api.github.com/orgs/google/hooks',
            'issues_url': 'https://api.github.com/orgs/google/issues',
            'members_url': (
                'https://api.github.com/orgs/google/members{/member}'
            ),
            'public_members_url': (
                'https://api.github.com/orgs/google/public_members{/member}'
            ),
            'avatar_url': (
                'https://avatars.githubusercontent.com/u/1342004?v=4'
            ),
            'description': 'Google ❤️ Open Source',
            'name': 'Google',
            'company': None,
            'blog': 'https://opensource.google/',
            'location': 'United States of America',
            'email': 'opensource@google.com',
            'twitter_username': 'GoogleOSS',
            'is_verified': True,
            'has_organization_projects': True,
            'has_repository_projects': True,
            'public_repos': 2782,
            'public_gists': 0,
            'followers': 57327,
            'following': 0,
            'html_url': 'https://github.com/google',
            'created_at': '2012-01-18T01:30:18Z',
            'updated_at': '2025-06-28T19:58:20Z',
            'archived_at': None,
            'type': 'Organization'
        }),
        ("abc", {
            'message': 'Not Found',
            'documentation_url': (
                'https://docs.github.com/rest/orgs/orgs#get-an-organization'
            ),
            'status': '404'
        }),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that org() returns correct payload for given org_name.
        """
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @parameterized.expand([
        ("google", ["repo1", "repo2"])
    ])
    def test_public_repos(self, org_name, expected_repos, mock_get_json):
        """
        Test that public_repos() returns list of repo names
        and calls get_json and _public_repos_url correctly.
        """
        with patch("client.get_json") as mock_get_json:
            # Mock get_json to return a payload
            mock_get_json.return_value = [
                {"name": "repo1"},
                {"name": "repo2"}
            ]

            public_repos_url = "client.GithubOrgClient._public_repos_url"
            with patch(public_repos_url, new_callable=PropertyMock) as mock_url:
                url = f"https://api.github.com/orgs/{org_name}/repos"
                mock_url.return_value = url

                client = GithubOrgClient(org_name)
                result = client.public_repos()

                self.assertEqual(result, expected_repos)
                mock_get_json.assert_called_once_with(mock_url.return_value)
                mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license() returns True when repo license matches.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), expected
        )

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google/repos")
    ])
    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, org_name, expected_repos_url, mock_org):
        """
        Test _public_repos_url property returns correct repos_url.
        """
        # Mock .org property to return dict with repos_url
        mock_org.return_value = {
            "repos_url": expected_repos_url
        }

        client = GithubOrgClient(org_name)
        result = client._public_repos_url

        self.assertEqual(result, expected_repos_url)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [TEST_PAYLOAD[0]]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.
    Only external HTTP calls are mocked. Internal logic is tested as-is.
    """

    @classmethod
    def setUpClass(cls):
        """
        Start patcher for requests.get and configure side_effects
        based on URL.
        """
        cls.get_patcher = patch("requests.get")

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

        # Create side_effect function
        def side_effect(url):
            mock_resp = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop the requests.get patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos returns repos with license apache-2.0"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )
