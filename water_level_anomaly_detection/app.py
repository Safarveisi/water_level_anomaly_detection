import json
import sys
import logging
from typing import Tuple, Optional
from etl import get_station_measurements
from stations import get_stations_uuid
from plot import plot_detection, plot_reference_data
from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import streamlit as st

logger = logging.getLogger("WaterLevelAnomalyDetection")
logger.setLevel(logging.INFO)

# Create console handler (ch) and set level to info
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

# Add ch to logger
logger.addHandler(ch)


def detection(df_ref: pd.DataFrame, df_pred: pd.DataFrame) -> pd.DataFrame:
    logger.info("Running novelty detection ...")

    # Initialize the novelty detection ML algorithm
    clf = LocalOutlierFactor(n_neighbors=2, novelty=True)

    # Feed the reference measurements to the ML model
    clf.fit(df_ref["value"].values.reshape(-1, 1))

    # Add a new column to the data frame holding the detection results 
    # (1 --> normal, -1 --> abnormal)
    df_pred["novelty"] = clf.predict(df_pred["value"].values.reshape(-1, 1))

    return df_pred


def get_station_data(
    uuid: str,
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    logger.info(f"Getting latest station data with id: {uuid} ...")

    # Retrieve data for the selected station
    df_ref, df_pred = get_station_measurements(
        uuid=uuid, reference_window="PT6H", prediction_window="PT1H"
    )

    return df_ref, df_pred


st.set_page_config(layout="wide")
st.title("Novelty Detection for Water Level")

# Select station uuid
uuid = st.selectbox("Station UUID", get_stations_uuid())

# Retrieve data for the selected station (reference + prediction)
df_ref, df_pred = get_station_data(uuid=uuid)

if df_pred is None or df_ref is None:
    msg = """
    There are no measurements for the requested station.
    Please try again later! :sleeping:
    """
    st.write(msg)
    logger.error(msg)

else:
    msg = "Fetching new measurements successful!"
    st.write(msg)
    logger.info(msg)

    if df_pred.empty or df_ref.empty:
        msg = """
        Either reference or prediction data frames
        are empty! Please try again later! :sleeping:
        """
        st.write(msg)
        logger.info(msg)
    else:
        st.write("Running novelty detection and plotting :fire:")
        df_pred = detection(df_ref=df_ref, df_pred=df_pred)
        fig_pred = plot_detection(df=df_pred)
        st.pyplot(fig_pred, use_container_width=True)
        fig_ref = plot_reference_data(df=df_ref)
        st.pyplot(fig_ref, use_container_width=True)
