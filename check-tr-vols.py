#!/usr/bin/env python
#
# Verify that a design.fsf file has the correct TR and nvols matching
# the nifti file

# set fmri(tr) 1.300001
# set fmri(npts) 224
# set feat_files(1) "SUBJDIR/preproc_bold.nii.gz"

import argparse
import nibabel


parser = argparse.ArgumentParser()
parser.add_argument('--design_fsf', required=True)
args = parser.parse_args()

# Count feat_files and bail if more than one

# Read TR, nvols lines

