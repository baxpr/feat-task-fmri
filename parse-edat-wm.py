#!/usr/bin/env python
#
# Get WM task timings from eprime csv created by eprime_to_csv.py

import argparse
import math
import pandas

parser = argparse.ArgumentParser()
parser.add_argument('--eprime_csv', required=True)
args = parser.parse_args()

ep = pandas.read_csv(args.eprime_csv)

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
rows = [x in ['TRSyncPROC', 'TrialsPROC'] for x in ep.Procedure]

# Reduce the table
ep = ep.loc[rows,cols]

# Find fmri start time
starttime = [x for x in ep['GetReady.OffsetTime'] if not math.isnan(x)]
if len(starttime) != 1:
    raise Exception('Wrong number of starttime found')

# Compute stimulus timings in seconds relative to fmri start


