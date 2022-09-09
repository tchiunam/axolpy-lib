<img src="images/axolpy-logo-transparent.svg" width="50%" />

# axolpy-lib, the Axolotl Library in Python
#### Release
<div align="left">
  <a href="https://github.com/tchiunam/axolpy-lib/releases">
    <img alt="Version" src="https://img.shields.io/github/v/release/tchiunam/axolpy-lib?sort=semver" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-lib/releases">
    <img alt="Release Date" src="https://img.shields.io/github/release-date/tchiunam/axolpy-lib" />
  </a>
  <a href="https://pypi.org/project/axolpy-lib/">
    <img alt="Pypi" src="https://badge.fury.io/py/axolpy-lib.svg" />
  </a>
  <img alt="Pypi Status" src="https://img.shields.io/pypi/status/axolpy-lib" />
  <img alt="Python Version" src="https://img.shields.io/pypi/pyversions/axolpy-lib" />
  <img alt="Pypi Format" src="https://img.shields.io/pypi/format/axolpy-lib" />
  <img alt="Language" src="https://img.shields.io/github/languages/count/tchiunam/axolpy-lib" />
  <img alt="Lines of Code" src="https://img.shields.io/tokei/lines/github/tchiunam/axolpy-lib" />
  <img alt="File Count" src="https://img.shields.io/github/directory-file-count/tchiunam/axolpy-lib" />
  <img alt="Repository Size" src="https://img.shields.io/github/repo-size/tchiunam/axolpy-lib.svg?label=Repo%20size" />
</div>

#### Code Quality
<div align="left">
  <a href="https://github.com/tchiunam/axolpy-lib/actions/workflows/python.yaml">
    <img alt="Python" src="https://github.com/tchiunam/axolpy-lib/actions/workflows/python.yaml/badge.svg" />
  </a>
  <a href="https://codecov.io/gh/tchiunam/axolpy-lib">
    <img alt="codecov" src="https://codecov.io/gh/tchiunam/axolpy-lib/branch/main/graph/badge.svg?token=JZTOZY5UXL" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-lib/actions/workflows/codeql-analysis.yaml">
    <img alt="CodeQL" src="https://github.com/tchiunam/axolpy-lib/actions/workflows/codeql-analysis.yaml/badge.svg" />
  </a>
</div>

#### Activity
<div align="left">
  <a href="https://github.com/tchiunam/axolpy-lib/commits/main">
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/tchiunam/axolpy-lib" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-lib/issues?q=is%3Aissue+is%3Aclosed">
    <img alt="Closed Issues" src="https://img.shields.io/github/issues-closed/tchiunam/axolpy-lib" />
  </a>
  <a href="https://github.com/tchiunam/axolpy-lib/pulls?q=is%3Apr+is%3Aclosed">
    <img alt="Closed Pull Requests" src="https://img.shields.io/github/issues-pr-closed/tchiunam/axolpy-lib" />
  </a>
</div>

#### License
<div align="left">
  <a href="https://opensource.org/licenses/MIT">
    <img alt="License: MIT" src="https://img.shields.io/github/license/tchiunam/axolpy-lib" />
  </a>
  <a href="https://app.fossa.com/projects/custom%2B32310%2Fgithub.com%2Ftchiunam%2Faxolpy-lib?ref=badge_shield">
    <img alt="FOSSA Status" src="https://app.fossa.com/api/projects/custom%2B32310%2Fgithub.com%2Ftchiunam%2Faxolpy-lib.svg?type=shield" />
  </a>
</div>

#### Popularity
<div align="left">
  <a href="https://sourcegraph.com/github.com/tchiunam/axolpy-lib?badge">
    <img alt="Sourcegraph" src="https://sourcegraph.com/github.com/tchiunam/axolpy-lib/-/badge.svg" />
  </a>
  <img alt="Repo Stars" src="https://img.shields.io/github/stars/tchiunam/axolpy-lib?style=social" />
  <img alt="Watchers" src="https://img.shields.io/github/watchers/tchiunam/axolpy-lib?style=social" />
</div>

<br />

This is the library of the Axolotl series in Python. The implementation of it
aims at providing a handy all-in-one package for writing useful applications.

PyPi project: https://pypi.org/project/axolpy-lib

## Install axolpy-lib
```console
pip install axolpy-lib
```

### Install dependencies
Since this package contains libraries for many areas, not all dependencies
are configured as hard dependency and installed together with **axolpy-lib**. Therefore
you can decide what to not install to save your space. However, if you want to use
all features or develop on top of this package, you will have to install all dependencies.
#### Recommended way
You are recommended to use [pyenv](https://github.com/pyenv/pyenv) and [pipenv](https://github.com/pypa/pipenv)
to install the dependencies. To install all dependencies:
```console
pipenv install
```

To install particlular package only:
```console
pipenv install pyyaml
```

#### Alternative
You can install dependencies with the old way by using requirements.txt.
```console
pip install -r requirements.txt
```

## Run test
To run pytest:
```console
pytest
```

To run test with coverage result:
```console
coverage run -m pytest
```

To generate test coverage report:
```console
coverage report -m
```

To generate test coverage report in html:
```console
coverage html
```

## Build axolpy-lib package
To build with wheel:
```console
python -m build
```

You will see output like this:
```console
* Creating venv isolated environment...
* Installing packages in isolated environment... (setuptools>=42, wheel)
* Getting dependencies for sdist...
...
...
Successfully built axolpy-lib-1.0.0.tar.gz and axolpy_lib-1.0.0-py3-none-any.whl
```

## Test report
## Code Coverage graph
[![Code Coverage graph](https://codecov.io/gh/tchiunam/axolpy-lib/branch/main/graphs/tree.svg?token=JZTOZY5UXL)](https://app.codecov.io/gh/tchiunam/axolpy-lib)

---
#### See more  
1. [axolpy-script](https://github.com/tchiunam/axolpy-script) for using Axolpy scripts

## License
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B32310%2Fgithub.com%2Ftchiunam%2Faxolpy-lib.svg?type=large)](https://app.fossa.com/projects/custom%2B32310%2Fgithub.com%2Ftchiunam%2Faxolpy-lib?ref=badge_large)