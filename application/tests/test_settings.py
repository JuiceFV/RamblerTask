"""Tests responsible for 'load_config function which configure an application.
"""
import unittest
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import os
from sources.settings import load_config

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSettingsCases(unittest.TestCase):
    """The class which tests load_config() from application/settings.
    """
    def test_load_config_without_arguments(self):
        """The first case when an user doesn't pass a configuration file as an argument.
        Therefore the configuration copies from application/config.yaml
        """
        expected = \
            {
                'database_config':
                    {
                        'host': 'db',
                        'user': 'postgres',
                        'password': '12345qwerty',
                        'port': 5432,
                        'database': 'CatsQMS'
                    },
                'run_type': 'test'
            }
        res, _ = load_config()
        self.assertEqual(res, expected)

    def test_load_config_with_run_type_debug(self):
        """The second case when an user pass the 'debug' (python entry.py -d).
        Therefore in the configuration copied from application/config.yaml the run_type modifies onto 'debug'
        """

        expected = \
            {
                'database_config':
                    {
                        'host': 'db',
                        'user': 'postgres',
                        'password': '12345qwerty',
                        'port': 5432,
                        'database': 'CatsQMS'
                    },
                'run_type': 'debug'
            }
        res, _ = load_config(debug=True)
        self.assertEqual(res, expected)

    def test_load_config_with_run_type_release(self):
        """The second case when an user pass the 'release' (python entry.py -r).
        Therefore in the configuration copied from application/config.yaml the run_type modifies onto 'release'
        """

        expected = \
            {
                'database_config':
                    {
                        'host': 'db',
                        'user': 'postgres',
                        'password': '12345qwerty',
                        'port': 5432,
                        'database': 'CatsQMS'
                    },
                'run_type': 'release'
            }
        res, _ = load_config(release=True)
        self.assertEqual(res, expected)

    def test_load_config_with_custom_file(self):
        """A new config file updates the config.yaml (doesn't rewrite).
        Therefore it copies a data from config.yaml (rewrites if needed) and append a new data if it exists.
        """

        expected = \
            {
                # This part's been copied from config.yaml
                'database_config':
                    {
                        'host': 'db',
                        'user': 'postgres',
                        'password': '12345qwerty',
                        'port': 5432,
                        'database': 'CatsQMS'
                    },
                'run_type': 'test',
                # This is a new data which will be added to a basic configuration' data
                'option1': 'Name',
                'option2': 12345,
                'option3': 'https://rt.pornhub.com/',
                'option3_proponent': 'https://rt.pornhub.com/view_video.php?viewkey=ph5e85e9ec3f3b3'
            }

        path_to_custom_cfg = os.path.join(THIS_DIR, 'custom_cfg.yaml')
        with open(path_to_custom_cfg, 'r') as f:
            res, _ = load_config(cfg_file=f)
            self.assertEqual(res, expected)
