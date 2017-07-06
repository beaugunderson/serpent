# Installation:

`make && sudo make install`

*Note: this is a temporary PyPi package since ethereum-serpent hasn't pushed a
new version since 2015.*

# Testing

Testing is done using `pytest` and `tox`.

```bash
$ pip install tox -r requirements-dev.txt
```


To run the test suite in your current python version:

```bash
$ py.test
```


To run the full test suite across all supported python versions:

```bash
$ tox
```
