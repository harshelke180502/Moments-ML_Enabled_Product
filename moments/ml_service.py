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
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logging.warning("ML libraries not available. Alternative text generation will be disabled.")

logger = logging.getLogger(__name__)


class MLImageService:
    """Service for ML-powered image analysis and alternative text generation."""

    def __init__(self):
        self.caption_pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()

    def _initialize_models(self):
        """Initialize ML models for image captioning."""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available. Cannot initialize models.")
            return

        try:
            logger.info(f"Initializing ML models on device: {self.device}")

            model_name = "nlpconnect/vit-gpt2-image-captioning"

            self.caption_pipeline = pipeline(
                "image-to-text",
                model=model_name,
                device=0 if self.device == "cuda" else -1,
            )

            logger.info("ML models initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize ML models: {e}")
            self.caption_pipeline = None

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

    def is_available(self) -> bool:
        return ML_AVAILABLE and self.caption_pipeline is not None


_ml_service: Optional[MLImageService] = None


def get_ml_service() -> MLImageService:
    global _ml_service
    if _ml_service is None:
        _ml_service = MLImageService()
    return _ml_service


def is_ml_available() -> bool:
    service = get_ml_service()
    return service.is_available()


