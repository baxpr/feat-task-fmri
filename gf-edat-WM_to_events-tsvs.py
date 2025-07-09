#!/usr/bin/env python

import ast
import collections
import os
import pandas
import scipy

gf_edat_summary_csv = 'INPUTS/eprime_summary_WM.csv'
confounds_tsv = 'INPUTS/desc-confounds_timeseries.tsv'
out_dir = 'OUTPUTS'

inputs_dir = os.path.join(out_dir, 'feat_inputs')
os.makedirs(design_dir, exist_ok=True)

edat = pandas.read_csv(gf_edat_summary_csv)

# Convert the peculiar gf-edat event output format to list of onsets/durations and sort
info = ''
for x in edat.itertuples():
    onsets = ast.literal_eval(x.OnsetsSec)
    durations = ast.literal_eval(x.DurationsSec)
    accuracy = ast.literal_eval(x.Accuracy)
    blocktype = [x.BlockType for y in onsets]
    stimtype = [x.StimType for y in onsets]
    condition = [x.Condition for y in onsets]
    paramod = [1 for y in onsets]
    y = pandas.DataFrame( 
        zip(blocktype, stimtype, condition, onsets, durations, accuracy, paramod),
        columns=['BlockType', 'StimType', 'Condition', 'OnsetSec', 'DurationSec', 'Accuracy', 'ParaMod']
        )
    if isinstance(info, pandas.DataFrame):
        info = pandas.concat([info, y])
    else:
        info = y
info = info.sort_values('OnsetSec')

# Drop error trials
#info = info.loc[info.Accuracy==1,:]

# Save events file for each condition
for c in set(info.Condition):
    efile = os.path.join(inputs_dir, f'events_{c}.tsv')
    rows = info.loc[info.Condition==c,:]
    rows.to_csv(
        efile, 
        sep='\t', 
        columns=['OnsetSec', 'DurationSec', 'ParaMod'], 
        header=False, 
        index=False, 
        )

# Save mot params for confounds
conf = pandas.read_csv(confounds_tsv, sep='\t')
mot = conf[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
mot = mot.apply(scipy.stats.zscore, nan_policy='omit')
mot.to_csv(
    os.path.join(inputs_dir, 'confounds.tsv'), 
    sep='\t', 
    header=False, 
    index=False, 
    )
