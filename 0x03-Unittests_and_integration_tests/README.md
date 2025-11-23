

# 0x03. Unittests and Integration Tests

## Project Overview

This project focuses on writing **unit tests** and **integration tests** for Python modules using `unittest`, `unittest.mock`, and `parameterized`. The project emphasizes:

* Mocking external HTTP requests
* Parameterizing tests
* Testing memoization and properties
* Using fixtures for integration tests

The modules tested include `utils` and `client` (specifically `GithubOrgClient`).

---

## Requirements

* Python 3.7
* Ubuntu 18.04 LTS
* `pycodestyle` v2.5 for style compliance
* All files must be executable and start with:

  ```bash
  #!/usr/bin/env python3
  ```
* All modules, classes, and functions are documented
* Type annotations for all functions and coroutines

---

## Project Structure

```
0x03-Unittests_and_integration_tests/
├── client.py
├── fixtures.py
├── test_client.py
├── test_utils.py
├── utils.py
└── README.md
```

---

## Testing Overview

### Unit Tests

**1. `utils.access_nested_map`**

* Parameterized to test multiple nested dictionaries.
* Validates correct retrieval of nested values.

**2. `utils.get_json`**

* Uses `unittest.mock.patch` to mock HTTP requests.
* Ensures correct JSON payload is returned.
* Confirms the mocked `get_json` is called exactly once.

**3. `utils.memoize`**

* Tests that a memoized method is called only once.
* Uses `unittest.mock.patch` to verify call counts.

**4. `client.GithubOrgClient`**

* `org` property: Mocked to test proper API URL handling.
* `_public_repos_url` property: Mocked with `PropertyMock`.
* `public_repos` method: Tested both for full list and license filtering.
* `has_license` method: Parameterized to verify license matching logic.

---

### Integration Tests

* Use fixtures (`fixtures.py`) to simulate real API responses.
* Patch only `requests.get` to avoid real HTTP calls.
* Tests include:

  * `public_repos()` → full repository list
  * `public_repos(license_key="apache-2.0")` → filtered repository list

---

## How to Run Tests

1. Install dependencies:

```bash
pip install parameterized
```

2. Run unit tests:

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

All tests are designed to run without making external HTTP requests.

---

## Code Style

* `pycodestyle` v2.5 is used.
* All files end with a newline.
* Modules, classes, and functions are documented with descriptive sentences.

---

## Author

**Your Name**
Backend Python Developer
[GitHub](https://github.com/yourusername)

---

If you want, I can also create a **shorter, more beginner-friendly version** suitable for submitting in your ALX repository.

Do you want me to do that?
