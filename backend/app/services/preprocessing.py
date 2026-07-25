import pandas as pd

from app.schemas.prediction import PredictionRequest

# Must exactly match the column names used when training the pipeline
# in notebooks/house_price_model.ipynb (section 2.4).
NUMERIC_FEATURES = ["carpet_area_sqft", "floor_num", "bathroom", "balcony"]
CATEGORICAL_FEATURES = ["location_grouped", "Furnishing", "Transaction", "Ownership", "facing"]


def request_to_dataframe(payload: PredictionRequest, known_locations: set[str]) -> pd.DataFrame:
    """
    Turn a single prediction request into a one-row DataFrame with exactly
    the column names the training pipeline expects. The fitted Pipeline
    (loaded from house_price.pkl) already contains the imputer, scaler and
    one-hot encoder, so no manual encoding is needed here -- we just need
    to hand it a DataFrame shaped like the training data.
    """
    location = payload.location if payload.location in known_locations else "other"

    row = {
        "carpet_area_sqft": payload.carpet_area_sqft,
        "floor_num": payload.floor_num,
        "bathroom": payload.bathroom,
        "balcony": payload.balcony,
        "location_grouped": location,
        "Furnishing": payload.furnishing,
        "Transaction": payload.transaction,
        "Ownership": payload.ownership,
        "facing": payload.facing,
    }

    return pd.DataFrame([row], columns=NUMERIC_FEATURES + CATEGORICAL_FEATURES)
