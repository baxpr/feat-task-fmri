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

# Find fmri start time (use the onset of trigger item as start time for the old
# version of oddball task)
starttime = [x for x in ep['scanstart2.OnsetTime'] if not math.isnan(x)]
if len(starttime) != 1:
    raise Exception('Wrong number of starttime found')
else:
    starttime = starttime[0]

# Columns of interest
cols = [
    'scanstart2.OnsetTime',
    'Running',
    'duration',
    'tone',
    'MainScreen.OnsetTime',
    'MainScreen.RT',
    'MainScreen.ACC',
    ]

# Rows of interest
rows = [x=='MainStimuli' for x in ep.Running]

# Reduce the table to modeled events
ep = ep.loc[rows,cols]

# Combine timings for both conditions
ep['Condition'] = ''
ep['OnsetTime'] = math.nan

ep = ep.loc[ep.tone!='stimuli\\silence.wav', :]

ep.loc[ep.tone=='stimuli\\1000.wav', 'Condition'] = 'Standard'
ep.loc[ep.tone=='stimuli\\1000.wav', 'OnsetTime'] = ep.loc[ep.tone=='stimuli\\1000.wav', 'MainScreen.OnsetTime']

ep.loc[ep.tone=='stimuli\\1200.wav', 'Condition'] = 'Deviant'
ep.loc[ep.tone=='stimuli\\1200.wav', 'OnsetTime'] = ep.loc[ep.tone=='stimuli\\1200.wav', 'MainScreen.OnsetTime']


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
