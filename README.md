<img src="images/axolpy-logo-transparent.svg" width="50%" />

# axolpy-lib, the Axolotl Library in Python
[![CodeQL](https://github.com/tchiunam/axolpy-lib/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/tchiunam/axolpy-lib/actions/workflows/codeql-analysis.yml)
[![Python](https://github.com/tchiunam/axolpy-lib/actions/workflows/python.yml/badge.svg)](https://github.com/tchiunam/axolpy-lib/actions/workflows/python.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This is the library and useful scripts of the Axolotl series in 
Python. The implementation of it aims at providing a handy all-in-one 
package for writing useful applications.

PyPi project: https://pypi.org/project/axolpy-lib

## Install axolpy-lib
```
pip install axolpy-lib
```

## Run test
To run pytest
```
pytest
```

To run test with coverage result:
```
coverage run -m pytest
```

To generate test coverage report:
```
coverage report -m
```

To generate test coverage report in html:
```
coverage html
```

## Build axolpy-lib package
To build with wheel:
```
python -m build
```

You will see output like this:
```
* Creating venv isolated environment...
* Installing packages in isolated environment... (setuptools>=42, wheel)
* Getting dependencies for sdist...
...
...
Successfully built axolpy-lib-0.0.1.tar.gz and axolpy_lib-0.0.1-py3-none-any.whl
```

---
#### See more  
1. [axolpy-cli](https://github.com/tchiunam/axolpy-cli) for using Axolpy in command line
