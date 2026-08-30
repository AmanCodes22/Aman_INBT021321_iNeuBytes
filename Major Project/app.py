import streamlit as st
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class FeatureEngineeringTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        # Dates
        X["published_date"] = pd.to_datetime(
            X["published_date"],
            errors="coerce",
            utc=True
        )

        X["updated_date"] = pd.to_datetime(
            X["updated_date"],
            errors="coerce",
            utc=True
        )

        # Date features
        X["published_year"] = X["published_date"].dt.year
        X["published_month"] = X["published_date"].dt.month
        X["published_quarter"] = X["published_date"].dt.quarter
        X["published_dayofweek"] = X["published_date"].dt.dayofweek

        # Text features
        X["title"] = X["title"].fillna("")
        X["description"] = X["description"].fillna("")

        X["title_length"] = X["title"].str.len()
        X["title_word_count"] = X["title"].str.split().str.len()

        X["description_length"] = X["description"].str.len()
        X["description_word_count"] = (
            X["description"].str.split().str.len()
        )

        X["text_length"] = (
            X["title_length"] +
            X["description_length"]
        )

        X["text_word_count"] = (
            X["title_word_count"] +
            X["description_word_count"]
        )

        # Organisation
        X["author_organisation"] = (
            X["author_organisation"].fillna("")
        )

        X["organisation_length"] = (
            X["author_organisation"].str.len()
        )

        X["organisation_word_count"] = (
            X["author_organisation"].str.split().str.len()
        )

        # Topic
        X["has_topic"] = (
            X["topic_url"].notna()
        ).astype(int)

        X["topic_category"] = (
            X["topic_url"]
            .fillna("")
            .str.replace(
                "https://www.gov.uk/",
                "",
                regex=False
            )
            .str.split("/")
            .str[0]
        )

        return X

# -----------------------------------
# LOAD MODEL
# -----------------------------------

model = joblib.load(
    "data/govuk_final_deployment_pipeline.joblib"
)


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="GOV.UK Update Time Predictor",
    page_icon="🇬🇧",
    layout="centered"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("🇬🇧 GOV.UK Publication Update Predictor")

st.write(
    "Predict whether a GOV.UK publication is likely to "
    "have a high update time."
)


# -----------------------------------
# USER INPUT
# -----------------------------------

title = st.text_input(
    "Publication Title",
    placeholder="Enter publication title"
)

description = st.text_area(
    "Description",
    placeholder="Enter publication description"
)

author_organisation = st.text_input(
    "Author Organisation",
    placeholder="e.g. Department for Transport"
)

published_date = st.date_input(
    "Published Date"
)

topic_url = st.text_input(
    "Topic URL",
    placeholder="https://www.gov.uk/transport"
)


# -----------------------------------
# PREDICTION
# -----------------------------------

if st.button("Predict"):

    if not title or not author_organisation:
        st.warning(
            "Please enter at least the title "
            "and author organisation."
        )

    else:

        # Convert date to datetime
        published_datetime = pd.Timestamp(
            published_date,
            tz="UTC"
        )

        # updated_date is not required for prediction
        # because days_to_update is not used as a feature.
        new_data = pd.DataFrame({
            "title": [title],
            "description": [description],
            "url": [""],
            "author_organisation": [author_organisation],
            "published_date": [published_datetime],
            "updated_date": [published_datetime],
            "topic_url": [
                topic_url if topic_url else None
            ]
        })

        prediction = model.predict(new_data)[0]

        probability = model.predict_proba(
            new_data
        )[0][1]


        # -----------------------------------
        # RESULT
        # -----------------------------------

        st.subheader("Prediction")

        if prediction == 1:

            st.error(
                "⚠️ High Update Time"
            )

            st.write(
                f"Probability of high update time: "
                f"{probability:.2%}"
            )

        else:

            st.success(
                "✅ Low Update Time"
            )

            st.write(
                f"Probability of high update time: "
                f"{probability:.2%}"
            )