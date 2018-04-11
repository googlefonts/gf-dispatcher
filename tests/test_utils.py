import unittest
import os
from dispatcher.utils import get_repo_family_name


class TestUtils(unittest.TestCase):

    def test_get_family_name(self):
        font_paths = [
            os.path.join('foo', 'Bar-Regular.ttf'),
            os.path.join('foo', 'Bar-Bold.ttf')
        ]
        family_name = get_repo_family_name(font_paths)
        self.assertEqual('bar', family_name)


if __name__ == '__main__':
    unittest.main()
