import pandas as pd

def process_asteroid_data(raw_data):
    """
    Converts raw NASA NEO API data into a clean pandas DataFrame
    """
    records = []

    for response in raw_data:
        for date, asteroids in response.get("near_earth_objects", {}).items():
            for asteroid in asteroids:

                name = asteroid.get("name")
                hazardous = asteroid.get("is_potentially_hazardous_asteroid")

                diameter_data_km = asteroid.get("estimated_diameter", {}).get("kilometers", {})
                min_diameter_km = diameter_data_km.get("estimated_diameter_min")
                max_diameter_km = diameter_data_km.get("estimated_diameter_max")
                mean_diameter_km = None

                if min_diameter_km and max_diameter_km:
                    mean_diameter_km = (min_diameter_km + max_diameter_km) / 2

                diameter_data_mile = asteroid.get("estimated_diameter", {}).get("miles", {})
                min_diameter_mile = diameter_data_mile.get("estimated_diameter_min")
                max_diameter_mile = diameter_data_mile.get("estimated_diameter_max")
                mean_diameter_mile = None

                if min_diameter_mile and max_diameter_mile:
                    mean_diameter_mile = (min_diameter_mile + max_diameter_mile) / 2

                for approach in asteroid.get("close_approach_data", []):

                    velocity_kms = float(approach.get("relative_velocity", {}).get("kilometers_per_second", 0))

                    velocity_mph = float(approach.get("relative_velocity", {}).get("miles_per_hour", 0))

                    miss_distance_km = float(approach.get("miss_distance", {}).get("kilometers", 0))

                    miss_distance_mile = float(approach.get("miss_distance", {}).get("miles", 0))

                    records.append({
                        "name": name,
                        "date": approach.get("close_approach_date"),

                        "min_diameter_km": min_diameter_km,
                        "max_diameter_km": max_diameter_km,
                        "mean_diameter_km": mean_diameter_km,

                        "min_diameter_miles": min_diameter_mile,
                        "max_diameter_miles": max_diameter_mile,
                        "mean_diameter_miles": mean_diameter_mile,

                        "velocity_km_s": velocity_kms,
                        "velocity_mph": velocity_mph,

                        "miss_distance_km": miss_distance_km,
                        "miss_distance_miles": miss_distance_mile,

                        "is_hazardous": hazardous
                    })

    df = pd.DataFrame(records)
    print(df)
    df["date"] = pd.to_datetime(df["date"])

    df["risk_score"] = (df["mean_diameter_km"] * df["velocity_km_s"]) / df["miss_distance_km"]

    # Normalize risk score
    if not df["risk_score"].empty:
        df["risk_score"] = df["risk_score"] / df["risk_score"].max()

    return df

if __name__ == "__main__":
    df = process_asteroid_data()