#!/usr/bin/env bash

# Replace the string SUBJDIR in an FSL FEAT design.fsf file with a 
# subject-specific dir (fully specified path). No spaces can exist 
# in the dir or filenames.

subjdir="/INPUTS"

sed -e "s/SUBJDIR/${subjdir}/g" design-template.fsf > design-subj.fsf
