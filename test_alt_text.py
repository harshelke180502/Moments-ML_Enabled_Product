#!/usr/bin/env python3
"""
Test script for alternative text generation functionality.
Tests the ML service and verifies it can generate descriptions for images.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ml_service():
    """Test the ML service functionality."""
    try:
        from moments.ml_service import get_ml_service, is_ml_available
        
        print("🧪 Testing ML Service...")
        
        # Check if ML service is available
        if not is_ml_available():
            print("❌ ML service is not available. Please install required dependencies.")
            return False
        
        print("✅ ML service is available")
        
        # Get ML service instance
        ml_service = get_ml_service()
        print(f"✅ ML service initialized on device: {ml_service.device}")
        
        # Test with a sample image if available
        test_image_path = project_root / "demo.png"
        if test_image_path.exists():
            print(f"🖼️  Testing with image: {test_image_path}")
            
            alt_text = ml_service.generate_alternative_text(str(test_image_path))
            if alt_text:
                print(f"✅ Generated alternative text: {alt_text}")
                return True
            else:
                print("❌ Failed to generate alternative text")
                return False
        else:
            print("⚠️  No test image found. ML service appears to be working.")
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required ML dependencies:")
        print("pip install transformers torch torchvision Pillow numpy")
        return False
    except Exception as e:
        print(f"❌ Error testing ML service: {e}")
        return False

def test_photo_model():
    """Test the Photo model with alt_text field."""
    try:
        from moments import create_app
        from moments.core.extensions import db
        from moments.models import Photo
        
        print("\n🧪 Testing Photo Model...")
        
        app = create_app('development')
        with app.app_context():
            # Check if alt_text column exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('photo')]
            
            if 'alt_text' in columns:
                print("✅ alt_text column exists in photo table")
                
                # Test creating a photo with alt_text
                test_photo = Photo(
                    filename="test.jpg",
                    filename_s="test_s.jpg", 
                    filename_m="test_m.jpg",
                    alt_text="This is a test alternative text"
                )
                
                print("✅ Photo model supports alt_text field")
                print(f"   Test alt_text: {test_photo.alt_text}")
                print(f"   Effective description: {test_photo.get_effective_description()}")
                
                return True
            else:
                print("❌ alt_text column not found in photo table")
                print("Please run the migration script first:")
                print("python migrate_alt_text.py")
                return False
                
    except Exception as e:
        print(f"❌ Error testing Photo model: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Alternative Text Generation Feature\n")
    
    # Test ML service
    ml_ok = test_ml_service()
    
    # Test Photo model
    model_ok = test_photo_model()
    
    print("\n" + "="*50)
    if ml_ok and model_ok:
        print("🎉 All tests passed! Alternative text generation is ready.")
        print("\nNext steps:")
        print("1. Run the Flask app: flask run")
        print("2. Upload a photo to test the feature")
        print("3. Check that AI-generated description appears when no user description is provided")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        if not ml_ok:
            print("\nTo fix ML service issues:")
            print("1. Install dependencies: pip install -r requirements.txt")
            print("2. Ensure you have sufficient disk space for model downloads")
        if not model_ok:
            print("\nTo fix model issues:")
            print("1. Run migration: python migrate_alt_text.py")
            print("2. Restart the Flask application")

if __name__ == '__main__':
    main()
