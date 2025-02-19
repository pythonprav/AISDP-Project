# Define storage path (modify if needed)
STORAGE_PATH=~/wine-quality

# Create directory if it doesn't exist
if [ ! -d "$STORAGE_PATH" ]; then
    echo "Creating storage directory at $STORAGE_PATH..."
    mkdir -p $STORAGE_PATH
fi

# Copy dataset files to the storage directory
echo "Copying volume files to $STORAGE_PATH..."
cp -r volumes/* $STORAGE_PATH/

echo "Storage setup complete!"
