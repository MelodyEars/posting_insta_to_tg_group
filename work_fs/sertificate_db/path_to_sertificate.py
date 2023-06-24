import os
from pathlib import Path

from work_fs import path_in_exefile


def path_to_sertificate():
    """return path to sertificate"""

    # path_this_file = os.path.abspath(__file__)
    # bundle_dir = path_in_exefile(path_this_file)
    #
    # path_to_certificate = os.path.join(bundle_dir, 'ca-certificate.crt')

    path_this_file = Path(__file__).resolve()
    bundle_dir = path_in_exefile(path_this_file)

    path_to_certificate = bundle_dir / 'ca-certificate.crt'
    return path_to_certificate
