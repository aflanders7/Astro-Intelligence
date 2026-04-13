import pandas as pd

def process_asteroid_data(raw_data=[]):
    """
    Converts raw NASA NEO API data into a clean pandas DataFrame
    """
    records = []

    for response in raw_data:
        for date, asteroids in response.get("near_earth_objects", {}).items():
            for asteroid in asteroids:

                name = asteroid.get("name")
                hazardous = asteroid.get("is_potentially_hazardous_asteroid")

                diameter_data = asteroid.get("estimated_diameter", {}).get("kilometers", {})
                diameter_min = diameter_data.get("estimated_diameter_min")
                diameter_max = diameter_data.get("estimated_diameter_max")

                for approach in asteroid.get("close_approach_data", []):

                    velocity = float(
                        approach.get("relative_velocity", {})
                        .get("kilometers_per_second", 0)
                    )

                    miss_distance = float(
                        approach.get("miss_distance", {})
                        .get("kilometers", 0)
                    )

                    records.append({
                        "name": name,
                        "date": approach.get("close_approach_date"),
                        "min_diameter": diameter_min,
                        "max_diameter": diameter_max,
                        "velocity_km_s": velocity,
                        "miss_distance_km": miss_distance,
                        "is_hazardous": hazardous
                    })

    df = pd.DataFrame(records)

    return df

if __name__ == "__main__":
    df = process_asteroid_data()