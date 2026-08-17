import numpy as np


def add_baseline(
    df,
    column,
    window=7
):

    baseline_column = f"{column}_baseline"

    df[baseline_column] = (
        df[column]
        .rolling(window)
        .mean()
        .shift(1)
    )

    return df


def calculate_deviation(
    df,
    column
):

    baseline_column = f"{column}_baseline"

    deviation_column = f"{column}_deviation"

    df[deviation_column] = (
        (
            df[column]
            - df[baseline_column]
        )
        / df[baseline_column]
    ) * 100

    return df


def calculate_zscore(
    df,
    column,
    window=7
):

    mean_column = f"{column}_mean"

    std_column = f"{column}_std"

    zscore_column = f"{column}_zscore"

    df[mean_column] = (
        df[column]
        .rolling(window)
        .mean()
        .shift(1)
    )

    df[std_column] = (
        df[column]
        .rolling(window)
        .std()
        .shift(1)
    )

    df[zscore_column] = (
        df[column]
        - df[mean_column]
    ) / df[std_column]

    return df


def detect_anomaly(
    df,
    column,
    deviation_threshold=20,
    zscore_threshold=3
):

    deviation_column = f"{column}_deviation"

    zscore_column = f"{column}_zscore"

    anomaly_column = f"{column}_anomaly"

    df[anomaly_column] = (

        (
            df[deviation_column]
            .abs()
            >= deviation_threshold
        )

        |

        (
            df[zscore_column]
            .abs()
            >= zscore_threshold
        )

    )

    return df


def get_severity(
    deviation
):

    if np.isnan(deviation):

        return "Normal"

    absolute_deviation = abs(
        deviation
    )

    if absolute_deviation >= 30:

        return "Critical"

    elif absolute_deviation >= 20:

        return "High"

    elif absolute_deviation >= 10:

        return "Warning"

    else:

        return "Normal"


def calculate_anomaly_score(
    deviation,
    zscore,
    weight=1.0
):

    if np.isnan(deviation):

        return 0

    deviation_score = min(
        abs(deviation) / 50 * 70,
        70
    )

    if np.isnan(zscore):

        zscore_score = 0

    else:

        zscore_score = min(
            abs(zscore) / 5 * 30,
            30
        )

    score = (
        deviation_score
        + zscore_score
    )

    score = score * weight

    return round(
        min(score, 100),
        2
    )


def analyze_metric(
    df,
    column,
    window=7,
    deviation_threshold=20,
    zscore_threshold=3,
    weight=1.0
):

    df = add_baseline(
        df,
        column,
        window
    )

    df = calculate_deviation(
        df,
        column
    )

    df = calculate_zscore(
        df,
        column,
        window
    )

    df = detect_anomaly(
        df,
        column,
        deviation_threshold,
        zscore_threshold
    )

    severity_column = f"{column}_severity"

    score_column = f"{column}_score"

    df[severity_column] = (
        df[f"{column}_deviation"]
        .apply(get_severity)
    )

    df[score_column] = df.apply(

        lambda row:
        calculate_anomaly_score(

            row[f"{column}_deviation"],

            row[f"{column}_zscore"],

            weight

        ),

        axis=1
    )

    return df