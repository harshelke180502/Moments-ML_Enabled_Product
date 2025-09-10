"""
ML Service for generating alternative text from images.
Uses pre-trained models to automatically describe image content.
"""

import logging
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
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logging.warning("YOLO not available. Object detection will be disabled.")

logger = logging.getLogger(__name__)


class MLImageService:
    """Service for ML-powered image analysis and alternative text generation."""

    def __init__(self):
        self.caption_pipeline = None
        self.yolo_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()

    def _initialize_models(self):
        """Initialize ML models for image captioning and object detection."""
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

            # Initialize YOLO for object detection
            if YOLO_AVAILABLE:
                self.yolo_model = YOLO('yolov8n.pt')  # Use nano version for speed
                logger.info("YOLO model initialized successfully")

            logger.info("ML models initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize ML models: {e}")
            self.caption_pipeline = None
            self.yolo_model = None

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
        Detect objects in an image and return as JSON string.
        Returns a JSON string containing list of detected objects with confidence scores.
        """
        if not YOLO_AVAILABLE or not self.yolo_model:
            logger.warning("YOLO not available for object detection")
            return None

        try:
            # Run YOLO detection
            results = self.yolo_model(image_path)
            
            detected_objects = []
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        # Get class name and confidence
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = self.yolo_model.names[class_id]
                        
                        # Only include objects with confidence > 0.5
                        if confidence > 0.5:
                            detected_objects.append({
                                'name': class_name,
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
            logger.error(f"Error detecting objects: {e}")
            return None

    def is_available(self) -> bool:
        return ML_AVAILABLE and self.caption_pipeline is not None

    def is_object_detection_available(self) -> bool:
        return YOLO_AVAILABLE and self.yolo_model is not None


_ml_service: Optional[MLImageService] = None


def get_ml_service() -> MLImageService:
    global _ml_service
    if _ml_service is None:
        _ml_service = MLImageService()
    return _ml_service


def is_ml_available() -> bool:
    service = get_ml_service()
    return service.is_available()


