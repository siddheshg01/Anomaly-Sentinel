def get_direction(
    deviation
):

    if deviation > 0:

        return "Increased"

    elif deviation < 0:

        return "Decreased"

    return "Stable"


def generate_metric_message(
    metric,
    deviation
):

    direction = get_direction(
        deviation
    )

    absolute_deviation = abs(
        deviation
    )

    if direction == "Increased":

        return (
            f"{metric} increased by "
            f"{absolute_deviation:.1f}% "
            f"compared with its recent baseline."
        )

    elif direction == "Decreased":

        return (
            f"{metric} decreased by "
            f"{absolute_deviation:.1f}% "
            f"compared with its recent baseline."
        )

    return (
        f"{metric} remained close to "
        f"its recent baseline."
    )


def generate_business_insight(
    latest
):

    insights = []

    revenue_deviation = (
        latest["Revenue_deviation"]
    )

    traffic_deviation = (
        latest["Traffic_deviation"]
    )

    conversion_deviation = (
        latest["Conversion_Rate_deviation"]
    )

    orders_deviation = (
        latest["Orders_deviation"]
    )

    cost_deviation = (
        latest["Cost_deviation"]
    )

    refunds_deviation = (
        latest["Refunds_deviation"]
    )

    # Scenario 1:
    # Traffic increases,
    # conversion decreases,
    # revenue decreases.

    if (

        traffic_deviation > 20

        and conversion_deviation < -20

        and revenue_deviation < 0

    ):

        insights.append(

            "Traffic increased significantly "
            "while conversion rate declined and "
            "revenue decreased. This may indicate "
            "lower-quality traffic or a problem "
            "in the conversion funnel."
        )

    # Scenario 2:
    # Revenue and orders both decrease.

    if (

        revenue_deviation < -20

        and orders_deviation < -20

    ):

        insights.append(

            "Revenue and order volume both declined "
            "significantly compared with the recent "
            "baseline. Demand, traffic sources, "
            "pricing and conversion performance "
            "should be investigated."
        )

    # Scenario 3:
    # Refunds increase.

    if refunds_deviation > 20:

        insights.append(

            "Refund activity increased significantly. "
            "The team should investigate refund reasons, "
            "product quality, customer expectations "
            "and fulfillment issues."
        )

    # Scenario 4:
    # Cost increases while revenue decreases.

    if (

        cost_deviation > 20

        and revenue_deviation < 0

    ):

        insights.append(

            "Costs increased while revenue declined. "
            "This may indicate deteriorating "
            "profitability and should be investigated."
        )

    if not insights:

        insights.append(

            "No major business relationship "
            "between the detected metric movements "
            "was identified."
        )

    return insights