#!/usr/bin/env python3
# import unittest
# from unittest.mock import patch, PropertyMock, MagicMock
# from parameterized import parameterized, parameterized_class

# from client import GithubOrgClient
# from fixtures import TEST_PAYLOAD

# # task4
# class TestGithubOrgClient(unittest.TestCase):
#     """Test case for GithubOrgClient"""

#     @parameterized.expand([
#         ("google",),
#         ("abc",),
#     ])
#     @patch("client.get_json")
#     def test_org(self, org_name, mock_get_json):
#         """Test that GithubOrgClient.org returns the correct value."""
#         test_payload = {"org": org_name}
#         mock_get_json.return_value = test_payload

#         client = GithubOrgClient(org_name)
#         result = client.org

#         mock_get_json.assert_called_once_with(
#             f"https://api.github.com/orgs/{org_name}"
#         )
#         self.assertEqual(result, test_payload)


# # task5
#     def test_public_repos_url(self):
#         """Test _public_repos_url returns expected URL from org payload"""
#         test_payload = {
#             "repos_url": "https://api.github.com/orgs/test-org/repos"
#         }

#         with patch.object(
#             GithubOrgClient,
#             "org",
#             new_callable=PropertyMock,
#         ) as mock_org:
#             mock_org.return_value = test_payload

#             client = GithubOrgClient("test-org")
#             result = client._public_repos_url

#             mock_org.assert_called_once()
#             self.assertEqual(result, test_payload["repos_url"])

# # task6
#     @patch("client.get_json")
#     def test_public_repos(self, mock_get_json):
#         """Test public_repos returns the expected repo list"""
#         test_payload = [
#             {"name": "repo1"},
#             {"name": "repo2"},
#             {"name": "repo3"},
#         ]
#         mock_get_json.return_value = test_payload

#         with patch.object(
#             GithubOrgClient,
#             "_public_repos_url",
#             new_callable=PropertyMock,
#         ) as mock_repos_url:
#             mock_repos_url.return_value = (
#                 "https://api.github.com/orgs/test-org/repos"
#             )

#             client = GithubOrgClient("test-org")
#             result = client.public_repos()

#             # Assert output matches names from payload
#             self.assertEqual(result, ["repo1", "repo2", "repo3"])

#             # Assert mocks were called exactly once
#             mock_repos_url.assert_called_once()
#             mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")


# # task7
#     @parameterized.expand([
#         ({"license": {"key": "my_license"}}, "my_license", True),
#         ({"license": {"key": "other_license"}}, "my_license", False),
#     ])
#     def test_has_license(self, repo, license_key, expected):
#         """Test has_license returns expected boolean based on repo license"""
#         result = GithubOrgClient.has_license(repo, license_key)
#         self.assertEqual(result, expected)

# # task8

# @parameterized_class([
#     {
#         "org_payload": TEST_PAYLOAD[0][0],
#         "repos_payload": TEST_PAYLOAD[0][1],
#         "expected_repos": [repo["name"] for repo in TEST_PAYLOAD[0][1]],
#         "apache2_repos": [
#             repo["name"] for repo in TEST_PAYLOAD[0][1]
#             if repo.get("license", {}).get("key") == "apache-2.0"
#         ],
#     }
# ])
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration tests for GithubOrgClient.public_repos"""

#     @classmethod
#     def setUpClass(cls):
#         """Start patcher for requests.get and return fixture payloads"""
#         cls.get_patcher = patch("requests.get")
#         mock_get = cls.get_patcher.start()

#         # Configure the side effect for requests.get().json()
#         def side_effect(url):
#             mock_response = MagicMock()
#             if url == cls.org_payload["repos_url"].replace("/repos", ""):
#                 mock_response.json.return_value = cls.org_payload
#             elif url == cls.org_payload["repos_url"]:
#                 mock_response.json.return_value = cls.repos_payload
#             else:
#                 mock_response.json.return_value = {}
#             return mock_response

#         mock_get.side_effect = side_effect

#     @classmethod
#     def tearDownClass(cls):
#         """Stop patcher after tests"""
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """Test that public_repos returns the expected repo list"""
#         client = GithubOrgClient("google")
#         self.assertEqual(client.public_repos(), self.expected_repos)

#     def test_public_repos_with_license(self):
#         """Test that public_repos filters repos by license"""
#         client = GithubOrgClient("google")
#         self.assertEqual(
#             client.public_repos(license="apache-2.0"),
#             self.apache2_repos
#         )

# -------------------------------------

"""
Unit and integration tests for GithubOrgClient.

This module contains comprehensive tests for the GithubOrgClient class,
including unit tests for individual methods and integration tests that
verify the complete workflow using real fixture data.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_payload = {
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL"""
        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo list"""
        repos = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other"}},
        ]
        mock_get_json.return_value = repos
        expected_url = "https://api.github.com/orgs/google/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = expected_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(expected_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


# -------------------------------
# Integration tests
# -------------------------------
@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": [
            repo["name"] for repo in TEST_PAYLOAD[0][1]
        ],
        "apache2_repos": [
            repo["name"] for repo in TEST_PAYLOAD[0][1]
            if (repo.get("license") and
                repo["license"].get("key") == "apache-2.0")
        ],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure side_effect for different URLs
        def side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                return MockResponse(cls.org_payload)
            if url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos from fixtures"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license from fixtures"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


# Helper mock response
class MockResponse:
    """Mock response object for requests.get"""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload
