import unittest
from glob import glob
import shutil
import os
from dispatcher.qa import QA


class TestQA(unittest.TestCase):

    def setUp(self):
        this_file_path = os.path.dirname(__file__)

        master_ofl_dir = os.path.join(this_file_path, 'data', '_oswald')
        self.ofl_dir = os.path.join(this_file_path, 'data', 'oswald')
        shutil.copytree(master_ofl_dir, self.ofl_dir)
        license_file = os.path.join(self.ofl_dir, 'OFL.txt')
        fonts = glob(os.path.join(self.ofl_dir, '*.ttf'))
        self.qa = QA(license_file, fonts, '/users/marc/Desktop')

    def tearDown(self):
        shutil.rmtree(self.ofl_dir)

    def test_select_fonts_for_diffbrowsers(self):
        self.assertEqual(
            [
                'tests/data/oswald/Oswald-ExtraLight.ttf',
                'tests/data/oswald/Oswald-Regular.ttf',
                'tests/data/oswald/Oswald-Bold.ttf'
            ],
            self.qa._select_fonts_for_diffbrowsers()
        )

        fonts = [
            os.path.join('foo', 'Family-Regular.ttf')
        ]
        self.qa.fonts = fonts
        self.assertEqual(
            fonts,
            self.qa._select_fonts_for_diffbrowsers())

        fonts = [
            os.path.join('foo', 'Family-Regular.ttf'),
            os.path.join('foo', 'Family-Bold.ttf')
        ]
        self.qa.fonts = fonts
        self.assertEqual(
            fonts,
            self.qa._select_fonts_for_diffbrowsers()
        )

        fonts = [
            os.path.join('foo', 'Family-Light.ttf'),
            os.path.join('foo', 'Family-LightItalic.ttf'),
            os.path.join('foo', 'Family-Regular.ttf'),
            os.path.join('foo', 'Family-Italic.ttf'),
            os.path.join('foo', 'Family-Bold.ttf'),
            os.path.join('foo', 'Family-BoldItalic.ttf'),
            os.path.join('foo', 'Family-ExtraBold.ttf'),
            os.path.join('foo', 'Family-ExtraBoldItalic.ttf'),
            os.path.join('foo', 'Family-Black.ttf'),
            os.path.join('foo', 'Family-BlackItalic.ttf')
        ]
        self.qa.fonts = fonts
        self.assertEqual(
        [
            os.path.join('foo', 'Family-Light.ttf'),
            os.path.join('foo', 'Family-LightItalic.ttf'),
            os.path.join('foo', 'Family-Regular.ttf'),
            os.path.join('foo', 'Family-Italic.ttf'),
            os.path.join('foo', 'Family-Black.ttf'),
            os.path.join('foo', 'Family-BlackItalic.ttf')
        ],
            self.qa._select_fonts_for_diffbrowsers()
        )

        self.qa.fonts = [
            '/var/folders/f7/2dqpt71s6f7b91z7_vbgykkm0000gn/T/tmp8_JXCT/VollkornSC-Regular.ttf',
            '/var/folders/f7/2dqpt71s6f7b91z7_vbgykkm0000gn/T/tmp8_JXCT/VollkornSC-Regular.ttf',
            '/var/folders/f7/2dqpt71s6f7b91z7_vbgykkm0000gn/T/tmp8_JXCT/VollkornSC-Black.ttf']



if __name__ == '__main__':
    unittest.main()
