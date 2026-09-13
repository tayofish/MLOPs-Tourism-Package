
import os
import requests
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Tourism Wellness Package Prediction",
    page_icon="🌍",
    layout="wide"
)


# ---------------------------------------------------------
# API CONFIGURATION
# ---------------------------------------------------------

API_URL = os.getenv(
    "PREDICTION_API_URL"
)

if not API_URL:

    st.error(
        "Prediction API URL is not configured."
    )

    st.stop()


API_URL = API_URL.rstrip("/")

PREDICT_URL = f"{API_URL}/predict"
HEALTH_URL = f"{API_URL}/health"


# ---------------------------------------------------------
# API HELPERS
# ---------------------------------------------------------

def get_model_info():
    """Retrieve deployed model information."""

    try:

        response = requests.get(
            HEALTH_URL,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        return None


def get_prediction(payload):
    """Send customer data to prediction API."""

    response = requests.post(
        PREDICT_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title(
    "🌍 Tourism Prediction"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Prediction",
        "Model Information"
    ]
)


# =========================================================
# PREDICTION PAGE
# =========================================================

if page == "Prediction":

    st.title(
        "🌍 Wellness Tourism Package Prediction"
    )

    st.caption(
        "Enter customer information to estimate "
        "the likelihood of purchasing the package."
    )

    st.divider()


    # -----------------------------------------------------
    # CUSTOMER PROFILE
    # -----------------------------------------------------

    st.subheader(
        "Customer Profile"
    )

    col1, col2 = st.columns(2)


    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=35
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        marital_status = st.selectbox(
            "Marital Status",
            [
                "Single",
                "Married",
                "Divorced",
                "Unmarried"
            ]
        )


    with col2:

        occupation = st.selectbox(
            "Occupation",
            [
                "Salaried",
                "Small Business",
                "Large Business",
                "Free Lancer"
            ]
        )

        designation = st.selectbox(
            "Designation",
            [
                "Executive",
                "Manager",
                "Senior Manager",
                "AVP",
                "VP"
            ]
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            value=25000.0,
            step=1000.0
        )


    st.divider()


    # -----------------------------------------------------
    # TRAVEL & HOUSEHOLD
    # -----------------------------------------------------

    st.subheader(
        "Travel & Household"
    )

    col1, col2 = st.columns(2)


    with col1:

        city_tier_label = st.selectbox(
            "City Tier",
            [
                "Tier 1",
                "Tier 2",
                "Tier 3"
            ]
        )

        city_tier = {
            "Tier 1": 1,
            "Tier 2": 2,
            "Tier 3": 3
        }[city_tier_label]


        number_trips = st.number_input(
            "Number of Trips",
            min_value=0,
            max_value=50,
            value=2
        )


        passport_label = st.selectbox(
            "Passport",
            [
                "No",
                "Yes"
            ]
        )

        passport = (
            1
            if passport_label == "Yes"
            else 0
        )


    with col2:

        persons_visiting = st.number_input(
            "Number of Persons Visiting",
            min_value=1,
            max_value=20,
            value=2
        )


        children_visiting = st.number_input(
            "Number of Children Visiting",
            min_value=0,
            max_value=10,
            value=0
        )


        own_car_label = st.selectbox(
            "Own Car",
            [
                "No",
                "Yes"
            ]
        )

        own_car = (
            1
            if own_car_label == "Yes"
            else 0
        )


    st.divider()


    # -----------------------------------------------------
    # SALES & PACKAGE
    # -----------------------------------------------------

    st.subheader(
        "Sales & Package Information"
    )

    col1, col2 = st.columns(2)


    with col1:

        contact_type = st.selectbox(
            "Type of Contact",
            [
                "Self Enquiry",
                "Company Invited"
            ]
        )


        product_pitched = st.selectbox(
            "Product Pitched",
            [
                "Basic",
                "Standard",
                "Deluxe",
                "Super Deluxe",
                "King"
            ]
        )


        duration_pitch = st.number_input(
            "Duration of Pitch (minutes)",
            min_value=0,
            max_value=120,
            value=15
        )


    with col2:

        followups = st.number_input(
            "Number of Follow-ups",
            min_value=0,
            max_value=20,
            value=3
        )


        satisfaction = st.slider(
            "Pitch Satisfaction Score",
            min_value=1,
            max_value=5,
            value=3
        )


        property_star = st.slider(
            "Preferred Property Star",
            min_value=1,
            max_value=5,
            value=3
        )


    st.divider()


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    if st.button(
        "Predict Purchase",
        type="primary",
        use_container_width=True
    ):

        payload = {

            "Age":
                age,

            "TypeofContact":
                contact_type,

            "CityTier":
                city_tier,

            "Occupation":
                occupation,

            "Gender":
                gender,

            "NumberOfPersonVisiting":
                persons_visiting,

            "PreferredPropertyStar":
                property_star,

            "MaritalStatus":
                marital_status,

            "NumberOfTrips":
                number_trips,

            "Passport":
                passport,

            "OwnCar":
                own_car,

            "NumberOfChildrenVisiting":
                children_visiting,

            "Designation":
                designation,

            "MonthlyIncome":
                monthly_income,

            "PitchSatisfactionScore":
                satisfaction,

            "ProductPitched":
                product_pitched,

            "NumberOfFollowups":
                followups,

            "DurationOfPitch":
                duration_pitch
        }


        try:

            with st.spinner(
                "Generating prediction..."
            ):

                result = get_prediction(
                    payload
                )


            prediction = result[
                "prediction"
            ]

            probability = result[
                "purchase_probability"
            ]


            st.divider()


            if prediction == 1:

                st.success(
                    "Customer is likely to purchase "
                    "the tourism package."
                )

            else:

                st.warning(
                    "Customer is unlikely to purchase "
                    "the tourism package."
                )


            col1, col2 = st.columns(2)


            col1.metric(
                "Prediction",
                result.get(
                    "prediction_label",
                    prediction
                )
            )


            col2.metric(
                "Purchase Probability",
                f"{probability:.1%}"
            )


            st.progress(
                min(
                    max(probability, 0.0),
                    1.0
                )
            )


        except requests.RequestException as exc:

            st.error(
                f"Prediction API unavailable: {exc}"
            )


# =========================================================
# MODEL INFORMATION
# =========================================================

else:

    st.title(
        "Model Information"
    )

    st.caption(
        "Information about the deployed model "
        "and MLOps pipeline."
    )

    st.divider()


    info = get_model_info()


    if info:

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Input Features",
            info.get(
                "input_features",
                18
            )
        )


        col2.metric(
            "Classification Threshold",
            "45%"
        )


        col3.metric(
            "Model Type",
            info.get(
                "model_type",
                "N/A"
            )
        )


        st.subheader(
            "Deployed Model"
        )


        st.write(
            "**Model Repository:**",
            info.get(
                "model_repo",
                "N/A"
            )
        )


        st.write(
            "**Model File:**",
            info.get(
                "model_file",
                "N/A"
            )
        )


        st.subheader(
            "Pipeline Components"
        )


        pipeline_steps = info.get(
            "pipeline_steps",
            []
        )


        if pipeline_steps:

            pipeline_df = pd.DataFrame({
                "Pipeline Step":
                    pipeline_steps
            })

            st.dataframe(
                pipeline_df,
                hide_index=True,
                use_container_width=True
            )


    else:

        st.warning(
            "Unable to retrieve model information "
            "from the prediction API."
        )


    st.divider()


    # -----------------------------------------------------
    # INPUT FEATURES
    # -----------------------------------------------------

    st.subheader(
        "Input Features"
    )


    feature_col1, feature_col2 = st.columns(2)


    with feature_col1:

        st.markdown(
            """
            - Age
            - Gender
            - Marital Status
            - Occupation
            - Designation
            - Monthly Income
            - City Tier
            - Number of Trips
            - Passport
            """
        )


    with feature_col2:

        st.markdown(
            """
            - Number of Persons Visiting
            - Number of Children Visiting
            - Own Car
            - Type of Contact
            - Product Pitched
            - Duration of Pitch
            - Number of Follow-ups
            - Pitch Satisfaction Score
            - Preferred Property Star
            """
        )


    st.divider()


    # -----------------------------------------------------
    # MLOPS WORKFLOW
    # -----------------------------------------------------

    st.subheader(
        "MLOps Workflow"
    )


    st.code(
        """
GitHub Push
     ↓
HF Dataset Hub
     ↓
Clean → Split → Preprocess
     ↓
Train → Tune → MLflow
     ↓
Evaluate → Select Best Model
     ↓
HF Model Hub
     ↓
HF Prediction API
     ↓
Streamlit Interface
        """
    )


    with st.expander(
        "Prediction Logic"
    ):

        st.write(
            """
            The application sends the 18 original customer
            features to the prediction API.

            The deployed pipeline applies the same
            preprocessing used during model training and
            returns the predicted class and purchase
            probability.
            """
        )
