import shutil
import os
import requests
import hashlib
from os.path import basename
from dispatcher.exceptions import MultipleFamilies
from StringIO import StringIO


def get_repo_family_name(paths):
    family_names = []

    for path in paths:
        family_name = basename(path).split('-')[0]
        family_names.append(family_name)

    if len(set(family_names)) > 1:
        raise MultipleFamilies
    return family_names[0].replace(' ', '').lower()


def md5_checksum(file_path):
    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()


def download_file(url, dst_path=None):
    """Download a file from a url. If no url is specified, store the file
    as a StringIO object"""
    request = requests.get(url, stream=True)
    if not dst_path:
        return StringIO(request.content)
    with open(dst_path, 'wb') as downloaded_file:
        request.raw.decode_content = True
        shutil.copyfileobj(request.raw, downloaded_file)


def get_files(root_path, filetype='.ttf'):
    fonts = []
    for path, r, files in os.walk(root_path):
        for f in files:
            if f.endswith(filetype):
                fonts.append(os.path.join(path, f))
    return fonts
