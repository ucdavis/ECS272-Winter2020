from flask_caching import Cache
import tempfile


def setup_cache(app):
    def make_cache_dir():
        return tempfile.mkdtemp()

    cache_config = {
        'CACHE_TYPE': 'filesystem',
        'CACHE_THRESHOLD': 10,
        'CACHE_DIR': make_cache_dir()
    }
    cache = Cache()
    cache.init_app(app.server, config=cache_config)
    return cache
