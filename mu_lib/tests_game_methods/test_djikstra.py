from unittest import TestCase
from game_methods.djikstra import djikstra8, djikstra4

# DONE


class TestDjikstra(TestCase):

    def test_djikstra(self):
        print("START")
        array_map = [
            [1, 1, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        self.assertEqual(djikstra8((0, 0), (4, 4), array_map), [
                         (0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (4, 4)])
        self.assertEqual(djikstra4((0, 0), (4, 4), array_map), [
                         (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])
        self.assertEqual(djikstra8((0, 0), (2, 2), array_map),
                         [(0, 0), (0, 1), (1, 2), (2, 2)])
        self.assertEqual(djikstra4((0, 0), (2, 2), array_map), [
                         (0, 0), (0, 1), (0, 2), (1, 2), (2, 2)])
