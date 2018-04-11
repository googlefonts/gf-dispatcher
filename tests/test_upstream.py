import unittest
import tempfile
from dispatcher.upstream import UpstreamRepo


class TestUpstreamRepo(unittest.TestCase):

    def setUp(self):
        repo_url = 'https://github.com/BornaIz/Lalezar'
        repo_fonts_dir = '/fonts'
        self.repo = UpstreamRepo(repo_url, repo_fonts_dir, '/users/marc/Desktop')

    def test_init_upstream_repo(self):
        self.assertNotEqual({}, self.repo.families)

    def test_filter_styles(self):
        """Make sure fonts which do not have styles which suite the GF Api are
        not included."""
        font_paths = [
            '/foo/bar/FamilySans-Regular.ttf',
            '/foo/bar/FamilySans-Bold.ttf',
        ]
        font_paths_incorrect = font_paths + ['/foo/bar/FamilySans-Text.ttf']

        filtered = filter(UpstreamRepo._valid_style, font_paths_incorrect)
        self.assertEqual(font_paths, filtered)


if __name__ == '__main__':
    unittest.main()
