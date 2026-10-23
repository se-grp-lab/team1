"""Tests for VAMC-F-021 (on-device adaptation) and VAMC-F-022 (DP federated sync)."""

import os
import tempfile
import unittest

import numpy as np

from src.learning.adaptation import FEATURE_DIM, AcousticAdapter
from src.learning.federated import (FederatedClient, PrivacyBudgetExceeded, aggregate,
                                    clip_update)


class TestAcousticAdapter(unittest.TestCase):
    def test_correction_applies_only_after_min_support(self):
        a = AcousticAdapter(min_support=2)
        a.observe("pause the sung", "pause the song")
        self.assertEqual(a.correct("pause the sung"), "pause the sung")
        a.observe("pause the sung", "pause the song")
        self.assertEqual(a.correct("pause the sung"), "pause the song")

    def test_unseen_text_unchanged(self):
        self.assertEqual(AcousticAdapter().correct("play"), "play")

    def test_identical_pairs_ignored(self):
        a = AcousticAdapter()
        a.observe("play", "play")
        self.assertEqual(a.stats()["pairs"], 0)

    def test_weights_move_on_observation(self):
        a = AcousticAdapter()
        a.observe("lauder", "louder")
        self.assertEqual(a.weight_vector().shape, (FEATURE_DIM,))
        self.assertGreater(float(np.linalg.norm(a.weight_vector())), 0.0)

    def test_persistence_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "adapt.json")
            a = AcousticAdapter(min_support=1, store_path=path)
            a.observe("next sung", "next song")
            b = AcousticAdapter(min_support=1, store_path=path)
            self.assertEqual(b.correct("next sung"), "next song")
            np.testing.assert_allclose(a.weight_vector(), b.weight_vector())


class TestFederatedPrivacy(unittest.TestCase):
    def test_clip_bounds_l2_norm(self):
        clipped = clip_update(np.array([3.0, 4.0]), 1.0)
        self.assertAlmostEqual(float(np.linalg.norm(clipped)), 1.0)
        small = np.array([0.1, 0.1])
        np.testing.assert_array_equal(clip_update(small, 1.0), small)

    def test_update_is_noised_and_not_raw(self):
        c = FederatedClient(seed=1)
        delta = np.full(FEATURE_DIM, 0.01)
        sent = c.prepare_update(delta)
        self.assertFalse(np.allclose(sent, delta))

    def test_noise_scales_with_multiplier(self):
        delta = np.zeros(2000)
        low = FederatedClient(noise_multiplier=0.5, epsilon_budget=1e9, seed=3).prepare_update(delta)
        high = FederatedClient(noise_multiplier=2.0, seed=3).prepare_update(delta)
        self.assertGreater(float(np.std(high)), float(np.std(low)) * 3)

    def test_noise_averages_out_across_clients(self):
        true_delta = np.full(32, 0.1)
        updates = [FederatedClient(clip_norm=1.0, noise_multiplier=0.1, epsilon_budget=1e9, seed=s).prepare_update(true_delta)
                   for s in range(500)]
        np.testing.assert_allclose(aggregate(updates), true_delta, atol=0.03)

    def test_budget_exhaustion_blocks_sync(self):
        c = FederatedClient(epsilon_budget=1.0, noise_multiplier=1.0, seed=0)
        with self.assertRaises(PrivacyBudgetExceeded):
            c.prepare_update(np.zeros(4))
        self.assertEqual(c.rounds, 0)

    def test_budget_accumulates(self):
        c = FederatedClient(seed=0)
        c.prepare_update(np.zeros(4))
        c.prepare_update(np.zeros(4))
        self.assertAlmostEqual(c.epsilon_spent, 2 * c.epsilon_per_round)

    def test_rejects_non_weight_payloads(self):
        c = FederatedClient()
        with self.assertRaises(TypeError):
            c.prepare_update(b"\x00" * 100)
        with self.assertRaises(TypeError):
            c.prepare_update(np.array([1, 2, 3]))

    def test_uploader_receives_only_private_update(self):
        got = []
        c = FederatedClient(seed=5, uploader=got.append)
        sent = c.sync(np.ones(4))
        self.assertIs(got[0], sent)


if __name__ == "__main__":
    unittest.main()
