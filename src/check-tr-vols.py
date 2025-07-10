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

with open(args.design_fsf, 'rt') as fsf:
    fsflines = fsf.readlines()

tr = float('nan')
npts = float('nan')
fmri_niigz = ''
niicnt = 0
for ell in fsflines:
    if ell.startswith('set fmri(tr)'):
        tr = float(ell.split(' ')[2].strip())
    elif ell.startswith('set fmri(npts)'):
        npts = int(ell.split(' ')[2].strip())
    elif ell.startswith('set feat_files'):
        niicnt = niicnt + 1
        if niicnt > 1:
            raise Exception('More than 1 feat_file')
        fmri_niigz = ell.split(' ')[2].strip().strip('"')

if tr != tr:
    raise Exception(f'No fmri(tr) found in {args.design_fsf}')
if npts != npts:
    raise Exception(f'No fmri(npts) found in {args.design_fsf}')
if fmri_niigz == '':
    raise Exception(f'No feat_files found in {args.design_fsf}')

print(fmri_niigz)
fmri_img = nibabel.load(fmri_niigz)
nii_tr = fmri_img.header['pixdim'][4]
nii_npts = fmri_img.header['dim'][4]

if abs(tr-nii_tr) > 0.001:
    raise Exception(f'Design TR {tr} does not match nifti TR {nii_tr}')
if npts != nii_npts:
    raise Exception(f'Design npts {npts} does not match nifti npts {nii_npts}')

