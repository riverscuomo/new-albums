import unittest

from build_description import build_description


class TestBuildDescription(unittest.TestCase):
    def setUp(self) -> None:
        self.artists = [{'name': 'Geezer'}]
        self.accepted_albums = [{
            'artists': self.artists,
            'name': 'The Testing Album'
        }, {
            'artists': self.artists,
            'name': 'The Second Testing Album'
        }
        ]
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def testBuildSubscription(self):
        expected = 'Geezer "The Testing Album", Geezer "The Second Testing Album"'
        actual = build_description(self.accepted_albums)

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()