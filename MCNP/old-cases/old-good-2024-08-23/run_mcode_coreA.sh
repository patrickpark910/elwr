#!/bin/bash

# Function to run dos2unix and mcode12 commands in a directory
process_directory() {
    local dir=$1
    local input_file=$2
    local log_file=$3

    echo "Processing directory: $dir" | tee -a "$log_file"
    
    # Navigate to the directory
    cd "$dir" || exit

    # Convert all files to Unix format
    echo "Converting files to Unix format..." | tee -a "$log_file"
    dos2unix ** >> "$log_file" 2>&1

    # Run the mcode12 command
    echo "Running MCODE12 for input file: $input_file" | tee -a "$log_file"
    nohup /home/patrick/MCODE12/mcode12 "$input_file" >> "$log_file" 2>&1

    echo "Completed processing for $dir" | tee -a "$log_file"
    echo "---------------------------------------" | tee -a "$log_file"
}

# Define directories and input files
declare -a directories=(
    "/home/patrick/A-cladSS-clean"
#    "/home/patrick/A-cladSS-Li0_1mg"
#    "/home/patrick/A-cladSS-Li01mg"
#    "/home/patrick/A-cladSS-Li05mg"
    "/home/patrick/A-cladSS-Li10mg"
    "/home/patrick/A-cladSS-Li15mg"
    "/home/patrick/A-cladZr-clean"
    "/home/patrick/A-cladZr-Li0_1mg"
    "/home/patrick/A-cladZr-Li01mg"
    "/home/patrick/A-cladZr-Li05mg"
    "/home/patrick/A-cladZr-Li10mg"
    "/home/patrick/A-cladZr-Li15mg"
)

declare -a input_files=(
    "elwr-coreA-cladSS-clean.mcode.inp"
#    "elwr-coreA-cladSS-Li0_1mg.mcode.inp"
#    "elwr-coreA-cladSS-Li01mg.mcode.inp"
#    "elwr-coreA-cladSS-Li05mg.mcode.inp"
    "elwr-coreA-cladSS-Li10mg.mcode.inp"
    "elwr-coreA-cladSS-Li15mg.mcode.inp"
    "elwr-coreA-cladZr-clean.mcode.inp"
    "elwr-coreA-cladZr-Li0_1mg.mcode.inp"
    "elwr-coreA-cladZr-Li01mg.mcode.inp"
    "elwr-coreA-cladZr-Li05mg.mcode.inp"
    "elwr-coreA-cladZr-Li10mg.mcode.inp"
    "elwr-coreA-cladZr-Li15mg.mcode.inp"
)

# Log file location
log_file="/home/patrick/mcode12_execution.log"

# Clear previous log file
echo "Starting MCODE12 execution at $(date)" > "$log_file"

# Iterate over directories and input files
for i in "${!directories[@]}"; do
    process_directory "${directories[i]}" "${input_files[i]}" "$log_file"
done

echo "All processes have been executed. Please check the log file for details: $log_file"
