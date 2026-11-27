import unittest

from src.builder_dummy import business_abstract, helper_arolla, impl_common


class TestStory(unittest.TestCase):
    def test_intro_mentions_the_artefact_and_the_keys(self):
        lines = business_abstract()
        text = "\n".join(lines)
        self.assertIn("Golden Die", text)
        self.assertIn("hjkl", text)

    def test_every_depth_has_a_story_message(self):
        for depth in range(1, 6):
            self.assertTrue(helper_arolla(depth))

    def test_unknown_depth_gets_a_fallback(self):
        self.assertEqual(helper_arolla(9), "Depth 9.")

    def test_events_have_messages(self):
        for event in ("dragon", "amulet", "win", "death"):
            self.assertTrue(impl_common(event))

    def test_unknown_event_returns_empty(self):
        self.assertEqual(impl_common("bogus"), "")


if __name__ == "__main__":
    unittest.main()
