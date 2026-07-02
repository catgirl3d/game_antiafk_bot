# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [v.1.0.2] - 2026-07-02

### Added

- Drift-resistant countdown logic that keeps the next key press timer aligned with system time, even when the UI tick is delayed.
- A configurable cursor micro-movement range in advanced settings.

### Changed

- The countdown UI now catches up missed cycles instead of drifting behind the bot loop.
- The main settings controls were redesigned into clearer option cards with a dedicated advanced settings modal.
- Frameless window dragging now uses explicit drag regions instead of global easy drag behavior.

## [v.1.0.1] - 2026-01-29

### Added

- Multi-key support with random key selection for each action.
- Configurable minimum and maximum action intervals for more natural timing.
- Configurable minimum and maximum key press durations.
- Optional micro-movements and random mouse clicks.

### Changed

- The settings model moved from a single key and interval to a richer configuration with timing ranges and optional behaviors.
