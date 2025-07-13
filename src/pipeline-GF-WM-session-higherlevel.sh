#!/usr/bin/env bash
#
# Main entrypoint for FSL/FEAT higher level stats for GF WM task - take mean
# of two runs of the task with fixed effects model
#
# All input files must have fully specified paths

# Parse input options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in      
        --wm1feat_dir)       export wm1feat_dir="$2";     shift; shift ;;
        --wm2feat_dir)       export wm2feat_dir="$2";     shift; shift ;;
        --out_dir)           export out_dir="$2";         shift; shift ;;
        *) echo "Input ${1} not recognized"; shift ;;
    esac
done

# Update the FEAT design file directory names. Assume our template
# is in the same dir as this script
echo Creating design file
src_dir=$(dirname "${BASH_SOURCE[0]}")
sed -e "s:WM1DIR:${wm1feat_dir}:g" "${src_dir}"/design-template-GF-WM-session-higherlevel.fsf \
    > "${out_dir}"/design.fsf
sed -i "" -e "s:WM2DIR:${wm2feat_dir}:g" "${out_dir}"/design.fsf
sed -i "" -e "s:OUTDIR:${out_dir}/GF-WM-12:g" "${out_dir}"/design.fsf

# Run
echo Running FEAT
cd "${out_dir}"
feat design.fsf

# Copy html to a different location to be a separate output
mkdir "${out_dir}"/HTML
cp -R "${feat_dir}"/GF-WM-12.feat/*.html "${out_dir}"/HTML
cp -R "${feat_dir}"/GF-WM-12.feat/*.png "${out_dir}"/HTML
cp -R "${feat_dir}"/GF-WM-12.feat/.files "${out_dir}"/HTML
