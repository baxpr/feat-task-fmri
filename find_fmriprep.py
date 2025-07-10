#!/usr/bin/env python

import argparse
import bids

parser = argparse.ArgumentParser()
parser.add_argument('--fmriprep_dir', required=True)
parser.add_argument('--space', default='MNI152NLin6Asym')
parser.add_argument('--task', default='bold')
parser.add_argument('--output', required=True)
args = parser.parse_args()

bids_fmriprep = bids.layout.BIDSLayout(args.fmriprep_dir, validate=False)

fmri_niigz = bids_fmriprep.get(
    space=args.space,
    extension='.nii.gz',
    desc='preproc',
    suffix=args.task,
    )
if len(fmri_niigz)!=1:
    raise Exception(f'Found {len(fmri_niigz)} fmri .nii.gz instead of 1')
fmri_niigz = fmri_niigz[0]

mask_niigz = bids_fmriprep.get(
    space=args.space,
    extension='.nii.gz',
    desc='brain',
    suffix='mask',
    task=fmri_niigz.get_entities()['task'],
    run=fmri_niigz.get_entities()['run'],
    )
if len(mask_niigz)!=1:
    raise Exception(f'Found {len(mask_niigz)} mask .nii.gz instead of 1')
mask_niigz = mask_niigz[0]

confounds_tsv = bids_fmriprep.get(
    extension='tsv',
    desc='confounds',
    suffix='timeseries',
    )
if len(confounds_tsv)!=1:
    raise Exception(f'Found {len(confounds_tsv)} confounds.tsv instead of 1')
confounds_tsv = confounds_tsv[0]

if args.output=='fmri':
    print(fmri_niigz.path)
elif args.output=='mask':
    print(mask_niigz.path)
elif args.output=='confounds':
    print(confounds_tsv.path)
else:
    raise Exception(f'Requested output {args.output} not known')

