"""GoogleFonts Dispatcher"""
import subprocess
import argparse
import os
import json
import logging
import shutil

from repo import GFRepo
from upstream import UpstreamRepo
from qa import QA
from settings import SETTINGS
from exceptions import NoGoogleRepoPath, InvalidFontLicense
from utils import get_repo_family_name
import tempfile


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pr_family_to_googlefonts(repo_url, license, fonts, upstream_commit, qa_out, html_snippet=None):
    """Send a family pr to a google/fonts repo"""
    logger.info('Running preflight')
    qa = QA(license, fonts, qa_out)
    qa.preflight()

    #2 Package
    if not qa.passed_preflight:
        # TODO (M Foley) Submit a git issue to the upstream repo
        logger.info('Failed preflight')
        return

    repo = GFRepo()
    family_name = get_repo_family_name(fonts)

    if repo.has_family(family_name):
        logger.info('Family already exists. Replacing files')
        family = repo.get_family(family_name)
        family.replace_fonts(fonts)
        family.replace_file(license)
        family.update_metadata()
    else:
        logger.info('Family does not exist. Adding files')
        family = repo.new_family(license, family_name)
        family.add_fonts(fonts)
        family.add_file(license)
        if html_snippet:
            family.add_file(html_snippet)
        family.generate_metadata(input_designer=True, input_category=True)

    #3 QA
    qa.update_paths(fonts)
    logger.info('Running fonts through FontBakery')
    qa.fontbakery()

    qa.passed = True # When FB gets better tests, remove this.
    #3 QA: Regression Testing
    if family.is_updated and qa.passed:
        logger.info('Regression testing against fonts hosted on Google Fonts')
        qa.diffbrowsers_family_update()
    elif not family.is_updated and qa.passed:
        logger.info('Generating screenshots')
        qa.diffbrowsers_new_family()
        # TODO (M Foley) improve diffenator up to R Sheeter's spec
        # logger.info('Generating before and after images')
        # qa.diffenator()

    #4 PR
    if qa.passed:
        logger.info('QA passed. commiting fonts to {}'.format(SETTINGS['local_gf_repo_path']))
        commit_msg = repo.commit(family_name, repo_url, upstream_commit)
        # push to google/fonts. We need a bot
        logger.info('PRing fonts to {}. Be patient'.format(SETTINGS['local_gf_repo_path']))
        repo.pull_request(
            commit_msg,
            qa.fb_report,
            qa.diffbrowsers_report,
            qa.images,
            qa.path,
            qa.gfr_url)
    else:
        logger.info('QA failed. FB reported the following errors\n{}\n\n'
                    'Project state will be reset to avoid damage'.format(
                     json.dumps(qa.failed_tests, indent=4)))


def pr_upstream_to_googlefonts(upstream_url, upstream_fonts_dir, license_dir=None):
    #1 Download license and fonts
    logger.info('Downloading license and fonts from {}'.format(upstream_url))

    try:
        upstream_out = tempfile.mkdtemp()
        upstream_repo = UpstreamRepo(upstream_url, upstream_fonts_dir, upstream_out, license_dir)

        for family in upstream_repo.families:
            logger.info('PRing {} to google/fonts repo'.format(family))
            qa_out = tempfile.mkdtemp()
            pr_family_to_googlefonts(
                upstream_url,
                upstream_repo.license,
                upstream_repo.families[family],
                upstream_repo.commit,
                qa_out
            )
            shutil.rmtree(qa_out)
            git_cleanup()
    except KeyboardInterrupt:
        logger.info("Dispatcher terminated. Cleaning up.")
    finally:
        shutil.rmtree(upstream_out)


def main():
    """User specifies an upstream repository url and the dir containing the shipped fonts.

    Once finished, the temporary directories containing the reports, images
    and upstream fonts will be removed"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_url")
    parser.add_argument("repo_fonts_dir")
    parser.add_argument("--license_dir")
    args = parser.parse_args()

    if args.license_dir:
        pr_upstream_to_googlefonts(args.repo_url, args.repo_fonts_dir, args.license_dir)
    else:
        pr_upstream_to_googlefonts(args.repo_url, args.repo_fonts_dir)


def git_cleanup():
    cwd = os.getcwd()
    os.chdir(SETTINGS['local_gf_repo_path'])
    subprocess.call(['git', 'stash'])
    subprocess.call(['git', 'checkout', 'master'])
    subprocess.call(['git', 'reset', '--hard'])
    subprocess.call(['git', "clean", '-f'])
    logger.info("Repo {} reset back to master.".format(SETTINGS['local_gf_repo_path']))
    os.chdir(cwd)


if __name__ == '__main__':
    main()
