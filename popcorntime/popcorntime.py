#  Copyright (c) 2022.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

from typing import Optional, Union

import requests
import logging
import sys
import unittest


from urllib.parse import urljoin
from .wrapers import deprecated, beta


class PopcornTime:
    _BASE_URL: str = 'https://popcorn-time.ga/'
    _LANGUAGE: str = 'en'
    _CAM_KEYWORDS: list = [
        'CAM',
        'HDCAM',
        'TS',
        'TC'
        'TELESYNC',
        'HDTS'
    ]

    def __init__(self, debug: bool = False, language: str = 'en'):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG if debug else logging.INFO)
        self.log.addHandler(logging.StreamHandler(sys.stdout))

        self._LANGUAGE = language

    def _get(self, url: str, **kwargs) -> Optional[requests.Response.json]:
        """
            Performs a GET request to the url provided and returns the response

            :param url: str (Example: "http://popcorntime.com/shows")
            :param kwargs: dict (Example: {"headers": {"X-Requested-With": "XMLHttpRequest"}})
            :return: dict (Example: {"status": "success", "data": {"shows": []}})
        """

        req = requests.get(url, **kwargs)
        if req.status_code != 200:
            self.log.error(f'Request to {url} failed with status code {req.status_code}')
            return None
        return req.json()

    def _build_url(self, path: str) -> str:
        """
            Builds a URL from the base URL and the path

            :param path: string (Example: "/shows")
            :return: string (Example: "http://popcorntime.com/shows")
        """

        return urljoin(self._BASE_URL, path)

    @staticmethod
    def _get_torrent_seeds(torrent):
        """
            Movie have different seed name for the same thing so
            this function will handle that difference

            :param torrent:
            :return:
        """
        try:
            return torrent['seeds']
        except KeyError:
            return torrent['seed']

    """PROPERTIES START"""

    @property
    def logging_level(self):
        return self.log.getEffectiveLevel()

    @logging_level.setter
    def logging_level(self, level):
        self.log.setLevel(level)

    @property
    def base_url(self) -> str:
        return self._BASE_URL

    @base_url.setter
    def base_url(self, url: str):
        self._BASE_URL = url

    @property
    def language(self) -> str:
        return self._LANGUAGE

    @language.setter
    def language(self, language: str):
        self._LANGUAGE = language.lower()

    @property
    def cam_keywords(self) -> list:
        return self._CAM_KEYWORDS

    @cam_keywords.setter
    def cam_keywords(self, keywords: list):
        self._CAM_KEYWORDS = keywords
    """PROPERTIES END"""

    def _select_torrents_language(self, torrents: dict) -> dict:
        """
            Select the torrents language based on the language set if the language is not found
            it will revert to the first available language

            :param torrents: dict (Example: {"...": {"...": "..."}})
            :return:
        """

        torrents_language: list = list(torrents.keys())
        torrents_language: list = [language.lower() for language in torrents_language]

        """
            Some torrents may not have a selectable language so to figure this out
            we check if the "language" contains any digits cuz if it does it probably a resolution
            and not a language
        """
        if any(map(str.isdigit, torrents_language[0])):
            return torrents

        if self._LANGUAGE in torrents_language:
            return torrents[self._LANGUAGE]

        return torrents[torrents_language[0]]

    def get_server_status(self) -> Optional[requests.Response.json]:
        """
            Get the server status

            :return: dict (Example: {"repo": ..., "version": ..., "uptime": ...})
        """

        status = self._get(self._build_url('/status'))

        if status:
            self.log.info('Got status')
            return status
        return None

    """SHOWS START"""

    def get_shows_stats(self) -> Optional[requests.Response.json]:
        """
            Get the shows stats

            :return: dict (Example: {"action & adventure": {"count": 600, "title": "Action & Adventure"}})
        """

        stats = self._get(self._build_url('/shows/stat'))

        if stats:
            self.log.info('Got shows stats')
            return stats
        return None

    def get_shows_page(self, page: (int, str)) -> Optional[requests.Response.json]:
        """
            Gets the shows page

            :param page: int (Example: 1)
            :return: dict (Example: {_id: "...", ...})
        """

        shows = self._get(self._build_url(f'/shows/{page}'))

        if shows:
            self.log.info(f'Got shows page {page}')
            return shows
        return None

    def get_show(self, show_id: (int, str)) -> Optional[requests.Response.json]:
        """
            Get the show

            :param show_id: int (Example: tt1285016)
            :return: dict (Example: {"status": "success", "data": {"show": {"...show data..."}}}
        """

        show = self._get(self._build_url(f'/show/{show_id}'))

        if show:
            self.log.info(f'Got show {show_id}')
            return show
        return None

    def get_random_show(self) -> Optional[requests.Response.json]:
        """
            Get a random show

            :return: dict (Example: {"_id": "...", ...})
        """

        show = self._get(self._build_url(f'/random/show'))

        if show:
            self.log.info(f'Got random show {show["_id"]}')
            return show
        return None

    """SHOWS END"""

    """MOVIES START"""

    def get_movies_stats(self) -> Optional[requests.Response.json]:
        """
            Get the movies stats

            :return: dict (Example: {"action & adventure": {"count": 600, "title": "Action & Adventure"}})
        """

        stats = self._get(self._build_url('/movies/stat'))

        if stats:
            self.log.info('Got movies stats')
            return stats
        return None

    def get_movies_page(self, page: Union[int, str]) -> Optional[requests.Response.json]:
        """
            Gets the movies page

            :param page: int (Example: 1)
            :return: dict (Example: {_id: "...", ...})
        """

        movies = self._get(self._build_url(f'/movies/{page}'))

        if movies:
            self.log.info(f'Got movies page {page}')
            return movies
        return None

    def get_movie(self, movie_id: Union[int, str]) -> Optional[requests.Response.json]:
        """
            Get the movie

            :param movie_id: int (Example: tt1234567)
            :return: dict (Example: {_id: "...", ...})
        """

        movie = self._get(self._build_url(f'/movie/{movie_id}'))

        if movie:
            self.log.info(f'Got movie {movie_id}')
            return movie
        return None

    def get_random_movie(self) -> Optional[requests.Response.json]:
        """
            Gets a random movie from the api

            :return: dict (Example: {_id: "...", ...})
        """
        movie = self._get(self._build_url(f'/random/movie'))

        if movie:
            self.log.info(f'Got random movie {movie["_id"]}')
            return movie
        return None

    """MOVIES END"""

    """AUXILIARY METHODS START"""

    def get_best_torrent(self, torrents: dict, min_quality: int = 1080,
                         revert_to_default: bool = False) -> Optional[dict]:
        """
            Get the best torrent

            :param revert_to_default: bool (If True, it will revert to popcorn default torrent)
            :param torrents: dict (Example: {"720p": ..., "1080p": ...})
            :param min_quality: int (Example: 1080)
            :return: dict (Example: {"720p": ..., "1080p": ...})
        """
        self.log.info(f'Getting best torrent for quality {min_quality}')

        torrents = self._select_torrents_language(torrents)

        # Make list of torrents with quality > min_quality
        filtered_torrents = []
        for quality, torrent in torrents.items():
            if 'd' in quality.lower():
                continue

            quality = int(quality.replace('p', ''))
            if quality >= min_quality:
                filtered_torrents.append(torrent)

        if not filtered_torrents:
            if revert_to_default:
                self.log.info('No torrents found, reverting to default torrent')
                try:
                    return torrents['0']
                except KeyError:
                    return None
            return None

        self.log.info(f'Got {len(filtered_torrents)} torrents with quality >= {min_quality}')

        # Get the torrents with the most seeds
        filtered_torrents.sort(key=self._get_torrent_seeds, reverse=True)

        self.log.debug(f'Got torrent with most seeds: {filtered_torrents[0]}')

        return filtered_torrents[0]

    @beta
    def remove_cam_torrents(self, torrents: dict) -> Optional[dict]:
        """
            Remove torrents that where filmed by a camera
            These are normally those films that where filmed inside the cinema which
            are really annoying to watch

            :param language:
            :param torrents: dict (Example: {"720p": ..., "1080p": ...})
            :return: dict (Example: {"720p": ..., "1080p": ...})
        """

        self.log.info('Removing camera filmed torrents')

        torrents = self._select_torrents_language(torrents)

        # Make list of torrents with quality > min_quality
        filtered_torrents = {}
        for quality, torrent in torrents.items():
            url = torrent['url']
            if any(keyword in url for keyword in self._CAM_KEYWORDS):
                continue
            filtered_torrents[quality] = torrent

        if not filtered_torrents:
            logging.warning('All torrents were camera filmed')
            return None

        self.log.info(f'Got {len(filtered_torrents)} not filmed by camera')

        return filtered_torrents

    """AUXILIARY METHODS END"""


class TestPopcorn(unittest.TestCase):

    def setUp(self):
        self.popAPI = PopcornTime()

        # Check for internet connection
        logging.info('Testing internet connection ...')
        req = False
        try:
            req = requests.get("https://google.com", timeout=10)
        except Exception:
            pass

        if not req:
            logging.error(
                'Testing internet connection failed, please check your connection and try again!')
            sys.exit()

        logging.info("Internet connection test was successful")

    def test_get_show_stats(self):
        self.assertIsNotNone(self.popAPI.get_shows_stats)

    def test_get_shows_page(self):
        self.assertIsNotNone(self.popAPI.get_shows_page, 1)

    def test_get_show(self):
        self.assertIsNotNone(self.popAPI.get_show, "tt10160804")

    def test_get_random_show(self):
        self.assertIsNotNone(self.popAPI.get_random_show)

    def test_get_best_torrent(self):
        movie = self.popAPI.get_movie("tt0111161")
        torrents = movie["torrents"]
        best = self.popAPI.get_best_torrent(torrents)
        print(best)
        self.assertIsNotNone(best)

    def test_remove_cam_torrents(self):
        # Test with a movie with all camera torrents
        movie = self.popAPI.get_movie("tt8041270")
        torrents = movie["torrents"]
        no_cam = self.popAPI.remove_cam_torrents(torrents)
        print(no_cam)
        self.assertIsNone(no_cam)

        # Test with a movie with no camera torrents
        movie = self.popAPI.get_movie("tt1285016")
        torrents = movie["torrents"]
        no_cam = self.popAPI.remove_cam_torrents(torrents)
        print(no_cam)
        self.assertIsNotNone(no_cam)

    def test_get_movies_stats(self):
        self.assertIsNotNone(self.popAPI.get_movies_stats)

    def test_get_movie_page(self):
        self.assertIsNotNone(self.popAPI.get_movies_page, 1)

    def test_get_movie(self):
        self.assertIsNotNone(self.popAPI.get_movie, "tt0111161")

    def test_get_random_movie(self):
        self.assertIsNotNone(self.popAPI.get_random_movie)


if __name__ == '__main__':
    unittest.main()
