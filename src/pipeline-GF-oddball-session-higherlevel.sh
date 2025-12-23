#!/usr/bin/env bash
#
# Main entrypoint for FSL/FEAT higher level stats for GF Oddball task - take mean
# of two runs of the task with fixed effects model
#
# All input files must have fully specified paths

# Parse input options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in      
        --oddball1feat_dir)       export oddball1feat_dir="$2";     shift; shift ;;
        --oddball2feat_dir)       export oddball2feat_dir="$2";     shift; shift ;;
        --out_dir)                export out_dir="$2";              shift; shift ;;
        *) echo "Input ${1} not recognized"; shift ;;
    esac
done

# Update the FEAT design file directory names. Assume our template
# is in the same dir as this script
echo Creating design file
src_dir=$(dirname "${BASH_SOURCE[0]}")
sed -e "s:ODDBALL1DIR:${oddball1feat_dir}:g" "${src_dir}"/design-template-GF-oddball-session-higherlevel.fsf \
    > "${out_dir}"/design.fsf
sed -i -e "s:ODDBALL2DIR:${oddball2feat_dir}:g" "${out_dir}"/design.fsf
sed -i -e "s:OUTDIR:${out_dir}/GF-oddball-12:g" "${out_dir}"/design.fsf

# Run
echo Running FEAT
cd "${out_dir}"
feat design.fsf
