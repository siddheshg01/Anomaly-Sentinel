import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

from config import (
    ROLLING_WINDOW,
    DEVIATION_THRESHOLD,
    ZSCORE_THRESHOLD,
    METRIC_WEIGHTS
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(

    page_title="AI Anomaly Monitoring Agent",

    page_icon="🚨",

    layout="wide"

)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "🚨 AI Anomaly Monitoring Agent"
)

st.caption(
    "Automated Business Metric Monitoring "
    "& Intelligent Alerts"
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(

    "Upload Business Excel File",

    type=["xlsx"]

)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if uploaded_file is not None:

    df = pd.read_excel(
        uploaded_file
    )

else:

    st.info(
        "No file uploaded. Using sample dataset."
    )

    df = load_data(
        "data/business_data.xlsx"
    )


# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

df["Date"] = pd.to_datetime(
    df["Date"]
)

df = df.sort_values(
    "Date"
)


# --------------------------------------------------
# METRICS
# --------------------------------------------------

metrics = [

    "Revenue",

    "Orders",

    "Conversion_Rate",

    "Traffic",

    "Cost",

    "Refunds"

]


# --------------------------------------------------
# ANALYZE METRICS
# --------------------------------------------------

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


# --------------------------------------------------
# LATEST DATA
# --------------------------------------------------

latest = df.iloc[-1]


# --------------------------------------------------
# CALCULATE TOTAL ANOMALIES
# --------------------------------------------------

anomaly_count = 0

for metric in metrics:

    if latest[
        f"{metric}_anomaly"
    ]:

        anomaly_count += 1


# --------------------------------------------------
# OVERALL RISK SCORE
# --------------------------------------------------

scores = []

for metric in metrics:

    score = latest[
        f"{metric}_score"
    ]

    scores.append(score)


if scores:

    overall_risk = max(scores)

else:

    overall_risk = 0


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader(
    "📊 Business Overview"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(

        "Revenue",

        f"₹{latest['Revenue']:,.0f}",

        f"{latest['Revenue_deviation']:+.1f}%"

    )


with col2:

    st.metric(

        "Orders",

        f"{latest['Orders']:,.0f}",

        f"{latest['Orders_deviation']:+.1f}%"

    )


with col3:

    st.metric(

        "Conversion Rate",

        f"{latest['Conversion_Rate']:.2f}%",

        f"{latest['Conversion_Rate_deviation']:+.1f}%"

    )


with col4:

    st.metric(

        "Traffic",

        f"{latest['Traffic']:,.0f}",

        f"{latest['Traffic_deviation']:+.1f}%"

    )


# --------------------------------------------------
# ALERT SUMMARY
# --------------------------------------------------

st.subheader(
    "🚨 Anomaly Status"
)

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "Anomalies Detected",

        anomaly_count

    )


with col2:

    st.metric(

        "Overall Risk Score",

        f"{overall_risk:.1f}/100"

    )


with col3:

    if overall_risk >= 70:

        status = "🔴 Critical"

    elif overall_risk >= 50:

        status = "🟠 High"

    elif overall_risk >= 20:

        status = "🟡 Warning"

    else:

        status = "🟢 Normal"

    st.metric(

        "Business Risk",

        status

    )


# --------------------------------------------------
# ANOMALY TABLE
# --------------------------------------------------

st.subheader(
    "🔎 Detected Anomalies"
)

anomaly_rows = []


for metric in metrics:

    anomaly = latest[
        f"{metric}_anomaly"
    ]

    if anomaly:

        anomaly_rows.append({

            "Metric": metric,

            "Current Value": latest[
                metric
            ],

            "Baseline": latest[
                f"{metric}_baseline"
            ],

            "Deviation %": latest[
                f"{metric}_deviation"
            ],

            "Z-Score": latest[
                f"{metric}_zscore"
            ],

            "Severity": latest[
                f"{metric}_severity"
            ],

            "Score": latest[
                f"{metric}_score"
            ]

        })


if anomaly_rows:

    anomaly_df = pd.DataFrame(
        anomaly_rows
    )

    st.dataframe(

        anomaly_df,

        use_container_width=True,

        hide_index=True

    )

else:

    st.success(
        "No significant anomalies detected."
    )


# --------------------------------------------------
# CHARTS
# --------------------------------------------------

st.subheader(
    "📈 Metric Trends"
)


# Revenue chart

fig_revenue = go.Figure()


fig_revenue.add_trace(

    go.Scatter(

        x=df["Date"],

        y=df["Revenue"],

        mode="lines",

        name="Revenue"

    )

)


fig_revenue.add_trace(

    go.Scatter(

        x=df["Date"],

        y=df["Revenue_baseline"],

        mode="lines",

        name="7-Day Baseline",

        line=dict(
            dash="dash"
        )

    )

)


fig_revenue.update_layout(

    title="Revenue vs Historical Baseline",

    xaxis_title="Date",

    yaxis_title="Revenue"

)


st.plotly_chart(

    fig_revenue,

    use_container_width=True

)


# Traffic chart

fig_traffic = go.Figure()


fig_traffic.add_trace(

    go.Scatter(

        x=df["Date"],

        y=df["Traffic"],

        mode="lines",

        name="Traffic"

    )

)


fig_traffic.add_trace(

    go.Scatter(

        x=df["Date"],

        y=df["Traffic_baseline"],

        mode="lines",

        name="7-Day Baseline",

        line=dict(
            dash="dash"
        )

    )

)


fig_traffic.update_layout(

    title="Traffic vs Historical Baseline",

    xaxis_title="Date",

    yaxis_title="Traffic"

)


st.plotly_chart(

    fig_traffic,

    use_container_width=True

)


# Conversion chart

fig_conversion = go.Figure()


fig_conversion.add_trace(

    go.Scatter(

        x=df["Date"],

        y=df["Conversion_Rate"],

        mode="lines",

        name="Conversion Rate"

    )

)


fig_conversion.add_trace(

    go.Scatter(

        x=df["Date"],

        y=df["Conversion_Rate_baseline"],

        mode="lines",

        name="7-Day Baseline",

        line=dict(
            dash="dash"
        )

    )

)


fig_conversion.update_layout(

    title="Conversion Rate vs Historical Baseline",

    xaxis_title="Date",

    yaxis_title="Conversion Rate (%)"

)


st.plotly_chart(

    fig_conversion,

    use_container_width=True

)


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader(
    "🧠 Business Insights"
)

insights = generate_business_insight(
    latest
)


for insight in insights:

    st.info(
        insight
    )


# --------------------------------------------------
# AI BUSINESS SUMMARY
# --------------------------------------------------

st.subheader(
    "🤖 AI Business Summary"
)


summary = generate_ai_summary(

    latest,

    insights

)

st.write(
    summary
)


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

st.subheader(
    "💡 Recommended Investigation"
)


recommendations = []


if latest[
    "Traffic_deviation"
] > 20 and latest[
    "Conversion_Rate_deviation"
] < -20:

    recommendations.append(
        "Investigate traffic sources "
        "and traffic quality."
    )

    recommendations.append(
        "Check landing-page conversion "
        "performance."
    )

    recommendations.append(
        "Review the customer conversion funnel."
    )


if latest[
    "Refunds_deviation"
] > 20:

    recommendations.append(
        "Investigate the main reasons "
        "for customer refunds."
    )


if latest[
    "Cost_deviation"
] > 20:

    recommendations.append(
        "Investigate the recent increase "
        "in operating or acquisition costs."
    )


if latest[
    "Revenue_deviation"
] < -20:

    recommendations.append(
        "Compare revenue performance "
        "across previous periods."
    )


if not recommendations:

    recommendations.append(
        "No immediate investigation "
        "is required based on current anomalies."
    )


for recommendation in recommendations:

    st.write(
        "• " + recommendation
    )


# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

with st.expander(
    "View Processed Data"
):

    st.dataframe(

        df,

        use_container_width=True

    )

      