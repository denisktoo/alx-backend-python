import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, Mock


class TestGithubOrgClient(unittest.TestCase):
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
            'members_url': 'https://api.github.com/orgs/google/members{/member}',
            'public_members_url': 'https://api.github.com/orgs/google/public_members{/member}',
            'avatar_url': 'https://avatars.githubusercontent.com/u/1342004?v=4',
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
            'documentation_url': 'https://docs.github.com/rest/orgs/orgs#get-an-organization',
            'status': '404'
        }),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
