# Google Fonts Dispatcher.

PR upstream font repositories to any forked Google Font repository.

## How To Upload Fonts to Google Fonts

This guide will assist users in uploading fonts to the [google/fonts](https://github.com/google/fonts) repository.

1. Make sure your font family has its own Github repo and complies with the [checklist](https://github.com/googlefonts/gf-docs/blob/master/ProjectChecklist.md)
2. Create your own fork of https://github.com/google/fonts and clone your fork locally
3. Get a [BrowserStack "open source" account](https://www.browserstack.com/opensource)
4. Download and install [gfdispatcher]().
5. Run `gfdispatcher GITHUB-REPO-URL /path-containing-ttfs`. Eg, for <https://github.com/googlefonts/anaheimFont> the command will be:

    gfdispatcher https://github.com/googlefonts/anaheimFont /fonts/ttf

Note that (1) could be made more simple with a set of Font Bakery checks for repos; and this whole uploading process could be more simple with a web service that runs the dispatcher remotely. 


## How GF Dispatcher works



4. QA the fonts using fontbakery and diffbrowsers
5. Send a PR to the user's google/fonts fork.
6. If the user is happy with the pr, he can resend the pr to google/fonts
7. google/fonts PR gets reviewed by GF team
8. PR is merged by GF team
9. google/fonts master branch is pushed to GF sandbox API and Directory servers and checked
10. google/fonts master branch is pushed to GF production API and Directory servers


## What makes for a successful pull request?

The biggest factor today to determine whether a pull request is accepted or not is these QA tools.
The GF Reviewers team has discretion to accept PRs even if some checks are failing.

## How it works

### Updating an existing font family

0. Download resources from Upstream font repo

- Download fonts
- Download license
- Terminate if multiple license files are found

1. Initial QA

- Stop if there is no license file
- Run though [fontbakery](https://github.com/googlefonts/fontbakery)
- (TODO) If errors, report them to the upstream

2. Package downloaded files into a **family dir**, located in the user's local clone of the github.com/google/fonts repo

- Check license
- Get dir location of local clone of [google/fonts](https://github.com/google/fonts) repo
- Replace fonts in cloned dir with fonts from upstream dir
- Replace license in cloned dir with license from upstream dir
- Regenerate `METADATA.pb` file for the dir, using script in [googlefonts/tools](https://github.com/googlefonts/tools) with update argument

3. QA & Compare

- Re-run through [fontbakery](https://github.com/googlefonts/fontbakery)
- Gen images using [diffbrowsers](https://github.com/googlefonts/diffbrowsers)
- Run through [diffenator](https://github.com/googlefonts/fontdiffenator)

4. PR

- Git commit update folder
- Send pr to [google/fonts](https://github.com/google/fonts) or forked repo

### Adding a new family

0. Download resources from Upstream font repo

- Download fonts
- Download license
- Terminate if multiple license files are found

1. Initial QA

- Stop if there is no license file and report to upstream repo
- Run through [fontbakery](https://github.com/googlefonts/fontbakery)
- (TODO) If errors, stop and file errors to upstream repo

2. Package

- Check license
- Get dir location of local clone of [google/fonts](https://github.com/google/fonts) repo
- Create dir of family name (lowercase, all one word) under license dir inside repo dir 
- Copy fonts from upstream to dir
- Copy license from upstream to dir
- Generate `METADATA.pb` and placeholder `DESCRIPTION.html`
- Update html file with project text

3. QA & Compare
- Rerun through [fontbakery](https://github.com/googlefonts/fontbakery)
- Gen images using [diffbrowsers](https://github.com/googlefonts/diffbrowsers)

4. PR

- Git commit the new dir
- Send pr to [google/fonts](https://github.com/google/fonts) or `<head>/fonts`


## Usage:


    dispatcher github_upstream_url /path/to/repo/fonts/dir ;

Example: For <https://github.com/googlefonts/caveat> run

    dispatcher https://github.com/googlefonts/caveat /fonts/TTF ;

## Installation

    virtualenv venv ;
    source venv/bin/activate ;
    pip install -r requirements.txt ;
    pip install -e . ;

### Authentification and path provisions

Dispatcher relies on several 3rd party applications and their APIs.
We keep the authentification credentials and paths to these services in a hidden file.
A template has been included in this repo called `gf-dispatcher-config`.
Once you have completed it, run

    mv gf-dispatcher-credentials ~/.gf-dispatcher-config ;

### 3rd party

Dispatcher uses the following 3rd party services:

#### Imgur

This service is used to host the gifs which are included every pull request that Dispatcher makes.

Once you have registed an account, you'll need to create an application. Dispatcher only needs the application's Client ID to work. Include this in `~/.gf-dispatcher-credentials`


#### Google Drive

Drive is used for uploading a zip of all the image files. We don't include every image in the body of the pull request. If the report looks suspicious, reviewers can download the zip and inspect the images themselves.

Follow authentification step in the quickstart guide to get setup, <https://pythonhosted.org/PyDrive/quickstart.html>
