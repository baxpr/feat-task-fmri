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
starttime = [x for x in ep['Instructions.OffsetTime'] if not math.isnan(x)]
if len(starttime) != 1:
    raise Exception('Wrong number of starttime found')
else:
    starttime = starttime[0]

# Columns of interest
cols = [
    'ImageType',
    'bbcolor',
    'PresentPicture.OnsetTime',
    ]

# Rows of interest
rows = [x in ['Scene', 'Scramble'] for x in ep.ImageType]

# Reduce the table to modeled events
ep = ep.loc[rows,cols]

# Combine timings for both conditions
ep['Condition'] = ''
ep['OnsetTime'] = math.nan

ep.loc[ep.ImageType=='Scene', 'Condition'] = 'Scene'
ep.loc[ep.ImageType=='Scene', 'OnsetTime'] = ep.loc[ep.ImageType=='Scene', 'PresentPicture.OnsetTime']

ep.loc[ep.ImageType=='Scramble', 'Condition'] = 'Scramble'
ep.loc[ep.ImageType=='Scramble', 'OnsetTime'] = ep.loc[ep.ImageType=='Scramble', 'PresentPicture.OnsetTime']

# Response trials overlap so done separately
ep2 = ep.loc[ep.bbcolor=='red', :]
ep2['Condition'] = 'Response'

# Combine
ep = pandas.concat([ep, ep2])

# Compute stimulus timings in seconds relative to fmri start
ep['OnsetSec'] = [(x - starttime) / 1000 for x in ep['OnsetTime']]

# Durations, parametric modulation
ep['DurationSec'] = 1
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
