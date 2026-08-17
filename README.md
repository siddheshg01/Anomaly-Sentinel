# Anomaly Sentinel

> **AI-powered Business Anomaly Monitoring Agent**

Anomaly Sentinel is an automated business-metric monitoring system that
reads Excel-based operational data, establishes historical baselines,
detects unusual metric behavior using statistical techniques, converts
detected patterns into business insights, generates a natural-language
summary, visualizes results through a Streamlit dashboard, and sends
email alerts when the business risk crosses a configurable threshold.

------------------------------------------------------------------------

## 1. Project Overview

Traditional Exploratory Data Analysis (EDA) projects usually answer
questions such as:

-   What happened?
-   What does the data look like?
-   Which metric is highest or lowest?
-   What patterns can be observed?

Anomaly Sentinel goes one step further.

It is designed as a **monitoring and alerting system** rather than a
static analysis notebook.

The system continuously follows this conceptual workflow:

``` text
Business Data
     |
     v
Data Loading
     |
     v
Data Validation / Preprocessing
     |
     v
Historical Baseline
     |
     v
Statistical Anomaly Detection
     |
     v
Severity + Risk Scoring
     |
     v
Business Rule Interpretation
     |
     v
AI Business Summary
     |
     +------------------+
     |                  |
     v                  v
Dashboard          Email Alert
```

The main objective is to help an analyst or manager identify important
changes early instead of manually checking spreadsheets.

------------------------------------------------------------------------

## 2. Problem Statement

Business teams frequently receive reports containing metrics such as:

-   Revenue
-   Orders
-   Traffic
-   Conversion Rate
-   Cost
-   Refunds

A typical manual workflow is:

``` text
Open Excel
   |
Compare today's numbers with previous periods
   |
Identify unusual changes
   |
Investigate related metrics
   |
Write an explanation
   |
Notify stakeholders
```

This process is:

-   Repetitive
-   Time-consuming
-   Easy to miss
-   Difficult to scale
-   Dependent on manual interpretation

### Proposed Solution

Anomaly Sentinel automates the first level of monitoring:

``` text
Excel
  |
Automatic analysis
  |
Detect unusual behavior
  |
Measure severity
  |
Interpret relationships
  |
Generate explanation
  |
Alert stakeholder
```

The system does not attempt to replace an analyst. It acts as an
**early-warning assistant** that tells the analyst where attention is
required.

------------------------------------------------------------------------

## 3. Key Objectives

The project has the following objectives:

1.  Read business data from Excel.
2.  Validate and prepare the data for analysis.
3.  Establish a historical baseline for each monitored metric.
4.  Detect statistically unusual observations.
5.  Quantify the magnitude of the anomaly.
6.  Assign severity levels.
7.  Calculate an anomaly/risk score.
8.  Identify meaningful relationships between metrics.
9.  Generate a business-friendly explanation.
10. Display results through an interactive dashboard.
11. Send email alerts for high-risk situations.
12. Maintain a historical alert log.
13. Produce a CSV anomaly report for further analysis.

------------------------------------------------------------------------

## 4. Business Use Case

Consider the following situation:

``` text
Traffic           +30%
Conversion Rate   -25%
Orders            -20%
Revenue           -34%
```

Looking at individual metrics is useful, but the relationship is more
important.

The system can identify the pattern:

``` text
Traffic increased
        |
        v
Conversion decreased
        |
        v
Orders decreased
        |
        v
Revenue decreased
```

The business interpretation may be:

> Traffic increased significantly while conversion rate declined and
> revenue decreased. This may indicate lower-quality traffic or a
> problem in the conversion funnel.

The system can then recommend investigation areas such as:

-   Traffic sources
-   Landing pages
-   Conversion funnel
-   Pricing
-   Customer journey
-   Acquisition channels

This is the main difference between a static chart and an operational
monitoring system.

------------------------------------------------------------------------

# 5. Monitored Metrics

The current version monitors six business metrics:

  Metric            Description
  ----------------- --------------------------------------
  Revenue           Revenue generated during the period
  Orders            Number of completed orders
  Conversion_Rate   Percentage of visitors who convert
  Traffic           Number of visitors/sessions
  Cost              Business or acquisition-related cost
  Refunds           Number/value of refunds

The architecture is extensible, so additional metrics can be added
later.

------------------------------------------------------------------------

# 6. Input Data

The primary input is:

``` text
data/business_data.xlsx
```

Expected columns:

``` text
Date
Revenue
Orders
Conversion_Rate
Traffic
Cost
Refunds
```

Example:

  Date           Revenue   Orders   Conversion_Rate   Traffic    Cost   Refunds
  ------------ --------- -------- ----------------- --------- ------- ---------
  2026-07-01      120000      400              3.20     12500   35000        18
  2026-07-02      121500      405              3.24     12700   35200        20
  2026-07-03      119800      395              3.11     12400   34900        19

The project can also accept an uploaded Excel file through the Streamlit
dashboard.

------------------------------------------------------------------------

# 7. Detection Methodology

## 7.1 Historical Baseline

The system calculates a rolling historical baseline.

The current implementation uses a configurable window:

``` python
ROLLING_WINDOW = 7
```

Conceptually:

``` text
Baseline = Average of previous 7 observations
```

The current observation is excluded from its own baseline.

This prevents an anomalous value from influencing the normal reference
point against which it is evaluated.

------------------------------------------------------------------------

## 7.2 Percentage Deviation

The system calculates:

``` text
Deviation % =
(Current Value - Baseline)
-------------------------- x 100
        Baseline
```

Example:

``` text
Baseline = 100,000
Current  = 70,000

Deviation =
(70,000 - 100,000) / 100,000 * 100

= -30%
```

Interpretation:

``` text
Revenue decreased by 30% compared with its recent baseline.
```

------------------------------------------------------------------------

## 7.3 Z-Score

The project also uses a Z-score:

``` text
Z = (Current Value - Historical Mean)
    ----------------------------------
        Historical Standard Deviation
```

The Z-score measures how far the current observation is from the
historical distribution.

For example:

``` text
Z = -3.5
```

means the observation is approximately 3.5 standard deviations below the
historical mean.

The configured threshold is:

``` python
ZSCORE_THRESHOLD = 3
```

Therefore, a sufficiently large absolute Z-score is treated as an
anomaly signal.

------------------------------------------------------------------------

## 7.4 Anomaly Detection

The project combines multiple signals.

Typical logic:

``` text
IF
    absolute percentage deviation >= threshold
OR
    absolute Z-score >= threshold

THEN
    anomaly = True
```

Current configuration:

``` python
DEVIATION_THRESHOLD = 20
ZSCORE_THRESHOLD = 3
```

This can be modified through `config.py`.

------------------------------------------------------------------------

# 8. Severity Classification

Anomaly severity is used to prioritize attention.

A typical interpretation is:

              Deviation Severity
  --------------------- ----------
         Small movement Normal
      Moderate movement Warning
         Large movement High
    Very large movement Critical

The exact thresholds are implemented in the
anomaly-detection/business-rule layer and can be adjusted as the project
evolves.

Severity should not be treated as a diagnosis. It is a prioritization
mechanism.

------------------------------------------------------------------------

# 9. Anomaly Score

The project produces an anomaly score on a 0--100 style scale.

The score is intended to answer:

> How urgent or unusual is this metric compared with its recent
> behavior?

The system also calculates an overall risk value from the monitored
metric scores.

Current configuration:

``` python
OVERALL_RISK_THRESHOLD = 70
```

Conceptually:

``` text
Risk < 70
    |
    v
No automatic alert

Risk >= 70
    |
    v
Email alert
```

The score is a prioritization mechanism rather than a probability of
business failure.

------------------------------------------------------------------------

# 10. Business Intelligence Layer

Pure statistical detection is not enough.

For example:

``` text
Traffic anomaly
+
Conversion anomaly
+
Revenue anomaly
```

is more meaningful than three independent anomaly messages.

The business-rule layer looks for combinations and directional
relationships between metrics.

Examples:

### Pattern 1

``` text
Traffic ↑
Conversion ↓
Revenue ↓
```

Possible interpretation:

``` text
Potential traffic-quality or conversion-funnel issue.
```

### Pattern 2

``` text
Cost ↑
Revenue ↓
```

Possible interpretation:

``` text
Potential deterioration in acquisition efficiency.
```

### Pattern 3

``` text
Refunds ↑
```

Possible investigation areas:

``` text
Product quality
Customer complaints
Delivery issues
Returns policy
Order fulfillment
```

The system deliberately uses language such as:

``` text
"may indicate"
"could indicate"
"should be investigated"
```

rather than claiming an unverified cause.

------------------------------------------------------------------------

# 11. AI Layer

The AI component is responsible for **interpretation and
communication**, not primary statistical detection.

The architecture is:

``` text
Raw Excel Data
      |
      v
Python Statistical Engine
      |
      v
Detected Anomalies
      |
      v
Business Rules
      |
      v
Structured Findings
      |
      v
AI Summarizer
      |
      v
Business-Friendly Explanation
```

This separation is intentional.

### Why?

The system should not ask an LLM to decide whether:

``` text
Revenue = anomaly
```

when a deterministic statistical method can make that decision
transparently.

Instead:

``` text
Python
    -> What changed?

Business rules
    -> What relationships are important?

AI
    -> How can this be explained clearly?
```

This makes the system easier to test, explain and debug.

------------------------------------------------------------------------

# 12. AI Fallback

The project includes a fallback summarizer.

If the OpenAI package or API configuration is unavailable, the system
can still produce a rule-based summary.

Conceptually:

``` text
AI available?
     |
   YES
     |
     v
LLM-generated summary

   NO
     |
     v
Fallback business summary
```

This is important for system reliability.

The core monitoring functionality should not completely fail just
because the AI service is temporarily unavailable.

------------------------------------------------------------------------

# 13. Dashboard

The project includes a Streamlit dashboard.

Run:

``` bash
streamlit run dashboard.py
```

The dashboard provides:

### Business Overview

-   Revenue
-   Orders
-   Conversion Rate
-   Traffic

### Anomaly Status

-   Number of anomalies
-   Overall risk score
-   Business risk level

### Anomaly Table

-   Metric
-   Current value
-   Baseline
-   Deviation
-   Z-score
-   Severity
-   Anomaly score

### Trend Charts

-   Revenue vs baseline
-   Traffic vs baseline
-   Conversion Rate vs baseline

### Intelligence

-   Business insights
-   AI summary
-   Recommended investigation areas

### Raw Data

The processed DataFrame can also be inspected from the dashboard.

------------------------------------------------------------------------

# 14. Email Alerting

The email system is implemented using Python SMTP.

The workflow is:

``` text
Anomaly detected
      |
      v
Calculate overall risk
      |
      v
Risk >= configured threshold?
      |
     YES
      |
      v
Create email
      |
      v
Send through SMTP
      |
      v
Save alert log
```

The email contains:

``` text
Date
Overall Risk Score
Detected Metrics
Deviation
Severity
Business Summary
```

The project uses environment variables for credentials rather than
hard-coding them.

------------------------------------------------------------------------

# 15. Environment Variables

Create a local `.env` file:

``` text
OPENAI_API_KEY=your_api_key

EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=receiver@example.com

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

Never commit `.env` to GitHub.

The `.gitignore` should include:

``` text
.env
venv/
__pycache__/
*.pyc
```

Use `.env.example` as the safe configuration template.

------------------------------------------------------------------------

# 16. Alert Logging

Successful alerts are recorded in:

``` text
logs/alerts.log
```

Example:

``` text
2026-08-17 20:10:00 | Risk Score: 86.42 | Email Sent
```

This provides a basic audit trail of alert activity.

A future production version should store structured alert records in a
database.

------------------------------------------------------------------------

# 17. Generated Report

Detected anomalies are saved as:

``` text
reports/anomaly_report.csv
```

The report contains fields such as:

``` text
Date
Metric
Current_Value
Baseline
Deviation_Percent
Z_Score
Severity
Anomaly_Score
```

This allows the user to perform additional analysis outside the
dashboard.

------------------------------------------------------------------------

# 18. Project Architecture

``` text
AI-Anomaly-Agent/
│
├── data/
│   └── business_data.xlsx
│
├── reports/
│   └── anomaly_report.csv
│
├── logs/
│   └── alerts.log
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── anomaly_detector.py
│   ├── business_rules.py
│   ├── ai_summarizer.py
│   ├── email_alert.py
│   └── main.py
│
├── dashboard.py
├── config.py
├── generate_data.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── venv/
```

------------------------------------------------------------------------

# 19. Module Responsibilities

## `data_loader.py`

Responsible for:

-   Reading Excel files
-   Basic validation
-   Preparing the DataFrame

------------------------------------------------------------------------

## `anomaly_detector.py`

Responsible for:

-   Rolling baseline calculation
-   Percentage deviation
-   Z-score
-   Anomaly flag
-   Severity
-   Anomaly score

This module should contain the core quantitative logic.

------------------------------------------------------------------------

## `business_rules.py`

Responsible for:

-   Comparing related metrics
-   Identifying meaningful business patterns
-   Producing business insights

------------------------------------------------------------------------

## `ai_summarizer.py`

Responsible for:

-   Creating fallback summaries
-   Calling the AI model
-   Converting structured findings into natural language
-   Handling AI failures gracefully

------------------------------------------------------------------------

## `email_alert.py`

Responsible for:

-   Loading email configuration
-   Connecting to SMTP
-   Creating messages
-   Sending alerts
-   Returning success/failure status

------------------------------------------------------------------------

## `main.py`

Responsible for orchestrating the complete backend workflow:

``` text
Load
  |
Analyze
  |
Score
  |
Interpret
  |
Summarize
  |
Alert
  |
Report
```

------------------------------------------------------------------------

## `dashboard.py`

Responsible for:

-   User interface
-   File upload
-   KPI display
-   Charts
-   Anomaly table
-   Business insights
-   AI summary
-   Recommendations

------------------------------------------------------------------------

## `config.py`

Contains configurable parameters such as:

``` python
ROLLING_WINDOW
DEVIATION_THRESHOLD
ZSCORE_THRESHOLD
METRIC_WEIGHTS
OVERALL_RISK_THRESHOLD
```

Centralizing configuration makes the system easier to tune without
changing core code.

------------------------------------------------------------------------

# 20. Technology Stack

  Technology      Purpose
  --------------- -----------------------------------
  Python          Application logic
  Pandas          Data manipulation and analysis
  NumPy           Numerical operations
  OpenPyXL        Excel file support
  Streamlit       Interactive dashboard
  Plotly          Data visualization
  OpenAI API      Natural-language business summary
  python-dotenv   Environment configuration
  SMTP            Email delivery
  Git             Version control
  GitHub          Source-code hosting

------------------------------------------------------------------------

# 21. Installation

## Step 1: Clone the repository

``` bash
git clone <repository-url>
cd AI-Anomaly-Agent
```

## Step 2: Create virtual environment

``` bash
python -m venv venv
```

## Step 3: Activate it on Windows

``` bash
venv\Scripts\activate
```

## Step 4: Install dependencies

``` bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet complete:

``` bash
pip install pandas openpyxl numpy streamlit plotly python-dotenv openai
```

## Step 5: Configure environment variables

Create:

``` text
.env
```

and populate it using `.env.example` as a reference.

------------------------------------------------------------------------

# 22. Running the Backend

From the project root:

``` bash
python -m src.main
```

The backend performs:

``` text
Load Excel
   |
Analyze metrics
   |
Calculate risk
   |
Generate business insights
   |
Generate AI summary
   |
Send alert if threshold is crossed
   |
Save anomaly report
```

------------------------------------------------------------------------

# 23. Running the Dashboard

Run:

``` bash
streamlit run dashboard.py
```

The Streamlit application will provide the browser-based interface.

------------------------------------------------------------------------

# 24. Expected Output

A successful backend execution should produce output similar to:

``` text
============================================================
AI ANOMALY MONITORING AGENT
============================================================

Latest Date: 2026-08-11

LATEST METRIC ANALYSIS
------------------------------------------------------------

Metric: Revenue
Current Value : 75000.00
Baseline      : 120000.00
Deviation     : -37.50%
Z-Score       : -3.80
Severity      : Critical
Anomaly Score : 90.00
Status        : ANOMALY

...

============================================================
BUSINESS INSIGHTS
============================================================

• Traffic increased significantly while conversion rate
  declined and revenue decreased.

============================================================
BUSINESS SUMMARY
============================================================

Revenue declined significantly despite increased traffic...
```

If the risk threshold is crossed and email configuration is valid:

``` text
Email alert sent successfully.
```

The report is saved to:

``` text
reports/anomaly_report.csv
```

------------------------------------------------------------------------

# 25. Testing Strategy

A senior-engineering approach should test more than the happy path.

## Test Case 1 --- Normal data

Expected:

``` text
No significant anomalies
No high-risk email
```

## Test Case 2 --- Revenue drops sharply

Expected:

``` text
Revenue anomaly
High/Critical severity
```

## Test Case 3 --- Traffic increases but conversion falls

Expected:

``` text
Traffic anomaly
Conversion anomaly
Business insight about traffic quality/funnel
```

## Test Case 4 --- Refunds increase sharply

Expected:

``` text
Refund anomaly
Investigation recommendation
```

## Test Case 5 --- Missing environment variables

Expected:

``` text
Graceful configuration error
Application should not expose secrets
```

## Test Case 6 --- AI unavailable

Expected:

``` text
Fallback summary
Core anomaly detection continues
```

## Test Case 7 --- Invalid Excel file

Expected:

``` text
Clear validation error
No silent failure
```

------------------------------------------------------------------------

# 26. Security Considerations

The project handles credentials, so security is important.

### Never do this:

``` python
EMAIL_PASSWORD = "mypassword123"
```

### Never commit:

``` text
.env
```

### Never expose:

-   Gmail App Password
-   OpenAI API key
-   SMTP credentials

Use environment variables.

The repository should contain:

``` text
.env.example
```

but not:

``` text
.env
```

------------------------------------------------------------------------

# 27. Design Decisions

## Why rolling average?

It is simple, interpretable and appropriate for a beginner-friendly
monitoring system.

## Why Z-score?

It provides a statistical measure of unusual behavior.

## Why both?

Percentage deviation communicates business magnitude, while Z-score
communicates statistical unusualness.

## Why rules before AI?

Rules are deterministic and explainable. AI is better suited for
summarization and communication.

## Why Streamlit?

It allows the analytical pipeline to be exposed as a usable application
without building a full frontend/backend stack.

## Why email?

Detection without notification still requires someone to manually check
the dashboard. Email makes the system proactive.

------------------------------------------------------------------------

# 28. Limitations

The current implementation has several limitations.

### 1. Limited historical depth

A seven-period baseline may not capture:

-   Weekly seasonality
-   Monthly seasonality
-   Holidays
-   Promotions
-   Long-term trends

### 2. Threshold sensitivity

Fixed thresholds such as:

``` text
20% deviation
Z-score 3
```

may not be optimal for every business metric.

### 3. Correlation is not causation

If:

``` text
Traffic ↑
Revenue ↓
```

the system can identify the pattern, but it cannot prove that traffic
quality caused the revenue decline.

### 4. AI can produce incorrect explanations

AI-generated explanations should be treated as hypotheses for
investigation, not verified business facts.

### 5. Excel is not a production data source

A production system would ideally consume data from:

-   SQL databases
-   Data warehouses
-   APIs
-   ETL pipelines
-   Cloud storage

------------------------------------------------------------------------

# 29. Future Improvements

A production-grade version could include:

## Advanced anomaly detection

-   Isolation Forest
-   Local Outlier Factor
-   Seasonal decomposition
-   Prophet
-   ARIMA
-   Robust statistical methods

## Seasonality

Automatically account for:

``` text
Daily
Weekly
Monthly
Yearly
```

patterns.

## Database

Store:

-   Historical metrics
-   Detected anomalies
-   Alert history
-   User feedback

using PostgreSQL or another production database.

## Automated scheduling

Run the monitoring process automatically:

``` text
Every morning
      |
Load latest data
      |
Analyze
      |
Alert if required
```

## Better alerting

Add:

-   Slack
-   Microsoft Teams
-   SMS
-   Webhooks

## Feedback loop

Allow analysts to mark alerts as:

``` text
True anomaly
False positive
Expected event
```

This feedback can be used to improve thresholds.

## Production deployment

Possible architecture:

``` text
Cloud Scheduler
      |
      v
Python Monitoring Service
      |
      v
Database / Data Warehouse
      |
      v
Anomaly Engine
      |
      +--------+
      |        |
      v        v
Dashboard   Alert Service
```

------------------------------------------------------------------------

# 30. Interview Explanation

A concise explanation:

> I built Anomaly Sentinel, an AI-powered business anomaly monitoring
> system. It reads Excel-based business metrics such as revenue, orders,
> traffic and conversion rate, calculates historical baselines, and
> detects unusual behavior using percentage deviation and Z-score
> analysis. It then assigns severity and risk scores. A business-rule
> layer analyzes relationships between metrics, while an AI layer
> converts those findings into a concise business explanation. The
> results are exposed through a Streamlit dashboard and high-risk
> situations trigger email alerts. The main goal is to move from static
> EDA toward proactive business monitoring.

------------------------------------------------------------------------

# 31. Why This Is Better Than a Standard EDA Project

A standard EDA project generally follows:

``` text
Load
  |
Explore
  |
Visualize
  |
Explain
```

Anomaly Sentinel follows:

``` text
Load
  |
Monitor
  |
Detect
  |
Prioritize
  |
Interpret
  |
Explain
  |
Alert
```

The second workflow is closer to an operational analytics use case.

------------------------------------------------------------------------

# 32. Portfolio Value

This project demonstrates multiple skills in one system:

### Data Analysis

-   Pandas
-   Statistical analysis
-   Baselines
-   Z-score
-   Metric comparison

### Software Engineering

-   Modular Python architecture
-   Configuration management
-   Error handling
-   Environment variables
-   Logging
-   Separation of concerns

### AI

-   LLM integration
-   Prompt design
-   AI-assisted summarization
-   Fallback handling

### Visualization

-   Streamlit
-   Plotly
-   KPI dashboards

### Automation

-   Email notifications
-   Alert logging
-   Automated anomaly reporting

### Business Thinking

-   Metric relationships
-   Risk prioritization
-   Investigation recommendations

------------------------------------------------------------------------

# 33. Project Success Criteria

The project is considered successful when:

-   [ ] Excel data loads successfully.
-   [ ] Data is validated and prepared.
-   [ ] Historical baselines are calculated.
-   [ ] Anomalies are detected correctly.
-   [ ] Severity is assigned.
-   [ ] Risk score is generated.
-   [ ] Business rules generate meaningful insights.
-   [ ] AI summary works when configured.
-   [ ] Fallback summary works when AI is unavailable.
-   [ ] Streamlit dashboard loads.
-   [ ] Excel upload works.
-   [ ] Anomaly report is generated.
-   [ ] High-risk email alerts work.
-   [ ] Alert history is logged.
-   [ ] Secrets are excluded from Git.
-   [ ] README documentation is complete.

------------------------------------------------------------------------

# 34. Final Architecture Summary

``` text
                 +----------------------+
                 |   Business Excel     |
                 |        Data          |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |    Data Loader       |
                 |       Pandas         |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Data Preprocessing   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Historical Baseline  |
                 |   Rolling Average    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Anomaly Detection    |
                 | Deviation + Z-score  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Severity + Risk      |
                 |       Score          |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Business Rules     |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |    AI Summarizer     |
                 +----------+-----------+
                            |
                  +---------+---------+
                  |                   |
                  v                   v
        +----------------+   +----------------+
        |   Streamlit    |   |  Email Alert   |
        |   Dashboard    |   |     SMTP       |
        +----------------+   +----------------+
                  |
                  v
        +----------------+
        | Analyst /      |
        | Decision Maker |
        +----------------+
```

------------------------------------------------------------------------

# 35. Final Takeaway

Anomaly Sentinel is not intended to be a replacement for a full
enterprise monitoring platform.

Its purpose is to demonstrate a practical engineering and analytics
workflow:

``` text
DATA
 ↓
STATISTICS
 ↓
ANOMALY DETECTION
 ↓
BUSINESS LOGIC
 ↓
AI INTERPRETATION
 ↓
VISUALIZATION
 ↓
AUTOMATED ALERTING
```

The key portfolio message is:

> **"I didn't just analyze the data. I built a system that watches the
> data, identifies unusual behavior, explains why it may matter, and
> alerts someone when action may be required."**
