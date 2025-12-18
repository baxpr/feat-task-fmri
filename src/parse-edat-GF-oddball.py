#!/usr/bin/env python3
#
# Get Oddball task timings from eprime csv created by eprime_to_csv.py

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
starttime = [x for x in ep['Start1.OffsetTime'] if not math.isnan(x)]
if len(starttime) != 1:
    raise Exception('Wrong number of starttime found')
else:
    starttime = starttime[0]

# Columns of interest
cols = [
    'Start1.OffsetTime',
    'Procedure',
    'StandardTone.OnsetTime',
    'StandardTone.RT',
    'StandardTone.ACC',
    'DeviantTone.OnsetTime',
    'DeviantTone.RT',
    'DeviantTone.ACC',
    ]

# Rows of interest
rows = [x in ['StandardProc', 'DeviantProc'] for x in ep.Procedure]

# Reduce the table to modeled events
ep = ep.loc[rows,cols]

# Combine timings for both conditions
ep['Condition'] = ''
ep['OnsetTime'] = math.nan
ep['RT'] = math.nan
ep['ACC'] = math.nan

ep.loc[ep.Procedure=='DeviantProc', 'Condition'] = 'Deviant'
ep.loc[ep.Procedure=='DeviantProc', 'OnsetTime'] = ep.loc[ep.Procedure=='DeviantProc', 'DeviantTone.OnsetTime']
ep.loc[ep.Procedure=='DeviantProc', 'RT'] = ep.loc[ep.Procedure=='DeviantProc', 'DeviantTone.RT']
ep.loc[ep.Procedure=='DeviantProc', 'ACC'] = ep.loc[ep.Procedure=='DeviantProc', 'DeviantTone.ACC']

ep.loc[ep.Procedure=='StandardProc', 'Condition'] = 'Standard'
ep.loc[ep.Procedure=='StandardProc', 'OnsetTime'] = ep.loc[ep.Procedure=='StandardProc', 'StandardTone.OnsetTime']
ep.loc[ep.Procedure=='StandardProc', 'RT'] = ep.loc[ep.Procedure=='StandardProc', 'StandardTone.RT']
ep.loc[ep.Procedure=='StandardProc', 'ACC'] = ep.loc[ep.Procedure=='StandardProc', 'StandardTone.ACC']


# Compute stimulus timings in seconds relative to fmri start
ep['OnsetSec'] = [(x - starttime) / 1000 for x in ep['OnsetTime']]

# Durations, parametric modulation
ep['DurationSec'] = 0.5
ep['ParaMod'] = 1

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
