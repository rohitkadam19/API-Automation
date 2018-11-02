# Twitter App only Auth Tests

## Prerequisites

### Python version
- 2.7.x
- pip

### Setup
- `pip install -r requirements.txt`.
- Enter twitter app consumer key and consumer secret in twitter_auth.conf
  (Above step is mandatory)

### Single Test Run
- `py.test --junitxml results.xml --html=reports/index.html -s -v tests/api/<test_file_name.py>`

### Run All Tests
- `py.test --junitxml results.xml --html=reports/index.html -s -v tests/api/`

### Reports
- For HTML reports, open `index.html` under reports directory.
- For test logs, open `twitter_auth.log`.