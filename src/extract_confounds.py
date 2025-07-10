#!/usr/bin/env python3
#
# Extract motion params from fmriprep confounds file and save in FEAT format

import argparse
import os
import pandas
import scipy

parser = argparse.ArgumentParser()
parser.add_argument('--confounds_tsv', required=True)
parser.add_argument('--feat_dir', required=True)
args = parser.parse_args()

conf = pandas.read_csv(args.confounds_tsv, sep='\t')
mot = conf[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
mot = mot.apply(scipy.stats.zscore, nan_policy='omit')
mot.to_csv(
    os.path.join(args.feat_dir, 'confounds.tsv'), 
    sep='\t', 
    header=False, 
    index=False, 
    )
