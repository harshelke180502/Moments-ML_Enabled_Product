# Moments - ML-Enabled Photo Sharing App

A photo sharing social networking app built with Python and Flask, enhanced with AI-powered features for automatic image description and object detection.

Demo: http://moments.helloflask.com

![Screenshot](demo.png)

## ✨ ML-Powered Features

### 🤖 AI-Powered Alternative Text Generation
- **Automatic Image Description**: When users upload photos without descriptions, AI generates meaningful alternative text
- **Enhanced Accessibility**: Improves experience for users with visual impairments
- **Smart Content Understanding**: Uses state-of-the-art vision-language models to analyze image content
- **Seamless Integration**: Works automatically in the background during photo uploads

### 🔍 AI-Powered Object Detection & Search
- **Automatic Object Detection**: Identifies objects in images using Microsoft Azure Computer Vision API
- **Smart Tagging**: Automatically creates searchable tags from detected objects
- **Enhanced Search**: Enables keyword-based image search by object types
- **Persistent Tags**: All detected tags are saved permanently for future searches

## 🚀 Complete Setup Guide

### Prerequisites
- Python 3.8 or higher
- Git
- Microsoft Azure account (for object detection features)

### Step 1: Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/harshelke180502/Moments-ML_Enabled_Product.git
cd Moments-ML_Enabled_Product/moments

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
# Install all dependencies (including ML libraries)
pip install -r requirements.txt
```

> **Note**: This will install PyTorch, Transformers, Azure SDK, and other ML dependencies. The first run will download pre-trained models (~1-2GB).

### Step 3: Database Setup

```bash
# Run database migrations for ML features
python migrate_alt_text.py
python migrate_detected_objects.py

# Initialize the application database
export FLASK_APP=app.py
flask init-app
```

<!-- To run the app -->

flask run

### Step 4: Configure Azure Computer Vision (Optional but Recommended)

For object detection features, you'll need Azure Computer Vision API credentials:

1. **Create Azure Computer Vision Resource**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a new Computer Vision resource
   - Choose F0 (Free) tier for testing

2. **Configure Environment Variables**:
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env file with your Azure credentials
   nano .env
   ```

   Add your Azure credentials:
   ```
   AZURE_COMPUTER_VISION_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   AZURE_COMPUTER_VISION_KEY=your-azure-subscription-key-here
   AZURE_OBJECT_DETECTION_ENABLED=true
   ```

### Step 5: Generate Test Data (Optional)

```bash
# Generate fake data for testing
flask lorem
```

This creates a test account:
- **Email**: `admin@helloflask.com`
- **Password**: `moments`

### Step 6: Run the Application

```bash
# Start the Flask application
flask run --port=5001
```

The application will be available at: http://localhost:5001

### Step 7: Test ML Features

```bash
# Test alternative text generation
python test_alt_text.py

# Test Azure integration (if configured)
python -c "from moments.ml_service import get_ml_service; print('Azure SDK:', get_ml_service().is_object_detection_available())"
```

## 🧪 Testing the ML Features

### Alternative Text Generation
1. Upload an image without a description
2. Check the photo sidebar for "AI Description:" with robot icon
3. The system automatically generates descriptive text

### Object Detection
1. Upload an image with objects (people, cars, animals, etc.)
2. Check the photo sidebar for "AI Detected Objects" section
3. Objects appear as badges with confidence scores
4. Search for images using object names (e.g., "person", "car")

### Search Functionality
1. Use the search bar to find images by:
   - Object types (e.g., "dog", "car", "person")
   - User descriptions
   - AI-generated alternative text
2. Browse the "Hot Tags" sidebar to see all detected objects

## 🔧 Troubleshooting

### Common Issues

**1. "ML libraries not available"**
```bash
# Reinstall ML dependencies
pip install --upgrade torch torchvision transformers
pip install azure-cognitiveservices-vision-computervision
```

**2. "Azure credentials not found"**
- Check the `.env` file has correct credentials(have not entered credentials)
- Ensure no extra spaces around `=` signs
- Restart the Flask application

**3. "Flask command not found"**
```bash
# Use python -m flask instead
python -m flask run --port=5001

# Or use the full path
./env/bin/flask run --port=5001
```

**4. Database errors**
```bash
# Reset database
rm instance/moments.db
flask init-app
python migrate_alt_text.py
python migrate_detected_objects.py
```

### Performance Notes

- **First Run**: Initial model download may take 5-10 minutes
- **Memory Usage**: ~2-3GB RAM for ML models
- **Azure API**: Free tier allows 5,000 calls/month
- **Image Size**: Recommended max 4MB for optimal performance

## 📁 Project Structure

```
moments/
├── moments/
│   ├── ml_service.py          # ML service implementation
│   ├── models.py              # Database models with ML fields
│   ├── blueprints/main.py     # Upload and search routes
│   └── templates/             # UI templates with ML features
├── requirements.txt           # All dependencies including ML
├── migrate_alt_text.py        # Database migration for alt_text
├── migrate_detected_objects.py # Database migration for objects
├── test_alt_text.py          # ML feature testing
├── AZURE_SETUP.md            # Azure configuration guide
└── .env                      # Environment variables
```

## 🎯 Features Overview

### For Users
- **Automatic Image Descriptions**: AI generates accessibility-friendly descriptions
- **Smart Object Detection**: Automatic tagging of objects in images
- **Enhanced Search**: Find images by object types and descriptions
- **Persistent Tags**: All detected objects remain searchable forever

### For Developers
- **Modular ML Service**: Easy to extend with new ML capabilities
- **Azure Integration**: Scalable cloud-based object detection
- **Local Processing**: Alternative text generation runs locally
- **Comprehensive Testing**: Built-in test scripts for ML features

## 📚 Additional Resources

- [Azure Computer Vision Setup Guide](AZURE_SETUP.md)
- [ML Features Testing](test_alt_text.py)
- [Database Migrations](migrate_alt_text.py)
- [Original Flask Book](https://helloflask.com/en/book/4)

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
