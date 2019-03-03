# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Changed
- Renamed deploy task in `.circleci/config.yml` to publish
### Added
- Added `--no-dev` in `.circleci/config.yml` deploy task
### Fixed
- CHANGELOG.md had 0.1.0 listed twice

## [0.1.1] - 2019-03-03
### Changed
- Went from MIT to Apache 2.0 License, to match aiohttp
- Example now uses `healthcheck_handler` instead of just `handler`
### Added
- .github directory for basic templates
- Keywords and classifiers for PyPI listing
- LICENSE file
- README.md file

## [0.1.0] - 2019-03-03
### Added
- Initial version. Includes sanic_healthchecks.start_healthchecks_server
