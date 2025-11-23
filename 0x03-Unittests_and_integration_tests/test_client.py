#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.org method
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock



class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        test_payload = {"org": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)




class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected result based on mocked org property"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/testorg/repos")



if __name__ == "__main__":
    unittest.main()
