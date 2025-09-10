"""
ML Service for generating alternative text from images and object detection.
Uses Azure Computer Vision API for object detection and local transformers for captioning.
"""

import logging
import os
from typing import Optional

try:
    from transformers import pipeline
    import torch
    from PIL import Image
    import json
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logging.warning("ML libraries not available. Alternative text generation will be disabled.")

try:
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
    from msrest.authentication import CognitiveServicesCredentials
    from dotenv import load_dotenv
    AZURE_AVAILABLE = True
    # Load environment variables
    load_dotenv()
except ImportError:
    AZURE_AVAILABLE = False
    logging.warning("Azure Computer Vision SDK not available. Object detection will be disabled.")

logger = logging.getLogger(__name__)


class MLImageService:
    """Service for ML-powered image analysis and alternative text generation."""

    def __init__(self):
        self.caption_pipeline = None
        self.azure_client = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()

    def _initialize_models(self):
        """Initialize ML models for image captioning and Azure Computer Vision."""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available. Cannot initialize models.")
            return

        try:
            logger.info(f"Initializing ML models on device: {self.device}")

            # Initialize image captioning model
            model_name = "nlpconnect/vit-gpt2-image-captioning"
            self.caption_pipeline = pipeline(
                "image-to-text",
                model=model_name,
                device=0 if self.device == "cuda" else -1,
            )

            # Initialize Azure Computer Vision client
            if AZURE_AVAILABLE:
                endpoint = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT')
                key = os.getenv('AZURE_COMPUTER_VISION_KEY')
                
                if endpoint and key:
                    credentials = CognitiveServicesCredentials(key)
                    self.azure_client = ComputerVisionClient(endpoint, credentials)
                    logger.info("Azure Computer Vision client initialized successfully")
                else:
                    logger.warning("Azure credentials not found in environment variables")
                    self.azure_client = None

            logger.info("ML models initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize ML models: {e}")
            self.caption_pipeline = None
            self.azure_client = None

    def generate_alternative_text(self, image_path: str) -> Optional[str]:
        """
        Generate alternative text description for an image.
        """
        if not ML_AVAILABLE or not self.caption_pipeline:
            logger.warning("ML service not available")
            return None

        try:
            image = Image.open(image_path).convert("RGB")
            result = self.caption_pipeline(image, max_new_tokens=50)
            if result and len(result) > 0:
                caption = result[0]["generated_text"].strip()
                logger.info(f"Generated alt text: {caption}")
                return caption
            logger.warning("No caption generated")
            return None
        except Exception as e:
            logger.error(f"Error generating alternative text: {e}")
            return None

    def detect_objects(self, image_path: str) -> Optional[str]:
        """
        Detect objects in an image using Azure Computer Vision API and return as JSON string.
        Returns a JSON string containing list of detected objects with confidence scores.
        """
        if not AZURE_AVAILABLE or not self.azure_client:
            logger.warning("Azure Computer Vision not available for object detection")
            return None

        try:
            # Read image file and pass file object to Azure API
            with open(image_path, 'rb') as image_file:
                # Call Azure Computer Vision API for object detection
                analysis = self.azure_client.analyze_image_in_stream(
                    image_file,
                    visual_features=[VisualFeatureTypes.objects]
                )
            
            detected_objects = []
            
            # Debug: Log the analysis response structure
            logger.info(f"Azure analysis response type: {type(analysis)}")
            logger.info(f"Azure analysis attributes: {dir(analysis)}")
            
            # Extract objects from Azure response
            if hasattr(analysis, 'objects') and analysis.objects:
                logger.info(f"Found {len(analysis.objects)} objects in Azure response")
                for i, obj in enumerate(analysis.objects):
                    logger.info(f"Object {i}: type={type(obj)}, attributes={dir(obj)}")
                for obj in analysis.objects:
                    # Azure Computer Vision API returns objects with different property names
                    if hasattr(obj, 'object') and hasattr(obj, 'confidence'):
                        object_name = obj.object
                        confidence = obj.confidence
                    elif hasattr(obj, 'object_property') and hasattr(obj, 'confidence'):
                        object_name = obj.object_property
                        confidence = obj.confidence
                    else:
                        # Try to get object name from other possible attributes
                        object_name = getattr(obj, 'name', getattr(obj, 'label', 'unknown'))
                        confidence = getattr(obj, 'confidence', 0.0)
                    
                    # Only include objects with confidence > 0.5
                    if confidence > 0.5:
                        detected_objects.append({
                            'name': object_name,
                            'confidence': round(confidence, 2)
                        })
            
            # Remove duplicates and sort by confidence
            unique_objects = {}
            for obj in detected_objects:
                name = obj['name']
                if name not in unique_objects or obj['confidence'] > unique_objects[name]['confidence']:
                    unique_objects[name] = obj
            
            final_objects = list(unique_objects.values())
            final_objects.sort(key=lambda x: x['confidence'], reverse=True)
            
            if final_objects:
                objects_json = json.dumps(final_objects)
                logger.info(f"Detected objects: {[obj['name'] for obj in final_objects]}")
                return objects_json
            else:
                logger.info("No objects detected with sufficient confidence")
                return None
                
        except Exception as e:
            logger.error(f"Error detecting objects with Azure: {e}")
            return None

    def is_available(self) -> bool:
        return ML_AVAILABLE and self.caption_pipeline is not None

    def is_object_detection_available(self) -> bool:
        return AZURE_AVAILABLE and self.azure_client is not None


_ml_service: Optional[MLImageService] = None


def get_ml_service() -> MLImageService:
    global _ml_service
    if _ml_service is None:
        _ml_service = MLImageService()
    return _ml_service


def is_ml_available() -> bool:
    service = get_ml_service()
    return service.is_available()


