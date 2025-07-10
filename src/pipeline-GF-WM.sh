#!/usr/bin/env bash
#
# Main entrypoint for FSL/FEAT first level stats for GF WM task
#
# All input files must have fully specified paths

# Parse input options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in      
        --eprime_txt)         export eprime_txt="$2";       shift; shift ;;
        --fmriprep_dir)       export fmriprep_dir="$2";     shift; shift ;;
        --out_dir)            export out_dir="$2";          shift; shift ;;
        *) echo "Input ${1} not recognized"; shift ;;
    esac
done

# Where to put FEAT inputs
feat_dir="${out_dir}/feat-GF-WM"
mkdir -p "${feat_dir}"

# Find preprocessed fmri, brain mask, and confounds tsv in fmriprep dir
echo Finding fmriprep files
fmri_niigz=$(find_fmriprep.py --fmriprep_dir ${fmriprep_dir} --output fmri)
mask_niigz=$(find_fmriprep.py --fmriprep_dir ${fmriprep_dir} --output mask)
confounds_tsv=$(find_fmriprep.py --fmriprep_dir ${fmriprep_dir} --output confounds)

# Convert eprime .txt log to csv format
echo Converting eprime log
eprime_to_csv.py -o "${out_dir}"/eprime.csv "${eprime_txt}"

# Convert fmri timings to FEAT format
echo Parsing eprime timings
parse-edat-GF-WM.py --eprime_csv "${out_dir}"/eprime.csv --feat_dir "${feat_dir}"

# Extract desired confounds from confounds file
echo Extracting confounds
extract_confounds.py --confounds_tsv "${confounds_tsv}" --feat_dir "${feat_dir}"

# Copy input images to feat dir. Filenames are hard coded in design template fsf
echo Copying images
cp "${fmri_niigz}" "${feat_dir}"/fmri.nii.gz
cp "${mask_niigz}" "${feat_dir}"/mask.nii.gz

# Update the FEAT design file with input directory name. Assume our template
# is in the same dir as this script
echo Creating design file
src_dir=$(dirname "${BASH_SOURCE[0]}")
sed -e "s:SUBJDIR:${feat_dir}:g" "${src_dir}"/design-template-GF-WM.fsf > "${feat_dir}"/design.fsf

# Verify that TR, nvols in design file match the fmri nifti
echo Checking design file params
check-tr-vols.py --design_fsf "${feat_dir}"/design.fsf

# Run the fmri
echo Running FEAT
cd "${feat_dir}"
feat design.fsf


