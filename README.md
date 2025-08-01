# Glicko

[![PyPI](https://img.shields.io/pypi/v/glicko.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/glicko.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/glicko)][pypi status]
[![License](https://img.shields.io/pypi/l/glicko)][license]

[![Documentation](https://github.com/arnesor/glicko/actions/workflows/docs.yml/badge.svg)][documentation]
[![Tests](https://github.com/arnesor/glicko/actions/workflows/tests.yml/badge.svg)][tests]
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=arnesor_glicko&metric=coverage)][sonarcov]
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=arnesor_glicko&metric=alert_status)][sonarquality]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)][poetry]

[pypi status]: https://pypi.org/project/glicko/
[documentation]: https://arnesor.github.io/glicko
[tests]: https://github.com/arnesor/glicko/actions?workflow=Tests

[sonarcov]: https://sonarcloud.io/summary/overall?id=arnesor_glicko
[sonarquality]: https://sonarcloud.io/summary/overall?id=arnesor_glicko
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[poetry]: https://python-poetry.org/

This library implements the Glicko rating system as described in
[this paper](https://www.glicko.net/glicko/glicko.pdf).

## Features

- TODO

## Requirements

- TODO

## Installation

You can install _Glicko_ via [pip] from [PyPI]:

```console
pip install glicko
```

## Usage

Please see the [Reference Guide] for API details.

The example directory contains two examples showing how to use the library:
One with soccer results, and one with table tennis results.

### File format
The results should be stored in a csv file and contain the required columns:
`HomeTeam`, `AwayTeam`, and `Result`. Optional columns: `Date`and `Round`.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Glicko_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [Statistics Norway]'s [SSB PyPI Template].

[statistics norway]: https://www.ssb.no/en
[pypi]: https://pypi.org/
[ssb pypi template]: https://github.com/statisticsnorway/ssb-pypitemplate
[file an issue]: https://github.com/arnesor/glicko/issues
[pip]: https://pip.pypa.io/


<!-- github-only -->

[license]: https://github.com/arnesor/glicko/blob/main/LICENSE
[contributor guide]: https://github.com/arnesor/glicko/blob/main/CONTRIBUTING.md
[reference guide]: https://arnesor.github.io/glicko/reference.html
