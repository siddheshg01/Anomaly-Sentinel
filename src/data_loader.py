import pandas as pd


def load_data(file_path):

    df = pd.read_excel(file_path)

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    df = df.sort_values(
        "Date"
    )

    df = df.drop_duplicates()

    return df