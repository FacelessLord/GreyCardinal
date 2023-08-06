import unittest

from search.collections.customizedHashSet import CustomizedHashSet


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.set = CustomizedHashSet(lambda x: x)

    def test_add_successfully(self):
        self.set.add(1)
        self.assertEqual(1, 1)

    def test_doesnt_contain_copies(self):
        self.set.add(1)
        self.set.add(1)
        self.assertEqual(1, len(self.set))

    def test_check_contains(self):
        self.set.add(1)
        self.assertIn(1, self.set)

    def test_check_not_contains(self):
        self.set.add(0)
        self.assertNotIn(1, self.set)

    def test_crashes_on_remove_on_empty_set(self):
        self.assertFalse(self.set.remove(1))

    def test_removes_item(self):
        self.set.add(1)
        self.assertTrue(self.set.remove(1))
        self.assertEqual(0, len(self.set))

    def test_counts_items(self):
        self.assertEqual(0, len(self.set))
        self.set.add(1)
        self.assertEqual(1, len(self.set))

    def test_intersection_updates(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)

        self.set.intersection_update(1, 5, 1)

        self.assertEqual(4, len(self.set))

    def test_list_mapping(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)

        lst = list(self.set)

        self.assertEqual(3, len(lst))


if __name__ == '__main__':
    unittest.main()
