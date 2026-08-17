from datetime import datetime

from src.data_loader import load_data

from src.anomaly_detector import (
    analyze_metric
)

from src.business_rules import (
    generate_business_insight
)

from src.ai_summarizer import (
    generate_ai_summary
)

from src.email_alert import (
    send_email_alert
)

from config import (
    ROLLING_WINDOW,
    DEVIATION_THRESHOLD,
    ZSCORE_THRESHOLD,
    METRIC_WEIGHTS,
    OVERALL_RISK_THRESHOLD
)


def main():

    # ==================================================
    # PROJECT TITLE
    # ==================================================

    print("=" * 60)

    print(
        "AI ANOMALY MONITORING AGENT"
    )

    print("=" * 60)


    # ==================================================
    # LOAD EXCEL DATA
    # ==================================================

    file_path = "data/business_data.xlsx"

    df = load_data(
        file_path
    )


    # ==================================================
    # METRICS TO MONITOR
    # ==================================================

    metrics = [

        "Revenue",

        "Orders",

        "Conversion_Rate",

        "Traffic",

        "Cost",

        "Refunds"

    ]


    # ==================================================
    # ANALYZE ALL METRICS
    # ==================================================

    for metric in metrics:

        df = analyze_metric(

            df,

            metric,

            window=ROLLING_WINDOW,

            deviation_threshold=(
                DEVIATION_THRESHOLD
            ),

            zscore_threshold=(
                ZSCORE_THRESHOLD
            ),

            weight=(
                METRIC_WEIGHTS[metric]
            )

        )


    # ==================================================
    # GET LATEST DATA
    # ==================================================

    latest = df.iloc[-1]


    # ==================================================
    # CALCULATE OVERALL RISK SCORE
    # ==================================================

    scores = []

    for metric in metrics:

        score = latest[
            f"{metric}_score"
        ]

        scores.append(
            score
        )


    overall_risk = max(
        scores
    )


    # ==================================================
    # DISPLAY LATEST DATE
    # ==================================================

    print()

    print(
        f"Latest Date: "
        f"{latest['Date'].date()}"
    )


    # ==================================================
    # DISPLAY METRIC ANALYSIS
    # ==================================================

    print()

    print(
        "LATEST METRIC ANALYSIS"
    )

    print("-" * 60)


    for metric in metrics:

        current = latest[
            metric
        ]

        baseline = latest[
            f"{metric}_baseline"
        ]

        deviation = latest[
            f"{metric}_deviation"
        ]

        zscore = latest[
            f"{metric}_zscore"
        ]

        anomaly = latest[
            f"{metric}_anomaly"
        ]

        severity = latest[
            f"{metric}_severity"
        ]

        score = latest[
            f"{metric}_score"
        ]


        print()

        print(
            f"Metric: {metric}"
        )

        print(
            f"Current Value : "
            f"{current:.2f}"
        )

        print(
            f"Baseline      : "
            f"{baseline:.2f}"
        )

        print(
            f"Deviation     : "
            f"{deviation:+.2f}%"
        )

        print(
            f"Z-Score       : "
            f"{zscore:.2f}"
        )

        print(
            f"Severity      : "
            f"{severity}"
        )

        print(
            f"Anomaly Score : "
            f"{score:.2f}"
        )


        if anomaly:

            print(
                "Status        : ANOMALY"
            )

        else:

            print(
                "Status        : Normal"
            )


    # ==================================================
    # BUSINESS INSIGHTS
    # ==================================================

    print()

    print("=" * 60)

    print(
        "BUSINESS INSIGHTS"
    )

    print("=" * 60)


    insights = generate_business_insight(
        latest
    )


    for insight in insights:

        print()

        print(
            "• " + insight
        )


    # ==================================================
    # AI BUSINESS SUMMARY
    # ==================================================

    summary = generate_ai_summary(

        latest,

        insights

    )


    print()

    print("=" * 60)

    print(
        "BUSINESS SUMMARY"
    )

    print("=" * 60)

    print()

    print(
        summary
    )


    # ==================================================
    # CREATE EMAIL BODY
    # ==================================================

    email_lines = []


    email_lines.append(
        "AI ANOMALY MONITORING AGENT"
    )


    email_lines.append(

        f"Date: "
        f"{latest['Date'].date()}"

    )


    email_lines.append("")


    email_lines.append(

        f"Overall Risk Score: "
        f"{overall_risk:.2f}/100"

    )


    email_lines.append("")


    email_lines.append(
        "Detected Anomalies:"
    )


    for metric in metrics:

        if latest[
            f"{metric}_anomaly"
        ]:

            email_lines.append(

                f"- {metric}: "
                f"{latest[f'{metric}_deviation']:+.2f}% "
                f"({latest[f'{metric}_severity']})"

            )


    email_lines.append("")


    email_lines.append(
        "Business Summary:"
    )


    email_lines.append(
        summary
    )


    email_body = "\n".join(
        email_lines
    )


    # ==================================================
    # SEND EMAIL ALERT
    # ==================================================

    if (
        overall_risk
        >= OVERALL_RISK_THRESHOLD
    ):

        email_sent = send_email_alert(

            "🚨 Business Metric Anomaly Detected",

            email_body

        )


        if email_sent:

            print()

            print(
                "Email alert sent successfully."
            )


            # ------------------------------------------
            # SAVE ALERT TO LOG
            # ------------------------------------------

            with open(

                "logs/alerts.log",

                "a"

            ) as file:

                file.write(

                    f"{datetime.now()} | "
                    f"Risk Score: "
                    f"{overall_risk:.2f} | "
                    f"Email Sent\n"

                )


        else:

            print()

            print(
                "Email alert could not be sent."
            )


    else:

        print()

        print(
            "Risk score is below "
            "the email alert threshold."
        )


    # ==================================================
    # CREATE ANOMALY REPORT
    # ==================================================

    anomaly_rows = []


    for metric in metrics:

        if latest[
            f"{metric}_anomaly"
        ]:

            anomaly_rows.append({

                "Date": latest[
                    "Date"
                ],

                "Metric": metric,

                "Current_Value": latest[
                    metric
                ],

                "Baseline": latest[
                    f"{metric}_baseline"
                ],

                "Deviation_Percent": latest[
                    f"{metric}_deviation"
                ],

                "Z_Score": latest[
                    f"{metric}_zscore"
                ],

                "Severity": latest[
                    f"{metric}_severity"
                ],

                "Anomaly_Score": latest[
                    f"{metric}_score"
                ]

            })


    # ==================================================
    # SAVE REPORT
    # ==================================================

    if anomaly_rows:

        import pandas as pd


        anomaly_df = pd.DataFrame(
            anomaly_rows
        )


        anomaly_df.to_csv(

            "reports/anomaly_report.csv",

            index=False

        )


        print()

        print(
            "Anomaly report saved to:"
        )

        print(
            "reports/anomaly_report.csv"
        )


    else:

        print()

        print(
            "No anomalies detected."
        )


# ======================================================
# PROGRAM START
# ======================================================

if __name__ == "__main__":

    main()