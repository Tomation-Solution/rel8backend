#!/bin/bash

# Simple Cloudinary Migration Script
# This script runs the Cloudinary migration process with user prompts between stages

# Path to Django manage.py
MANAGE_PY="./manage.py"

# Progress tracking file
PROGRESS_FILE="cloudinary_migration_progress.txt"

# Models and their image fields to migrate
MODELS_AND_FIELDS=(

)

# Function to run Django management command
run_command() {
    echo "Running: python $MANAGE_PY $1 ${@:2}"
    python "$MANAGE_PY" "$1" "${@:2}"
    return $?
}

# Function to prompt user to continue
prompt_continue() {
    echo
    read -p "Press Enter to continue or Ctrl+C to exit..."
    echo
}

# Function to save progress
save_progress() {
    echo "$1" > "$PROGRESS_FILE"
}

# Function to load progress
load_progress() {
    if [ -f "$PROGRESS_FILE" ]; then
        cat "$PROGRESS_FILE"
    else
        echo "start"
    fi
}

# Main script
echo "=== Cloudinary Migration Tool ==="
echo "This script will help you migrate images from one Cloudinary account to another."
echo "You can exit at any point and resume later by running the script again."
echo

# Load the current progress
CURRENT_STAGE=$(load_progress)
echo "Current progress: $CURRENT_STAGE"
echo

# Step 0: Initialize migration
if [ "$CURRENT_STAGE" = "start" ]; then
    echo "=== STEP 0: INITIALIZING MIGRATION ==="
    echo "This step will initialize the migration environment."

    for model_field in "${MODELS_AND_FIELDS[@]}"; do
        # Split the model_field string
        IFS=':' read -r model field <<< "$model_field"

        echo "Initializing migration for $model"
        run_command "cloudinary_migration" "init" "$model"
    done

    save_progress "collect"
    echo "Initialization complete for all models."
    prompt_continue
fi

# Step 1: Collect URLs from models
if [ "$CURRENT_STAGE" = "collect" ]; then
    echo "=== STEP 1: COLLECTING URLS ==="
    
    for model_field in "${MODELS_AND_FIELDS[@]}"; do
        # Split the model_field string
        IFS=':' read -r model field <<< "$model_field"
        
        echo "Collecting URLs from $model ($field)"
        run_command "cloudinary_migration" "collect-model" "$model" "$field"
        echo "Collection completed for $model"
        echo
    done
    
    save_progress "migrate"
    echo "URL collection complete for all models."
    prompt_continue
fi

# Step 2: Migrate batches
if [ "$CURRENT_STAGE" = "migrate" ]; then
    echo "=== STEP 2: MIGRATING IMAGES ==="

    for model_field in "${MODELS_AND_FIELDS[@]}"; do
        # Split the model_field string
        IFS=':' read -r model field <<< "$model_field"

        echo "Starting migration for $model"
        
        # Convert model path for state file lookup
        model_state_prefix=$(echo "$model" | tr '.' '_')
        state_file="${model_state_prefix}_migration_state.json"

        # Check if the state file exists
        if [ ! -f "$state_file" ]; then
            echo "Warning: State file for $model not found. Skipping."
            continue
        fi

        # Keep migrating batches until completed
        status="in_progress"
        batch_count=0

        while [ "$status" != "completed" ]; do
            batch_count=$((batch_count + 1))
            echo "Processing batch #$batch_count for $model"

            # Run the migration batch
            run_command "cloudinary_migration" "migrate-batch" "$model"

            # Check the status from the state file
            if [ -f "$state_file" ]; then
                status=$(grep -o '"status": *"[^"]*"' "$state_file" | cut -d'"' -f4)
                echo "Current status: $status"
            else
                echo "Warning: State file disappeared. Assuming completed."
                status="completed"
            fi

            # Ask to continue after each batch
            echo "Batch #$batch_count for $model completed."
        done

        echo "Migration completed for $model"
        echo
    done

    save_progress "update"
    echo "Image migration complete for all models."
    prompt_continue
fi

# Step 3: Update models
if [ "$CURRENT_STAGE" = "update" ]; then
    echo "=== STEP 3: UPDATING MODEL INSTANCES ==="
    
    for model_field in "${MODELS_AND_FIELDS[@]}"; do
        # Split the model_field string
        IFS=':' read -r model field <<< "$model_field"
        
        echo "Updating model instances for $model"
        run_command "cloudinary_migration" "update-models" "$model"
        echo "Model update completed for $model"
        echo
    done
    
    save_progress "cleanup"
    echo "Model updates complete for all models."
    prompt_continue
fi

# Step 4: Cleanup
if [ "$CURRENT_STAGE" = "cleanup" ]; then
    echo "=== STEP 4: CLEANING UP ==="
    echo "Cleaning up temporary files"
    run_command "cloudinary_migration" "cleanup"
    
    save_progress "completed"
    echo "Cleanup completed."
    echo
fi

# Final message
if [ "$CURRENT_STAGE" = "completed" ] || [ "$(load_progress)" = "completed" ]; then
    echo "=== MIGRATION COMPLETED ==="
    echo "The Cloudinary migration process has been completed successfully."
    # Reset progress file for future runs
    rm -f "$PROGRESS_FILE"
else
    echo "=== MIGRATION IN PROGRESS ==="
    echo "Current progress: $(load_progress)"
    echo "Run this script again to continue from this point."
fi

echo
echo "Thank you for using the Cloudinary Migration Tool."