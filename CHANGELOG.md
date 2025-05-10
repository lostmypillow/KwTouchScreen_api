# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Undocumented changes

## [0.2.0] - 2025-03-03


- Migrate to website format for Chrome Kiosk Mode consumption
- Added retries for video player
- Added transitions for image loading
- Improved numpad size
- Improved Survey Page Layout
- Improved dashboard


## [0.2.1] - 2025-03-10
- added infinite retries

## [0.2.2] - 2025-03-12

- Removed control from ws
- Fixed seats page center aligned (changed to left align)
- increased status font size
- added video player stall detection
- added video player console logs (it's still the weakest link here)
- added randomized websocket connection params

## [0.2.3] - 2025-03-12
- rollback 0.2.2 video player changes

## [0.2.4] - 2025-03-12
- Increased font size to 4xl

## [0.2.5] - 2025-03-12
- Increased font size even more

## [0.2.6] - 2025-04-11

### Added
- `CHANGELOG.md` for changelog
- sync_version.py to sync `package.json` version number to FastAPI constructor in `/backend/src/main.py`
- Echo version number in `run.sh`

### Changed
- Moved `run.sh` to root
- Updated NPM packages to patch axios security vulnerability
- Bumped `package.json` version
- Fixed Survey Page bug

### Removed
- Unnecessary Docker files in `/backend` folder
- Unnecessary `/backend/.vscode` folder
- `.env` and `config.py` files

## Undocumented [0.3.x]

## [0.4.2] - 2025-05-10

### Added
- `CHANGELOG.md` for changelog
- sync_version.py to sync `package.json` version number to FastAPI constructor in `/backend/src/main.py`
- Echo version number in `run.sh`

### Changed
- Moved `run.sh` to root
- Updated NPM packages to patch axios security vulnerability
- Bumped `package.json` version
- Fixed Survey Page bug

### Removed
- Unnecessary Docker files in `/backend` folder
- Unnecessary `/backend/.vscode` folder
- `.env` and `config.py` files



