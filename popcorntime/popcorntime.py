import requests
import logging
import sys
import unittest

from urllib.parse import urljoin


class PopcornTime:
    _BASE_URL: str = 'https://popcorn-ru.tk/'
    _MIN_SEEDS: int = 0
    _MIN_PEERS: int = 0

    def __init__(self, debug: bool = False, min_peers: int = 0, min_seeds: int = 0):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG if debug else logging.INFO)
        self.log.addHandler(logging.StreamHandler(sys.stdout))

        self._MIN_PEERS = min_peers
        self._MIN_SEEDS = min_seeds

    def _get(self, url: str, **kwargs) -> (requests.Response.json, None):
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

    @staticmethod
    def _get_torrent_peers(torrent):
        """
            Movie have different seed name for the same thing so
            this function will handle that difference

            :param torrent:
            :return:
        """
        try:
            return torrent['peers']
        except KeyError:
            return torrent['peer']

    def set_logging_level(self, level: int) -> int:
        """
            Sets the logging level

            :param level: int (Example: logging.DEBUG)
            :return: int (Example: logging.DEBUG)
        """

        self.log.setLevel(level)

        return level

    def set_base_url(self, url: str) -> str:
        """
            Sets the base URL

            :param url: string (Example: "http://popcorntime.com")
            :return: string (Example: "http://popcorntime.com")
        """

        self._BASE_URL = url

        return self._BASE_URL

    def set_min_seeds(self, value: int) -> int:
        """
            Sets the base URL

            :param value: int (Example: 50)
            :return: int (Example: 50)
        """

        self._MIN_SEEDS = value

        return self._MIN_SEEDS

    def set_min_peers(self, value: int) -> int:
        """
            Sets the base URL

            :param value: int (Example: 50)
            :return: int (Example: 50)
        """

        self._MIN_PEERS = value

        return self._MIN_PEERS

    def get_server_status(self) -> (requests.Response.json, None):
        """
            Get the server status

            :return: dict (Example: {"repo": ..., "version": ..., "uptime": ...})
        """

        status = self._get(self._build_url('/status'))

        if status:
            self.log.info('Got status')
            return status
        return None

    def get_shows_stats(self) -> (requests.Response.json, None):
        """
            Get the shows stats

            :return: dict (Example: {"action & adventure": {"count": 600, "title": "Action & Adventure"}})
        """

        stats = self._get(self._build_url('/shows/stat'))

        if stats:
            self.log.info('Got shows stats')
            return stats
        return None

    def get_shows_page(self, page: (int, str)) -> (requests.Response.json, None):
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

    def get_show(self, show_id: (int, str)) -> (requests.Response.json, None):
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

    def get_random_show(self) -> (requests.Response.json, None):
        """
            Get a random show

            :return: dict (Example: {"_id": "...", ...})
        """

        show = self._get(self._build_url(f'/random/show'))

        if show:
            self.log.info(f'Got random show {show["_id"]}')
            return show
        return None

    def get_best_quality_torrent(self, torrents: dict) -> (tuple, None):
        """
            Gets the show torrent with the best quality

            :param torrents: dict (Example: {"0": {"url": "magnet:?xt=urn:btih:..."}})
            :return: tuple<dict, int> (Example: ({"url": "magnet:?xt=urn:btih:..."}, 1080))
        """

        # Some torrents have different "sections" for each language so we will try
        # to get the en language all the time

        try:
            torrents = torrents['en']
        except KeyError:
            pass

        best_quality = -1
        best_quality_torrent = None
        for torrent_quality, torrent_data in torrents.items():
            # The dictionary identified is the quality but we need to make sure it's a number
            quality = int(torrent_quality.replace('p', ''))
            if quality > best_quality:
                # Check if torrent quality has minimum seeds/peers
                if self._get_torrent_seeds(torrent_data) >= self._MIN_SEEDS and \
                        self._get_torrent_peers(torrent_data) >= self._MIN_PEERS:
                    best_quality = quality
                    best_quality_torrent = torrent_data

        if best_quality_torrent:
            self.log.info(f'Got best quality torrent {best_quality_torrent["url"]}')
            return best_quality_torrent, best_quality

        # Try to revert to the default torrent if no torrents meet the minimum requirements
        if torrents["0"]:
            logging.info('Reverting to first torrent')
            return torrents["0"], 0

        logging.info('No torrents meet the minimum requirements and no torrent to revert to')
        return None

    def get_movies_stats(self) -> (requests.Response.json, None):
        """
            Get the movies stats

            :return: dict (Example: {"action & adventure": {"count": 600, "title": "Action & Adventure"}})
        """

        stats = self._get(self._build_url('/movies/stat'))

        if stats:
            self.log.info('Got movies stats')
            return stats
        return None

    def get_movies_page(self, page: (int, str)) -> (requests.Response.json, None):
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

    def get_movie(self, movie_id: (int, str)) -> (requests.Response.json, None):
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

    def get_random_movie(self) -> (requests.Response.json, None):
        """
            Gets a random movie from the api

            :return: dict (Example: {_id: "...", ...})
        """
        movie = self._get(self._build_url(f'/random/movie'))

        if movie:
            self.log.info(f'Got random movie {movie["_id"]}')
            return movie
        return None


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
            logging.error('Testing internet connection failed, please check your connection and try again!')
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

    def test_get_best_quality_torrent(self):
        show = self.popAPI.get_movie("tt0111161")
        torrents = show["torrents"]
        self.assertIsNotNone(self.popAPI.get_best_quality_torrent(torrents))

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
