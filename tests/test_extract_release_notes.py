import unittest

from scripts.extract_release_notes import extract_release_notes_from_text


SAMPLE_CHANGELOG = """# Changelog

## [Unreleased]

### Added

- Upcoming countdown improvements.

## [v.1.0.1] - 2026-01-29

### Added

- Multi-key support.

## [v.1.0] - 2026-01-21

### Added

- Initial release.
"""


class ExtractReleaseNotesTests(unittest.TestCase):
    def test_extracts_matching_version_section(self):
        notes = extract_release_notes_from_text("v.1.0.1", SAMPLE_CHANGELOG)

        self.assertIn("## [v.1.0.1] - 2026-01-29", notes)
        self.assertIn("- Multi-key support.", notes)
        self.assertNotIn("Upcoming countdown improvements", notes)

    def test_normalizes_version_tokens(self):
        notes = extract_release_notes_from_text("v1.0.1", SAMPLE_CHANGELOG)

        self.assertIn("## [v.1.0.1] - 2026-01-29", notes)

    def test_falls_back_to_unreleased_when_tag_section_is_missing(self):
        notes = extract_release_notes_from_text("v.1.0.2", SAMPLE_CHANGELOG)

        self.assertIn("## [v.1.0.2]", notes)
        self.assertIn("- Upcoming countdown improvements.", notes)


if __name__ == "__main__":
    unittest.main()
