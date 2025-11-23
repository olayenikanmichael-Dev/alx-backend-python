#!/usr/bin/env python3
"""
#!/usr/bin/env python3
Unit tests for utils.access_nested_map
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected JSON from mocked HTTP call"""
        with patch("utils.requests.get") as mock_get:
            mock_get.return_value = Mock(json=lambda: test_payload)

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)



class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list and calls methods correctly"""
        
        mock_payload = [
            {"name": "Repo1"},
            {"name": "Repo2"},
            {"name": "Repo3"},
        ]
        mock_get_json.return_value = mock_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/testorg/repos"
        ) as mock_repos_url:

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["Repo1", "Repo2", "Repo3"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct value"""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)



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
        """Set up a patcher for requests.get and mock JSON responses"""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            """Return correct fixture depending on the URL"""
            if url.endswith("/repos"):
                return cls.repos_payload
            return cls.org_payload

        mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repository names"""
        client = GithubOrgClient("example_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering of public_repos by license key"""
        client = GithubOrgClient("example_org")
        self.assertEqual(
            client.public_repos(license_key="apache-2.0"),
            self.apache2_repos
        )


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
        """Set up a patcher for requests.get and mock JSON responses"""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            """Return correct fixture depending on the URL"""
            if url.endswith("/repos"):
                return cls.repos_payload
            return cls.org_payload

        mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all expected repository names"""
        client = GithubOrgClient("example_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license key 'apache-2.0'"""
        client = GithubOrgClient("example_org")
        self.assertEqual(
            client.public_repos(license_key="apache-2.0"),
            self.apache2_repos
        )




            
if __name__ == "__main__":
    unittest.main()
