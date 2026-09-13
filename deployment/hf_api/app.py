import os
import joblib
import pandas as pd

from pathlib import Path
from flask import Flask, request, jsonify
from huggingface_hub import hf_hub_download


# ---------------------------------------------------------
# APP SETUP
# ---------------------------------------------------------

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Model information can be supplied either:
# 1. through model_repo.txt / model_output.txt
# 2. through environment variables

model_repo_file = BASE_DIR / "model_repo.txt"
model_output_file = BASE_DIR / "model_output.txt"


MODEL_REPO = (
    model_repo_file.read_text().strip()
    if model_repo_file.exists()
    else os.getenv("HF_MODEL_REPO")
)

MODEL_FILENAME = (
    model_output_file.read_text().strip()
    if model_output_file.exists()
    else os.getenv("MODEL_FILENAME")
)

HF_TOKEN = os.getenv("HF_TOKEN_ML")


if not MODEL_REPO:
    raise ValueError(
        "Model repository is not configured."
    )

if not MODEL_FILENAME:
    raise ValueError(
        "Model filename is not configured."
    )


# ---------------------------------------------------------
# MODEL INPUT FEATURES
# ---------------------------------------------------------

INPUT_COLUMNS = [
    "Age",
    "TypeofContact",
    "CityTier",
    "Occupation",
    "Gender",
    "NumberOfPersonVisiting",
    "PreferredPropertyStar",
    "MaritalStatus",
    "NumberOfTrips",
    "Passport",
    "OwnCar",
    "NumberOfChildrenVisiting",
    "Designation",
    "MonthlyIncome",
    "PitchSatisfactionScore",
    "ProductPitched",
    "NumberOfFollowups",
    "DurationOfPitch",
]


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

model_path = hf_hub_download(
    repo_id=MODEL_REPO,
    filename=MODEL_FILENAME,
    token=HF_TOKEN
)

model = joblib.load(model_path)


# Get final estimator name
if hasattr(model, "steps"):
    model_type = type(model.steps[-1][1]).__name__
    pipeline_steps = [
        name for name, _ in model.steps
    ]
else:
    model_type = type(model).__name__
    pipeline_steps = []


print(
    f"Loaded model: "
    f"{MODEL_REPO}/{MODEL_FILENAME}"
)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message":
            "Wellness Tourism Prediction API is running",
        "status": "online"
    })


# ---------------------------------------------------------
# HEALTH
# ---------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "model_repo": MODEL_REPO,
        "model_file": MODEL_FILENAME,
        "model_type": model_type,
        "input_features": len(INPUT_COLUMNS),
        "pipeline_steps": pipeline_steps
    })


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON payload received"
            }), 400


        # Validate required features
        missing_columns = [
            column
            for column in INPUT_COLUMNS
            if column not in data
        ]

        if missing_columns:

            return jsonify({
                "error":
                    "Missing required input columns",
                "missing_columns":
                    missing_columns
            }), 400


        # Preserve original training feature order
        input_df = pd.DataFrame(
            [[data[col] for col in INPUT_COLUMNS]],
            columns=INPUT_COLUMNS
        )


        # Model prediction
        prediction = int(
            model.predict(input_df)[0]
        )

        probability = float(
            model.predict_proba(input_df)[0][1]
        )


        return jsonify({
            "prediction": prediction,
            "prediction_label":
                "Likely to Purchase"
                if prediction == 1
                else "Unlikely to Purchase",
            "purchase_probability":
                round(probability, 4)
        })


    except Exception as exc:

        return jsonify({
            "error": str(exc)
        }), 500


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7860"))
    )
