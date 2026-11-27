import random
import unittest

from src.executor_service import arolla_service, executor_i


class TestHitChance(unittest.TestCase):
    def test_even_bonuses_give_sixty_percent(self):
        self.assertAlmostEqual(executor_i(0, 0), 0.6)

    def test_chance_is_capped_at_ninety_five_percent(self):
        self.assertEqual(executor_i(1000, 0), 0.95)

    def test_chance_is_floored_at_five_percent(self):
        self.assertEqual(executor_i(0, 1000), 0.05)


class TestDamage(unittest.TestCase):
    def test_miss_deals_zero_and_hit_is_a_die_plus_bonuses(self):
        rng = random.Random(4)
        rolls = [arolla_service(rng, 0, 0) for _ in range(200)]
        self.assertIn(0, rolls)
        self.assertTrue(any(1 <= roll <= 6 for roll in rolls))
        self.assertTrue(all(roll == 0 or 1 <= roll <= 6 for roll in rolls))

    def test_huge_attack_bonus_almost_always_hits_hard(self):
        rng = random.Random(4)
        rolls = [arolla_service(rng, 1000, 0) for _ in range(200)]
        self.assertTrue(all(roll == 0 or 1001 <= roll <= 1006 for roll in rolls))
        self.assertTrue(any(roll > 0 for roll in rolls))

    def test_same_seed_gives_same_rolls(self):
        first = [arolla_service(random.Random(9), 3, 1) for _ in range(10)]
        second = [arolla_service(random.Random(9), 3, 1) for _ in range(10)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
