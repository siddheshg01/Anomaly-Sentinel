import os

from dotenv import load_dotenv


load_dotenv()


def generate_fallback_summary(
    latest,
    insights
):

    anomaly_metrics = []

    metrics = [

        "Revenue",

        "Orders",

        "Conversion_Rate",

        "Traffic",

        "Cost",

        "Refunds"

    ]

    for metric in metrics:

        if latest[
            f"{metric}_anomaly"
        ]:

            anomaly_metrics.append(
                metric
            )

    if not anomaly_metrics:

        return (
            "No significant anomalies "
            "were detected in the latest "
            "business data."
        )

    summary = (

        f"{len(anomaly_metrics)} "
        f"business metrics show unusual "
        f"movement: "
        f"{', '.join(anomaly_metrics)}."

    )

    if insights:

        summary += " "

        summary += " ".join(
            insights
        )

    return summary


def generate_ai_summary(
    latest,
    insights
):

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        return generate_fallback_summary(
            latest,
            insights
        )

    try:

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key
        )

        prompt = f"""
You are a business data analyst.

Analyze the following detected business
metric anomalies.

Revenue:
Current = {latest["Revenue"]}
Baseline = {latest["Revenue_baseline"]}
Deviation = {latest["Revenue_deviation"]:.2f}%
Severity = {latest["Revenue_severity"]}

Orders:
Current = {latest["Orders"]}
Baseline = {latest["Orders_baseline"]}
Deviation = {latest["Orders_deviation"]:.2f}%
Severity = {latest["Orders_severity"]}

Conversion Rate:
Current = {latest["Conversion_Rate"]}
Baseline = {latest["Conversion_Rate_baseline"]}
Deviation = {latest["Conversion_Rate_deviation"]:.2f}%
Severity = {latest["Conversion_Rate_severity"]}

Traffic:
Current = {latest["Traffic"]}
Baseline = {latest["Traffic_baseline"]}
Deviation = {latest["Traffic_deviation"]:.2f}%
Severity = {latest["Traffic_severity"]}

Cost:
Current = {latest["Cost"]}
Baseline = {latest["Cost_baseline"]}
Deviation = {latest["Cost_deviation"]:.2f}%
Severity = {latest["Cost_severity"]}

Refunds:
Current = {latest["Refunds"]}
Baseline = {latest["Refunds_baseline"]}
Deviation = {latest["Refunds_deviation"]:.2f}%
Severity = {latest["Refunds_severity"]}

Business insights already identified:

{chr(10).join(insights)}

Write a concise business summary.

Include:

1. What changed
2. The most important anomaly
3. Possible business explanation
4. Potential business impact
5. What an analyst should investigate next

Important rules:

- Do not invent facts.
- Clearly distinguish observations from possible explanations.
- Use phrases such as "may indicate" when discussing causes.
- Keep the answer concise and professional.
"""

        response = client.responses.create(

            model="gpt-5.4-mini",

            input=prompt

        )

        return response.output_text

    except Exception as error:

        print(
            f"AI API error: {error}"
        )

        return generate_fallback_summary(
            latest,
            insights
        )