import re
import requests
from requests.exceptions import RequestException
from datetime import datetime, timedelta
from typing import Optional, Tuple
import pandas as pd

PATTERN = r"^PT(\d+)H$"


def extract_hours(window: str, pattern: str = PATTERN) -> int:
    match = re.match(pattern, window)
    if not match:
        raise ValueError(f"Window '{window}' does not match format 'PT(INTEGER)H'.")
    return int(match.group(1))


def get_station_measurements(
    uuid: str, reference_window: str = "PT6H", prediction_window: str = "PT1H"
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Get the water level measurements for the requested
    window and the selected uuid (station).

    Parameters
    ==========
    uuid: str
        The uuid of the station for which the measurements should be fetched.

    reference_window: str
        Window to be used to fetch reference data. Note that this
        window ends where the prediction_window starts.

    prediction_window: str
        Window (with respect to the current timestamp) to be
        used to fetch data for prediction (anomaly detection).

    Returns
    =======
    A tuple of two pandas dataframes or None.
    """

    current_ts = pd.to_datetime(datetime.now())  # This is already naive
    reference_hours = extract_hours(reference_window)
    prediction_hours = extract_hours(prediction_window)
    overall_window = f"PT{reference_hours+prediction_hours}H"

    url = (
        "https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations"
        f"/{uuid}/W/measurements.json?start={overall_window}"
    )
    try:
        res = requests.get(url)
        res.raise_for_status()
    except RequestException as e:
        return None, None

    measurements = res.json()
    if not measurements:
        return None, None

    df = pd.DataFrame(measurements)
    ref_cutoff = current_ts - timedelta(hours=prediction_hours)
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(
        None
    )  # Ensure DataFrame timestamps are also naive
    ref_df = df[df["timestamp"] < ref_cutoff]
    pred_df = df[df["timestamp"] >= ref_cutoff]

    return ref_df, pred_df
