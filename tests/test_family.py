import os
import unittest
import shutil

from dispatcher.repo import Family
from dispatcher.exceptions import IncorrectFontFormat, InsufficientFonts


class TestFamily(unittest.TestCase):

    def setUp(self):
        this_file_path = os.path.dirname(__file__)
        self.ofl_dir = os.path.join(this_file_path, 'data', 'oswald')
        self.upstream_dir = os.path.join(this_file_path, 'data', 'OswaldFont')
        self.family = Family(ofl_dir)

    def tearDown(self):
        pass

    def test_attrs(self):
        self.assertEqual('oswald', self.family.name)
        self.assertEqual(6, len(self.family.fonts))

    def test_replace_fonts(self):
        new_fonts = ['foo/Oswald-Regular.svg', 'foo/Oswald-Bold.svg']
        # Test ttf only exception
        self.assertRaises(IncorrectFontFormat,
                          self.family.replace_fonts,
                          new_fonts)
        # Test insufficient fonts
        new_fonts = ['foo/Oswald-Regular.ttf', 'foo/Oswald-Bold.ttf']
        self.assertRaises(InsufficientFonts,
                          self.family.replace_fonts,
                          new_fonts)

    def test_replace_file(self):
        new_license = os.path.join(self.upstream_dir, 'OFL.txt')
        self.family.replace_file(new_license)


if __name__ == '__main__':
    unittest.main()
