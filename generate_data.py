import pandas as pd
import numpy as np


def generate_business_data():

    np.random.seed(42)

    dates = pd.date_range(
        start="2026-06-13",
        periods=60,
        freq="D"
    )

    traffic = np.random.randint(
        9000,
        13000,
        60
    )

    conversion_rate = np.random.uniform(
        3.2,
        4.2,
        60
    )

    orders = (
        traffic * conversion_rate / 100
    ).astype(int)

    revenue = (
        orders * np.random.uniform(
            280,
            330,
            60
        )
    ).astype(int)

    cost = (
        revenue * np.random.uniform(
            0.30,
            0.40,
            60
        )
    ).astype(int)

    refunds = (
        revenue * np.random.uniform(
            0.008,
            0.015,
            60
        )
    ).astype(int)

    df = pd.DataFrame({

        "Date": dates,

        "Revenue": revenue,

        "Orders": orders,

        "Conversion_Rate": conversion_rate.round(2),

        "Traffic": traffic,

        "Cost": cost,

        "Refunds": refunds

    })

    # Anomaly 1:
    # Revenue and orders suddenly decrease

    df.loc[45, "Revenue"] = 78000
    df.loc[45, "Orders"] = 250

    # Anomaly 2:
    # Traffic increases but conversion decreases

    df.loc[50, "Traffic"] = 17000
    df.loc[50, "Conversion_Rate"] = 2.0

    # Recalculate orders for anomaly 2

    df.loc[50, "Orders"] = int(
        df.loc[50, "Traffic"]
        * df.loc[50, "Conversion_Rate"]
        / 100
    )

    # Anomaly 3:
    # Refunds suddenly increase

    df.loc[54, "Refunds"] = 6000

    # Anomaly 4:
    # Cost suddenly increases

    df.loc[57, "Cost"] = 70000

    # Anomaly 5:
    # Major revenue drop

    df.loc[59, "Revenue"] = 75000
    df.loc[59, "Orders"] = 240
    df.loc[59, "Traffic"] = 15000
    df.loc[59, "Conversion_Rate"] = 2.1

    return df


def main():

    df = generate_business_data()

    df.to_excel(
        "data/business_data.xlsx",
        index=False
    )

    print("Business data created successfully.")

    print()
    print(df)


if __name__ == "__main__":
    main()