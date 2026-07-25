import json
import logging
from pathlib import Path

import joblib

from app.core.config import settings
from app.schemas.prediction import PredictionRequest
from app.services.preprocessing import request_to_dataframe

logger = logging.getLogger(__name__)


class InferenceService:
    """
    Holds the loaded model pipeline and the set of known locations.
    Instantiated once at app startup (see app/main.py lifespan) so the
    .pkl is not re-read from disk on every request.
    """

    def __init__(self) -> None:
        self.model = None
        self.known_locations: set[str] = set()

    def load(self) -> None:
        model_path = Path(settings.MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. "
                "Copy house_price.pkl from the notebook's output into backend/models/."
            )
        self.model = joblib.load(model_path)
        logger.info("Loaded model from %s", model_path)

        locations_path = Path(settings.LOCATIONS_PATH)
        if locations_path.exists():
            with open(locations_path) as f:
                self.known_locations = set(json.load(f))
            logger.info("Loaded %d known locations", len(self.known_locations))
        else:
            logger.warning("locations.json not found at %s; all locations will map to 'other'", locations_path)

    def predict(self, payload: PredictionRequest) -> float:
        if self.model is None:
            raise RuntimeError("Model is not loaded yet")
        df = request_to_dataframe(payload, self.known_locations)
        prediction = self.model.predict(df)[0]
        return float(prediction)


inference_service = InferenceService()
