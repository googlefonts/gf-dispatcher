# Google Fonts Dispatcher.

PR upstream font repositories to any forked Google Font repository.

## How it works

### Updating an existing font family

0. Download resources from Upstream font repo:
    - Download fonts
    - Download license
    - Terminate if multiple license files are found

1. Initial QA:
    - Stop if there is no license file
    - Run though fontbakery
    - (TODO) If errors, report them to the upstream

2. Package:
    - Check license
    - Get folder google/fonts dir
    - Replace fonts from upstream dir
    - Replace license from upstream dir
    - Regenerate METADATA.pb file

3. QA:
    - Rerun through fontbakery
    - Gen images using diff browsers
    - Run through diffenator

4. PR:
    - Git commit update folder
    - Send pr to google/fonts or forked repo

### Adding a new family

0. Download resources from Upstream font repo:
    - Download fonts
    - Download license
    - Terminate if multiple license files are found

1. Initial QA:
    - Stop if there is no license file and report to upstream repo
    - Run through fontbakery
    - (TODO) If errors, stop and file errors to upstream repo

2. Package:
    - Check license
    - Create lowercase folder of family name
    - Copy fonts from upstream to dir
    - Copy license from upstream to dir
    - Generate METADATA.pb and placeholder Description.html
    - Update html description with user text

3. QA:
    - Rerun through fontbakery
    - Gen images using diffbrowsers

4. PR:
    - Git commit the new folder
    - Send pr to google/fonts or <head>/fonts


## Usage:

```
dispatcher github_upstream_url /path/to/repo/fonts/dir
```

e.g https://github.com/googlefonts/caveat:
```
dispatcher https://github.com/googlefonts/caveat /fonts/TTF
```


## Installation

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

### Authentification and path provisions

Dispatcher relies on several 3rd party aplications and their apis. We keep the authentification credentials and paths to these services in a hidden file. A template has been included in this repo called *gf-dispatcher-config*. Once you have completed it, `mv gf-dispatcher-credentials ~/.gf-dispatcher-config'`.


### 3rd party

Dispatcher uses the following 3rd party services:

- Imgur
- Google Drive


**Imgur**

This service is used to host the gifs which are included every pull request that Dispatcher makes.

Once you have registed an account, you'll need to create an application. Dispatcher only needs the application's Client ID to work. Include this in `~/.gf-dispatcher-credentials`


**Google Drive**

Drive is used for uploading a zip of all the image files. We don't include every image in the body of the pull request. If the report looks suspicious, reviewers can download the zip and inspect the images themselves.

Follow authentification step in the quickstart guide to get setup, https://pythonhosted.org/PyDrive/quickstart.html.

TODO (M Foley) make 3rd party services easier to install.
