#!/usr/bin/env bash
#
# For MNI space fmriprep processed fmri as inputs to feat, we need to add 
# a couple of files with registration info since registration is not
# performed at the first level.
#
# We will use the fmriprep mean fmri as the "standard" to avoid transformation
# issues. This means all participants must have the same voxel grid and 
# positions in the fmriprep for a group analysis to work.
#
# https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=fsl;a779b3b8.1408

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in      
        --feat_dir)       export feat_dir="$2";       shift; shift ;;
        --std_niigz)      export std_niigz="$2";       shift; shift ;;
        *) echo "Input ${1} not recognized"; shift ;;
    esac
done

# Reg dir shouldn't be present, so create it
mkdir "${feat_dir}"/reg

# One file is just the standard space T1
#std_niigz=$(grep 'set fmri(regstandard)' "${feat_dir}"/design.fsf | cut -d '"' -f 2).nii.gz
cp "${std_niigz}" "${feat_dir}"/reg/standard.nii.gz

# Then we need identity transform between feat space and standard space
cp "${FSLDIR}"/etc/flirtsch/ident.mat "${feat_dir}"/reg/example_func2standard.mat
cp "${FSLDIR}"/etc/flirtsch/ident.mat "${feat_dir}"/reg/standard2example_func.mat
