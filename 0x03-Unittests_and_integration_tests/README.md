# 0x03-Unittests_and_integration_tests

## Overview

This project demonstrates best practices for writing unit and integration tests in Python. It focuses on testing utility functions and a GitHub organization client, using tools such as `unittest`, `parameterized`, and `unittest.mock`.

---

## Folder Structure

- `client.py`  
  Contains the `GithubOrgClient` class, which interacts with the GitHub API to fetch organization and repository data.

- `fixtures.py`  
  Provides test payloads and fixtures used in integration tests.

- `test_client.py`  
  Unit and integration tests for `GithubOrgClient`, including tests for API calls, memoization, and repository filtering.

- `test_utils.py`  
  Unit tests for utility functions such as `access_nested_map`, `get_json`, and `memoize`.

- `utils.py`  
  Utility functions for nested map access, HTTP requests, and memoization.

---

## Key Concepts

- **Unit Testing:**  
  Isolates and tests individual functions and methods for correctness.

- **Integration Testing:**  
  Tests the interaction between components, such as API calls and data processing.

- **Mocking:**  
  Uses `unittest.mock` to simulate external dependencies (e.g., HTTP requests).

- **Parameterized Testing:**  
  Uses the `parameterized` library to run tests with multiple sets of inputs.

---

## Requirements

- Python 3.6+
- `requests`
- `parameterized`

Install dependencies with:

```sh
pip install requests parameterized
```

---

## Running Tests

To run all tests, execute:

```sh
python -m unittest discover
```

Or run individual test files:

```sh
python -m unittest test_utils.py
python -m unittest test_client.py
```

---

## Example Usage

- `GithubOrgClient` fetches organization data from GitHub and lists public repositories.
- Utility functions provide safe access to nested dictionaries and memoization for expensive operations.

