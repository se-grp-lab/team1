"""Tests for Privacy Budget Ledger."""
import unittest
from src.learning.ledger import PrivacyLedger

class TestPrivacyLedger(unittest.TestCase):
    def test_budget_consumption(self):
        ledger = PrivacyLedger(total_epsilon=5.0)
        self.assertTrue(ledger.record_round(1.5))
        self.assertAlmostEqual(ledger.remaining_epsilon, 3.5)

    def test_budget_exhaustion_rejected(self):
        ledger = PrivacyLedger(total_epsilon=2.0)
        self.assertTrue(ledger.record_round(1.5))
        self.assertFalse(ledger.record_round(1.0))
        self.assertAlmostEqual(ledger.remaining_epsilon, 0.5)

if __name__ == '__main__':
    unittest.main()
