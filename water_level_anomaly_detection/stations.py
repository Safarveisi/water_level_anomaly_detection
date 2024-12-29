from typing import List, Optional
import requests


def get_stations_uuid() -> Optional[List[str]]:
    """List of all available station ids"""
    try:
        res = requests.get(
            f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json"
        )
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    stations_uuid = [station["uuid"] for station in res.json()]
    return stations_uuid
