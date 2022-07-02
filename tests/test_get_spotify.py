import os
import unittest
from unittest import mock

import spotipy

_MOCK_ENVVARS = {
    'NEW_ALBUMS_PLAYLIST_ID': 'MockID',
    'SPOTIFY_CLIENT_ID': 'MockSpotifyID',
    'SPOTIFY_CLIENT_SECRET': 'MockSpotifySecret',
    'SPOTIFY_REDIRECT_URI': 'MockRedirectURI',
    'SPOTIFY_USER': 'TestMcTesterson'
}

class TestSpotify(unittest.TestCase):

    def setUp(self) -> None:

        mock_os = mock.patch.object(os, 'remove')
        mock_spotipy = mock.patch.object(spotipy, 'Spotify')
        # Mock Enviornment Variables
        mock.patch.dict(os.environ, _MOCK_ENVVARS).start()
        
        self.mock_remove = mock_os.start()
        self.mock_spotify = mock_spotipy.start()

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @mock.patch.object(spotipy.util, 'prompt_for_user_token')
    def testFailedCache(self, mock_prompt):
        from services.get_spotify import get_spotify

        mock_prompt.side_effect = [AttributeError, 'TestToken']
        self.mock_spotify.return_value = spotipy.client.Spotify
        ret = get_spotify()

        self.assertEqual(mock_prompt.call_count, 2)
        self.assertIsNotNone(ret)
    
    @mock.patch.object(spotipy.util, 'prompt_for_user_token')
    def testRaiseValueError(self, mock_prompt):
        from services.get_spotify import get_spotify
        
        mock_prompt.return_value = None

        with self.assertRaises(ValueError) as ctx:
            get_spotify()
        self.assertEqual(mock_prompt.call_count, 1)

if __name__ == '__main__':
    unittest.main()
