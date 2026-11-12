"""Tests for Learning Rate Scheduler."""
import unittest
from src.learning.scheduler import LearningRateScheduler

class TestLearningRateScheduler(unittest.TestCase):
    def test_initial_lr(self):
        sched = LearningRateScheduler(initial_lr=0.1)
        self.assertEqual(sched.get_lr(), 0.1)

    def test_decay_on_step(self):
        sched = LearningRateScheduler(initial_lr=0.1, decay_rate=0.9)
        sched.step()
        self.assertAlmostEqual(sched.get_lr(), 0.09)

if __name__ == '__main__':
    unittest.main()
