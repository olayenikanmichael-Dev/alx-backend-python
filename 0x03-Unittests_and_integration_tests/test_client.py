#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload"""
        payload = {"org": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org property"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/testorg/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list and mocks are called"""
        payload = [
            {"name": "Repo1"},
            {"name": "Repo2"},
            {"name": "Repo3"}
        ]
        mock_get_json.return_value = payload

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"
            client = GithubOrgClient("testorg")
            result = client.public_repos()
            self.assertEqual(result, ["Repo1", "Repo2", "Repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns True or False as expected"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return example payloads from fixtures"""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url.endswith("/repos"):
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: cls.org_payload)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns all expected repos"""
        client = GithubOrgClient("example_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos returns filtered repos by license"""
        client = GithubOrgClient("example_org")
        self.assertEqual(client.public_repos(license_key="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
