## 1. Environment

- Python 3.14.6

## 2. Install Libraries via requirements.txt

```command
$ pip install -r requirements.txt
```

## 3. Execution

```command
$ invoke run_template_creator
Provide your username(Default: hayat01sh1da)
hayat01sh1da
Provide your preferred unit d(daily - default), w(weekly) or m(monthly)
d
Provide the specific year you would like to create working report templates for(Default: the current year)
2024
```

## 4. Unit Test

```command
$ invoke
============================= test session starts ==============================
platform linux -- Python 3.14.6, pytest-9.0.3, pluggy-1.6.0
rootdir: template-creators/python
configfile: pyproject.toml
collected 8 items

test/test_application.py ........                                        [100%]

============================== 8 passed in 5.56s ===============================
```

## 5. Static Code Analysis

```command
$ flake8 .
./src/application.py:112:80: E501 line too long (82 > 79 characters)
./test/test_application.py:47:80: E501 line too long (93 > 79 characters)
./test/test_application.py:52:80: E501 line too long (83 > 79 characters)
./test/test_application.py:57:80: E501 line too long (98 > 79 characters)
./test/test_application.py:67:80: E501 line too long (97 > 79 characters)

$ autoflake8 --in-place --remove-duplicate-keys --remove-unused-variables --recursive .

$ autopep8 --in-place --aggressive --aggressive --recursive .
```

## 6. Type Checks

```command
$ mypy .
Success: no issues found in 4 source files
```
