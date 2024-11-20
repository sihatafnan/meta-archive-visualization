#!/bin/bash

# Define the list of Python scripts
scripts=(
    "2fa.py"
    "advertisers_targeting.py"
    "off_facebook_activity.py"
    "currently_logged_in.py"
)

# Loop through each script and execute
echo "Starting analysis pipeline..."
for script in "${scripts[@]}"
do
    echo "Running $script..."
    python3 "$script"
    if [ $? -ne 0 ]; then
        echo "Error: $script failed to execute properly."
        exit 1
    fi
done

echo "All scripts executed successfully!"
