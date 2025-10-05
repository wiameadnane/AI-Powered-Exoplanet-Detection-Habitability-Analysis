#!/bin/bash

echo "Installing required packages for Exoplanet Detection..."
echo

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not available. Please install Python with pip."
    exit 1
fi

echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "✅ All packages installed successfully!"
    echo "You can now run the Jupyter notebook."
else
    echo
    echo "❌ Some packages failed to install."
    echo "Please check the error messages above."
    exit 1
fi
