import os
import shutil
import json
import requests
import tempfile
import logging
from utils import download_file


VALID_STYLES = [
    'Thin',
    'ExtraLight',
    'Light',
    'Regular',
    'Medium',
    'SemiBold',
    'Bold',
    'ExtraBold',
    'Black',
    '' # Some old GF legacy fonts didn't include a stylename
]

VALID_STYLES = VALID_STYLES + [i + 'Italic' for i in VALID_STYLES]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpstreamRepo:
    def __init__(self, url, fonts_dir, path):
        self.path = path
        self.url = url.replace('.git', '') if url.endswith('.git') else url
        self.license =  self._get_license(self.url)
        self.families = self._get_family_fonts(self.url, fonts_dir)
        self.html_snippet = self._get_html_snippet(self.url)

    def _get_family_fonts(self, url, fonts_dir, filter_styles=True):
        """Download fonts from a repo directory.

        Often, font dirs can contain multiple sub families. For instance,
        Montserrat contains the Roman and Alternate families in the same
        dir, https://github.com/JulietaUla/Montserrat/tree/master/fonts/ttf.
        At GF, we count these as seperate families so they must be pr'd
        individually, they are not served from the same api request.

        The filter_styles param won't add fonts whose styles don't comply to
        the GF api."""
        families = {}
        fonts = self._download_files(url, fonts_dir)
        if filter_styles:
            fonts = filter(self._valid_style, fonts)
            fonts = filter(self._is_ttf, fonts)

        for font in fonts:
            family = os.path.basename(font.split('-')[0])
            if family not in families:
                families[family] = []
            families[family].append(font)
        return families

    @staticmethod
    def _valid_style(font_path):
        """Determine if a font style is valid for the GF API

        :type: path: str
        :rtype: boolean"""
        try:
            style = os.path.basename(font_path)[:-4].split('-')[1]
        except IndexError:
            style = 'Regular'
        if style in VALID_STYLES:
            return True
        logger.warn("skipping {}. {} not valid style".format(font_path, style))
        return False

    @staticmethod
    def _is_ttf(font_path):
        return True if font_path.endswith('.ttf') else False

    def _download_files(self, url, dirs=None, files=None):
        """Download files from a github repo directory.

        If no files are listed, download all the files contained in the dir"""
        items = []
        api_url = self._convert_url_to_api_url(url, dirs)
        request = requests.get(api_url)
        api_request = json.loads(request.text)
        for item in api_request:
            if not item['download_url']:
                continue

            dl_url = item['download_url']
            file_path = os.path.join(self.path, item['name'])
            if files:
                if item['name'] in files:
                    items.append(file_path)
                    download_file(dl_url, file_path)
            else:
                items.append(file_path)
                download_file(dl_url, file_path)
        return items

    def _convert_url_to_api_url(self, url, dirs=None):
        """
        https://github.com/m4rc1e/Pacifico -->
        https://api.github.com/repos/m4rc1e/Pacifico/contents/
        """
        url = url.replace('https://github.com/', 'https://api.github.com/repos/')
        url = url + '/contents'
        if dirs:
            url = url + dirs
        return url

    def _get_license(self, url):
        license = self._download_files(
            url,
            files=['OFL.txt', 'UFL.txt', 'LICENSE.txt']
        )
        if len(license) > 1:
            raise Exception('Multiple license files discovered "{}". Repo '
                            'should only contain one license'.format(
                                ', '.join(license))
                            )
        else:
            return license[0]

    def _get_html_snippet(self, url):
        snippet = self._download_files(
            url, files=['DESCRIPTION.en_us.html']
        )
        if len(snippet) == 0:
            return None
        return snippet[0]

    def close(self):
        """
        Delete the temporary folder which holds the resources
        """
        shutil.rmtree(self.path)
