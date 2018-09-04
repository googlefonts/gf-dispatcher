
download_fonts
    - Only download ttfs
download_license
    - Only take ofl/apache/ufl. Abort if no license 

package_into_dir
    - If fonts are identical abort
    - If font version has not increased abort

QA:
    - Run through FB, if FAILS, abort
    - If family already exists, generate diffs

PR:
    - 