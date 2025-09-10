# Azure Computer Vision Integration Setup

This guide will help you set up Microsoft Azure Computer Vision API for object detection in your Moments application.

## Prerequisites

1. **Azure Account**: You need an active Azure subscription
2. **Computer Vision Resource**: Create a Computer Vision resource in Azure Portal

## Step 1: Create Azure Computer Vision Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Computer Vision" and select it
4. Click "Create"
5. Fill in the required details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a region close to you
   - **Name**: Give your resource a unique name
   - **Pricing Tier**: Choose F0 (Free) for testing or S1 (Standard) for production
6. Click "Review + create" then "Create"

## Step 2: Get Your Credentials

1. Go to your Computer Vision resource in Azure Portal
2. Click on "Keys and Endpoint" in the left menu
3. Copy:
   - **Key 1** (or Key 2)
   - **Endpoint** URL

## Step 3: Configure Your Application

1. **Edit the .env file** in your project root:
   ```bash
   nano .env
   ```

2. **Update the credentials**:
   ```
   AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   AZURE_COMPUTER_VISION_KEY=your-actual-key-here
   AZURE_OBJECT_DETECTION_ENABLED=true
   ```

3. **Install Azure dependencies**:
   ```bash
   ./install_azure_deps.sh
   ```

## Step 4: Test the Integration

1. **Start your Flask application**:
   ```bash
   source env/bin/activate
   export FLASK_APP=app.py
   flask run --port=5001
   ```

2. **Upload an image** and check the logs for:
   - "Azure Computer Vision client initialized successfully"
   - "Detected objects: [list of objects]"

## Troubleshooting

### Common Issues:

1. **"Azure credentials not found"**:
   - Check your .env file has the correct variable names
   - Ensure no extra spaces around the = sign
   - Restart your Flask application after editing .env

2. **"Azure Computer Vision SDK not available"**:
   - Run: `pip install azure-cognitiveservices-vision-computervision`
   - Check your virtual environment is activated

3. **API Errors**:
   - Verify your endpoint URL is correct
   - Check your subscription key is valid
   - Ensure your Azure resource is active

### Cost Management:

- **Free Tier (F0)**: 20 calls per minute, 5,000 calls per month
- **Standard Tier (S1)**: 10 calls per second, pay per transaction
- Monitor usage in Azure Portal under "Metrics"

## Features

With Azure Computer Vision integration, your application now:

✅ **Detects objects** in uploaded images using Microsoft's AI
✅ **Creates tags automatically** from detected objects
✅ **Enables search** by object types (person, car, dog, etc.)
✅ **Persists tags forever** for future image searches
✅ **Shows latest detected tags** in the Hot Tags sidebar

## API Limits

- **Free Tier**: 20 requests/minute, 5,000 requests/month
- **Standard Tier**: 10 requests/second, pay per transaction
- **Image Size**: Max 4MB, recommended 1024x768 or smaller
- **Supported Formats**: JPEG, PNG, GIF, BMP

