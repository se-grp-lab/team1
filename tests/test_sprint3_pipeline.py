"""Tests for Sprint 3: CI/CD Pipeline Automation, Summaries, and Quality Gate Verification.

Validates that automated reporting, JUnit parsing, Cobertura coverage parsing,
and GitHub Step Summary generation function reliably.
"""

import unittest
import tempfile
import os
from scripts.generate_ci_summary import (
    parse_junit_xml,
    parse_coverage_xml,
    generate_markdown_summary,
)


class TestSprint3CIPipeline(unittest.TestCase):
    """Verifies CI/CD pipeline automation and summary reporting."""

    def test_parse_junit_valid_xml(self):
        sample_junit = """<?xml version="1.0" encoding="utf-8"?>
<testsuite name="pytest" tests="79" failures="0" errors="0" skipped="0" time="1.64">
    <testcase classname="test_audio" name="test_vad" time="0.05" />
</testsuite>
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".xml") as f:
            f.write(sample_junit)
            path = f.name
        try:
            res = parse_junit_xml(path)
            self.assertEqual(res["tests"], 79)
            self.assertEqual(res["failures"], 0)
            self.assertEqual(res["errors"], 0)
            self.assertAlmostEqual(res["time"], 1.64, places=2)
        finally:
            os.remove(path)

    def test_parse_coverage_valid_xml(self):
        sample_cov = """<?xml version="1.0" ?>
<coverage version="7.0" line-rate="0.865" branch-rate="0.820">
    <packages />
</coverage>
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".xml") as f:
            f.write(sample_cov)
            path = f.name
        try:
            res = parse_coverage_xml(path)
            self.assertEqual(res["line_rate"], 86.5)
            self.assertEqual(res["branch_rate"], 82.0)
        finally:
            os.remove(path)

    def test_generate_markdown_summary_contains_key_sections(self):
        summary = generate_markdown_summary("/nonexistent/junit.xml", "/nonexistent/cov.xml")
        self.assertIn("VAMC CI/CD Pipeline Summary (Sprint 3)", summary)
        self.assertIn("Build & Automated Test Execution", summary)
        self.assertIn("Code & Branch Coverage Quality Gate", summary)
        self.assertIn("Latency Budget Verification", summary)
        self.assertIn("Security & Privacy Validation", summary)

    def test_quality_gate_threshold_logic(self):
        # Statement coverage must be >= 80%
        res = parse_coverage_xml("docs/reports/coverage.xml")
        self.assertGreaterEqual(res["line_rate"], 80.0, "Quality gate violated: Line coverage below 80%")
        self.assertGreaterEqual(res["branch_rate"], 80.0, "Quality gate violated: Branch coverage below 80%")


if __name__ == "__main__":
    unittest.main()
