import json
import sys

_conf_cache = None  # caches config.json


def get_config():
    """
    Returns a cached `dict` of `config.json`
    If the cached `dict` does not exist, will try to load `config.json` from project root
    :return: cached `dict` of `config.json`
    """
    global _conf_cache
    if _conf_cache is None:
        with open('config.json', 'r') as f:
            _conf_cache = json.load(f)
    return _conf_cache
