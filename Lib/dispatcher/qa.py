import os
from os.path import basename
import subprocess
import shutil
from diffbrowsers.diffbrowsers import DiffBrowsers
from diffbrowsers.utils import load_browserstack_credentials, cli_reporter
from diffbrowsers.browsers import test_browsers

from settings import SETTINGS
from exceptions import InvalidFontLicense


WEIGHTS = [
    'Thin',
    'ExtraLight',
    'Light',
    'Regular',
    'Medium',
    'Bold',
    'ExtraBold',
    'Black',
]
LIGHTEST_STYLES = WEIGHTS
HEAVIEST_STYLES = LIGHTEST_STYLES[::-1]
MIDDLE_STYLES = ['Regular', 'Italic']


class QA:
    """Wrapper to orchestate the different QA tools at Google Fonts"""
    def __init__(self, license, fonts, path):
        self.fonts = fonts
        self.license = license
        self.passed_preflight = False
        self.passed = False
        self.fb_json = None
        self.fb_report = None
        self.diffbrowsers_report = None
        self.gfr_url = None
        self.images = []
        self.path = path

        self.bstack_auth = (
            SETTINGS['browserstack_username'],
            SETTINGS['browserstack_access_key']
        )

    def preflight(self):
        """Before we run any QA tool. It is worthwile to check if the
        license and fonts are the correct type.

        Fonts must be .ttf
        License must be either Apache, OFL or UFL"""
        self._correct_license()
        self.passed_preflight = True

    def fontbakery(self):
        """Google Font's main font linter

        TODO (M Foley) talk to Lasse to figure out how to remove the
        subprocess call by using the api instead"""
        from tempfile import NamedTemporaryFile
        import json

        report = NamedTemporaryFile(mode='w')
        cmd = ['fontbakery', 'check-googlefonts'] + self.fonts + ['--ghmarkdown', report.name]
        stdout = subprocess.check_output(cmd)
        self.fb_json = json.load(open(report.name))
        self.fb_report = stdout
        report.close()

    @property
    def passed(self):
        if self.fb_json:
            if self.fb_json['result']['FAIL'] > 0:
                return False
            return True
        return None

    @property
    def failed_tests(self):
        failed = []
        if self.fb_json:
            for item in self.fb_json['sections'][0]['checks']:
                if item['result'] == 'FAIL':
                    failed.append(item)
        return failed

    def diffenator(self):
        """If the fonts are already being served by Google Fonts, we must
        ensure they haven't regressed too much from the previous release."""
        pass

    def diffbrowsers_family_update(self, fonts_before='from-googlefonts'):
        """Compare and regression test the fonts on different browsers.

        If the family contains more than 3 weights, select the thinnest,
        heaviest and median styles. Proofing more than 3 styles leads to
        huge images. The median style will likely pick up any multiple
        master compatibility issues."""
        fonts_to_test = self._select_fonts_for_diffbrowsers()
        diffbrowsers = DiffBrowsers(self.bstack_auth, self.path)
        diffbrowsers.new_session(fonts_before, fonts_to_test)
        self.gfr_url = 'http://www.gf-regression.com/compare/' + diffbrowsers.gf_regression.uuid

        diffbrowsers.diff_view('waterfall', gen_gifs=True)
        diffbrowsers.update_browsers(test_browsers['osx_browser'])
        diffbrowsers.diff_view('glyphs-modified', gen_gifs=True)
        diffbrowsers.diff_view('glyphs-missing', gen_gifs=True)
        diffbrowsers.diff_view('glyphs-new', gen_gifs=True)
        diffbrowsers.diff_view('glyphs-all', 26, gen_gifs=True)
        self._get_images()
        self.diffbrowsers_report = cli_reporter(diffbrowsers.stats)

    def diffbrowsers_new_family(self):
        fonts_to_test = self._select_fonts_for_diffbrowsers()
        diffbrowsers = DiffBrowsers(self.bstack_auth, self.path)
        diffbrowsers.new_session(fonts_to_test, fonts_to_test,)
        self.gfr_url = 'http://www.gf-regression.com/compare/' + diffbrowsers.gf_regression.uuid
        diffbrowsers.diff_view('waterfall', gen_gifs=True)

        diffbrowsers.update_browsers(test_browsers['osx_browser'])
        diffbrowsers.diff_view('glyphs-all', 26, gen_gifs=True)
        self._get_images()
        self.diffbrowsers_report = cli_reporter(diffbrowsers.stats)

    def _get_images(self):
        images = []
        for path, r, files in os.walk(self.path):
            for f in files:
                img_path = os.path.join(path, f)
                images.append(img_path)
        self.images = images

    def update_paths(self, paths):
        self.fonts = paths

    def _correct_license(self):
        legit_license_types = ['OFL.txt', 'LICENSE.txt', 'UFL.txt']
        filename = basename(self.license)
        if filename not in legit_license_types:
            raise InvalidFontLicense(filename)

    def _select_fonts_for_diffbrowsers(self):
        """Test only the most extreme and middle weights of the family.

        Testing all weights leads to huge images. If the family only
        contains 3 styles (6 for italics), use all of them."""
        if len(self.fonts) <= 3:
            return self.fonts
        elif len(self.fonts) <= 6 and has_italics(self.fonts):
            return self.fonts
        fonts = {basename(f).split('-')[1][:-4]:f for f in self.fonts}
        lightest = self._get_extrema_style(fonts, LIGHTEST_STYLES)
        middle = self._get_extrema_style(fonts, MIDDLE_STYLES)
        heaviest = self._get_extrema_style(fonts, HEAVIEST_STYLES)
        if has_italics(self.fonts):
            lightest_i_styles = [i+'Italic' for i in LIGHTEST_STYLES]
            heaviest_i_styles = [i+'Italic' for i in HEAVIEST_STYLES]

            lightest_i = self._get_extrema_style(fonts, lightest_i_styles)
            middle_i = self._get_extrema_style(fonts, ['Italic'])
            heaviest_i = self._get_extrema_style(fonts, heaviest_i_styles)
            return list(set(lightest + lightest_i + middle + middle_i + \
                        heaviest + heaviest_i))
        return list(set(lightest + middle + heaviest))

    def _get_extrema_style(self, fonts, style_priority):
        """Get the most extreme style from a list"""
        found = []
        for style in style_priority:
            if style in fonts:
                found.append(fonts[style])
                break
        return found

    def close(self):
        shutil.rmtree(self.path)


def has_italics(fonts):
    for font in fonts:
        if 'Italic' in font:
            return True
    return False
