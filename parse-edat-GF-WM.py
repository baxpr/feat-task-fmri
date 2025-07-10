#!/usr/bin/env python
#
# Get WM task timings from eprime csv created by eprime_to_csv.py

import argparse
import math
import os
import pandas

parser = argparse.ArgumentParser()
parser.add_argument('--eprime_csv', required=True)
parser.add_argument('--feat_dir', required=True)
args = parser.parse_args()

ep = pandas.read_csv(args.eprime_csv)

# Find fmri start time
starttime = [x for x in ep['GetReady.OffsetTime'] if not math.isnan(x)]
if len(starttime) != 1:
    raise Exception('Wrong number of starttime found')
else:
    starttime = starttime[0]

# Columns of interest
cols = [
    'Procedure',
    'GetReady.OffsetTime',
    'StimType',
    'BlockType',
    'Stim.OnsetTime',
    'Stim.RT',
    'Stim.ACC',
    ]

# Rows of interest
rows = [x in ['TrialsPROC'] for x in ep.Procedure]

# Reduce the table
ep = ep.loc[rows,cols]

# Compute stimulus timings in seconds relative to fmri start
ep['OnsetSec'] = [(x - starttime) / 1000 for x in ep['Stim.OnsetTime']]

# Durations, parametric modulation
ep['DurationSec'] = 2.5
ep['ParaMod'] = 1

# Condition names
ep['Condition'] = ep.BlockType + '_' + ep.StimType

# Save events file for each condition
os.makedirs(args.feat_dir, exist_ok=True)
for c in set(ep.Condition):
    efile = os.path.join(args.feat_dir, f'events_{c}.tsv')
    rows = ep.loc[ep.Condition==c,:]
    rows.to_csv(
        efile, 
        sep='\t', 
        columns=['OnsetSec', 'DurationSec', 'ParaMod'], 
        header=False, 
        index=False, 
        )
