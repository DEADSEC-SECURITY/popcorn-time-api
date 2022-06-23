# Popcorn Time API ![Version](https://img.shields.io/badge/Version-v1.0.0-orange?style=flat-square&url=https://github.com/DEADSEC-SECURITY/popcorn-time-api/blob/main/CHANGELOG.md) ![Python_Version](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-red?style=flat-square) ![Donate](https://img.shields.io/badge/Donate-Crypto-yellow?style=flat-square) [![CodeQL](https://github.com/DEADSEC-SECURITY/popcorn-time-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/DEADSEC-SECURITY/popcorn-time-api/actions/workflows/codeql-analysis.yml) [![CodeQL](https://github.com/DEADSEC-SECURITY/popcorn-time-api/actions/workflows/python-app.yml/badge.svg)](https://github.com/DEADSEC-SECURITY/popcorn-time-api/actions/workflows/python-app.yml) [![Downloads](https://pepy.tech/badge/popcorn-time)](https://pepy.tech/project/popcorn-time) [![Downloads](https://pepy.tech/badge/popcorn-time/month)](https://pepy.tech/project/popcorn-time)
 
## 📝 CONTRIBUTIONS

Before doing any contribution read <a href="https://github.com/DEADSEC-SECURITY/popcorn-time-api/blob/main/CONTRIBUTING.md">CONTRIBUTING</a>.

## 📧 CONTACT

Email: amng835@gmail.com

General Discord: https://discord.gg/dFD5HHa

Developer Discord: https://discord.gg/rxNNHYN9EQ

## 📥 INSTALLING
<a href="https://pypi.org/project/popcorn-time">Latest PyPI stable release</a>
```bash
pip install popcorn-time
```

## ⚙ HOW TO USE
```python
from popcorntime import PopcornTime
popAPI = PopcornTime()
```

## 🤝 PARAMETERS
### CLASS PARAMETERS
- **debug** : bool, optional
  - Enable for debug mode (Default: False)
- **min_peers** : int, optional
  - Minimum number of peers to select torrent (Default: 0)
- **min_seeds** : int, optional
  - Minimum number of seeds to select torrent (Default: 0)
### FUNCTION PARAMETERS
- #### FUNCTION `set_logging_level`
  - **level** : int, required
    - Set the logging level
    - Accepted values:
      - 0: DEBUG
      - 1: INFO
      - 2: WARNING
      - 3: ERROR
      - 4: CRITICAL
      - 5: NOTSET
- #### FUNCTION `set_base_url`
  - **url** : str, required
    - Set the base url for the API
- #### FUNCTION `set_base_url`
  - **url** : str, required
    - Set the base url for the API
- #### FUNCTION `set_min_seeds`
  - **value** : int, required
    - Minimum number of seeds to select torrent
- #### FUNCTION `get_server_status`
  - Returns the server status in json format
- #### FUNCTION `get_shows_stats`
  - Returns the show stats in json format
- #### FUNCTION `get_shows_page`
  - **page** : (int, str), required
  - Returns the shows page in json format
- #### FUNCTION `get_movies_stats`
  - Returns the movies stats in json format
- #### FUNCTION `get_movies_page`
  - **page** : (int, str), required
  - Returns the movies page in json format
- #### FUNCTION `get_show`
  - **show_id** : (int, str), required
    - IMDB ID of the show
  - Returns the show data in json format
- #### FUNCTION `get_movie`
  - **movie_id** : (int, str), required
    - IMDB ID of the movie
  - Returns the movie data in json format
- #### FUNCTION `get_random_show`
  - Returns the show in json format
- #### FUNCTION `get_random_movie`
  - Returns the movie in json format
- #### FUNCTION `get_best_torrent`
  - **torrents** : dict, required
    - The dictionary of torrents provided by the API (get_show or get_movie)
  - **min_quality** : int, optional
    - Minimum quality to select torrent (Default: '1080')
  - **revert_to_default** : bool, optional
    - Revert to default item if no torrents are found (Default: False)
  - Returns the best torrent is json format
- #### FUNCTION `remove_cam_torrents`
  - **torrents** : dict, required
    - The dictionary of torrents provided by the API (get_show or get_movie)
  - Returns all the torrents without cam in json format

## Legal Notice
This SDK is not meant to be used for illegal purposes, use it at your own risk and check your local regulations first.
