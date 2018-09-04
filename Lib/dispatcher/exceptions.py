import os


class NoGoogleRepoPath(Exception):
    def __init__(self):
        Exception.__init__(self, "Add local path to Google Fonts Repo "
                                 "in settings.py")


class InvalidFontLicense(Exception):
    def __init__(self, license):
        self.license = license
        Exception.__init__(self, "License type '{}' is not supported. Family "
                                 "License must be either OFL, UFL or Apache".format(self.license))


class MultipleFamilies(Exception):
    def __init__(self):
        Exception.__init__(self, "Cannot add multiple familes")


class IncorrectFontFormat(Exception):
    def __init__(self):
        Exception.__init__(self, "Incorrect font format. fonts must be .ttf")


class InsufficientFonts(Exception):
    def __init__(self, upstream_fonts, repo_fonts):
        self.upstream_fonts = map(os.path.basename, upstream_fonts)
        self.repo_fonts = map(os.path.basename, repo_fonts)
        Exception.__init__(
            self,
            ("Fonts must replace all existing fonts. "
             "Upstream is missing the following fonts [{}]".format(
                set(self.repo_fonts) - set(self.upstream_fonts)))
        )


class FontsAreIdentical(Exception):
    def __init__(self):
        Exception.__init__(self, "Aborting. Fonts are identical")


class NoConfigFile(Exception):
    def __init__(self, path):
        self.path = path
        Exception.__init__(self, "Config file {} is missing. See README.".format(
            self.path
        ))
