#!/bin/bash
echo "Installing Azure Computer Vision dependencies..."

# Install Azure SDK packages
pip install azure-cognitiveservices-vision-computervision==0.9.0
pip install msrest==0.7.1
pip install python-dotenv==1.0.0

echo "Azure dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your Azure credentials:"
echo "   - AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/"
echo "   - AZURE_COMPUTER_VISION_KEY=your-azure-subscription-key-here"
echo "2. Restart your Flask application"
