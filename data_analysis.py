"""
Customer Churn & Retention Spend — data loading, cleaning, and SQL cohort analysis.
Uses SQLite for transparent, auditable cohort queries.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).resolve().parent / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

TENURE_BAND_ORDER = [
    "0–2 months",
    "3–6 months",
    "7–12 months",
    "13–24 months",
    "25–48 months",
    "49+ months",
]


def tenure_band(months: int) -> str:
    if months <= 2:
        return "0–2 months"
    if months <= 6:
        return "3–6 months"
    if months <= 12:
        return "7–12 months"
    if months <= 24:
        return "13–24 months"
    if months <= 48:
        return "25–48 months"
    return "49+ months"


def payment_group(method: str) -> str:
    if method in ("Bank transfer (automatic)", "Credit card (automatic)"):
        return "Autopay"
    if method == "Electronic check":
        return "Electronic check"
    return "Mailed check"


def load_and_clean(path: Path | str | None = None) -> pd.DataFrame:
    """Load Telco churn CSV and prepare analysis-ready columns."""
    csv_path = Path(path) if path else DATA_FILE
    df = pd.read_csv(csv_path)

    # TotalCharges is object because of blanks for tenure=0 new customers
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(0.0)

    df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)
    df["IsChurned"] = df["Churn"] == "Yes"
    df["tenure_band"] = df["tenure"].apply(tenure_band)
    df["payment_group"] = df["PaymentMethod"].apply(payment_group)
    df["AnnualRisk"] = df["MonthlyCharges"] * 12

    # Friendly labels for charts
    df["Contract"] = df["Contract"].replace(
        {"Month-to-month": "Month-to-month", "One year": "1-year", "Two year": "2-year"}
    )
    return df


def _to_sqlite(df: pd.DataFrame) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    # Keep a lean table for SQL analytics
    cols = [
        "customerID",
        "tenure",
        "tenure_band",
        "Contract",
        "InternetService",
        "PaymentMethod",
        "payment_group",
        "MonthlyCharges",
        "TotalCharges",
        "ChurnFlag",
        "AnnualRisk",
    ]
    df[cols].to_sql("customers", conn, index=False, if_exists="replace")
    return conn


def run_sql(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, conn)


def cohort_by_contract(conn: sqlite3.Connection) -> pd.DataFrame:
    q = """
    SELECT
        Contract AS segment,
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
        ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM customers
    GROUP BY Contract
    ORDER BY churn_rate_pct DESC
    """
    return run_sql(conn, q)


def cohort_by_tenure_band(conn: sqlite3.Connection) -> pd.DataFrame:
    q = """
    SELECT
        tenure_band AS segment,
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
        ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM customers
    GROUP BY tenure_band
    """
    df = run_sql(conn, q)
    df["segment"] = pd.Categorical(df["segment"], categories=TENURE_BAND_ORDER, ordered=True)
    return df.sort_values("segment").reset_index(drop=True)


def cohort_by_internet(conn: sqlite3.Connection) -> pd.DataFrame:
    q = """
    SELECT
        InternetService AS segment,
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
        ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM customers
    GROUP BY InternetService
    ORDER BY churn_rate_pct DESC
    """
    return run_sql(conn, q)


def cohort_by_payment(conn: sqlite3.Connection) -> pd.DataFrame:
    q = """
    SELECT
        payment_group AS segment,
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
        ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
    FROM customers
    GROUP BY payment_group
    ORDER BY churn_rate_pct DESC
    """
    return run_sql(conn, q)


def cohort_by_payment_detail(conn: sqlite3.Connection) -> pd.DataFrame:
    q = """
    SELECT
        PaymentMethod AS segment,
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk
    FROM customers
    GROUP BY PaymentMethod
    ORDER BY churn_rate_pct DESC
    """
    return run_sql(conn, q)


def contract_tenure_heatmap(conn: sqlite3.Connection) -> pd.DataFrame:
    """Cross-cohort: churn rate by contract × tenure band (for heatmap)."""
    q = """
    SELECT
        Contract,
        tenure_band,
        COUNT(*) AS total_customers,
        SUM(ChurnFlag) AS churned_customers,
        ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct
    FROM customers
    GROUP BY Contract, tenure_band
    """
    df = run_sql(conn, q)
    pivot = df.pivot(index="Contract", columns="tenure_band", values="churn_rate_pct")
    # Order columns
    ordered_cols = [c for c in TENURE_BAND_ORDER if c in pivot.columns]
    pivot = pivot[ordered_cols]
    # Order rows: m2m, 1y, 2y
    row_order = [r for r in ["Month-to-month", "1-year", "2-year"] if r in pivot.index]
    return pivot.reindex(row_order)


def compute_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    churned = int(df["ChurnFlag"].sum())
    retained = total - churned
    churn_rate = (churned / total * 100) if total else 0.0
    revenue_at_risk = float(df.loc[df["ChurnFlag"] == 1, "MonthlyCharges"].sum())
    annual_revenue_at_risk = revenue_at_risk * 12
    avg_churn_charge = float(df.loc[df["ChurnFlag"] == 1, "MonthlyCharges"].mean()) if churned else 0.0
    danger = df[df["tenure_band"] == "3–6 months"]
    danger_churn_rate = (
        float(danger["ChurnFlag"].mean() * 100) if len(danger) else 0.0
    )
    m2m = df[df["Contract"] == "Month-to-month"]
    m2m_churn = float(m2m["ChurnFlag"].mean() * 100) if len(m2m) else 0.0
    echeck = df[df["payment_group"] == "Electronic check"]
    echeck_churn = float(echeck["ChurnFlag"].mean() * 100) if len(echeck) else 0.0
    autopay = df[df["payment_group"] == "Autopay"]
    autopay_churn = float(autopay["ChurnFlag"].mean() * 100) if len(autopay) else 0.0

    return {
        "total_customers": total,
        "churned_customers": churned,
        "retained_customers": retained,
        "churn_rate_pct": round(churn_rate, 2),
        "revenue_at_risk": round(revenue_at_risk, 2),
        "annual_revenue_at_risk": round(annual_revenue_at_risk, 2),
        "avg_churn_monthly_charge": round(avg_churn_charge, 2),
        "danger_zone_churn_pct": round(danger_churn_rate, 2),
        "m2m_churn_pct": round(m2m_churn, 2),
        "echeck_churn_pct": round(echeck_churn, 2),
        "autopay_churn_pct": round(autopay_churn, 2),
    }


def storytelling_examples(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Pick concrete churned-customer examples for narrative storytelling."""
    churned = df[df["ChurnFlag"] == 1].copy()
    # Prefer danger-zone + high monthly charge stories
    danger = churned[churned["tenure_band"] == "3–6 months"].nlargest(2, "MonthlyCharges")
    m2m_hi = churned[churned["Contract"] == "Month-to-month"].nlargest(2, "MonthlyCharges")
    echeck_hi = churned[churned["payment_group"] == "Electronic check"].nlargest(2, "MonthlyCharges")
    sample = pd.concat([danger, m2m_hi, echeck_hi]).drop_duplicates("customerID").head(n)
    sample = sample[
        [
            "customerID",
            "tenure",
            "tenure_band",
            "Contract",
            "InternetService",
            "PaymentMethod",
            "MonthlyCharges",
            "AnnualRisk",
        ]
    ].reset_index(drop=True)
    sample["story"] = sample.apply(
        lambda r: (
            f"Customer {r['customerID']} churned at month {int(r['tenure'])} "
            f"({r['tenure_band']}) on a {r['Contract']} plan with "
            f"${r['MonthlyCharges']:.2f}/mo → ${r['AnnualRisk']:.2f} annual revenue at risk."
        ),
        axis=1,
    )
    return sample


def empty_analysis_result(df: pd.DataFrame | None = None) -> dict:
    """Safe empty payload when filters match zero rows."""
    empty_cols = [
        "segment",
        "total_customers",
        "churned_customers",
        "churn_rate_pct",
        "revenue_at_risk",
        "avg_monthly_charge",
        "annual_revenue_at_risk",
    ]
    empty_cohort = pd.DataFrame(columns=empty_cols)
    empty_detail = pd.DataFrame(
        columns=["segment", "total_customers", "churned_customers", "churn_rate_pct", "revenue_at_risk"]
    )
    base_df = df if df is not None else pd.DataFrame()
    return {
        "df": base_df,
        "kpis": {
            "total_customers": 0,
            "churned_customers": 0,
            "retained_customers": 0,
            "churn_rate_pct": 0.0,
            "revenue_at_risk": 0.0,
            "annual_revenue_at_risk": 0.0,
            "avg_churn_monthly_charge": 0.0,
            "danger_zone_churn_pct": 0.0,
            "m2m_churn_pct": 0.0,
            "echeck_churn_pct": 0.0,
            "autopay_churn_pct": 0.0,
        },
        "by_contract": empty_cohort.copy(),
        "by_tenure": empty_cohort.copy(),
        "by_internet": empty_cohort.copy(),
        "by_payment": empty_cohort.copy(),
        "by_payment_detail": empty_detail.copy(),
        "heatmap": pd.DataFrame(),
        "stories": pd.DataFrame(
            columns=[
                "customerID",
                "tenure",
                "tenure_band",
                "Contract",
                "InternetService",
                "PaymentMethod",
                "MonthlyCharges",
                "AnnualRisk",
                "story",
            ]
        ),
    }


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """Run KPIs + SQL cohorts on an already-cleaned (optionally filtered) frame."""
    if df is None or len(df) == 0:
        return empty_analysis_result(df if df is not None else pd.DataFrame())

    conn = _to_sqlite(df)
    try:
        result = {
            "df": df,
            "kpis": compute_kpis(df),
            "by_contract": cohort_by_contract(conn),
            "by_tenure": cohort_by_tenure_band(conn),
            "by_internet": cohort_by_internet(conn),
            "by_payment": cohort_by_payment(conn),
            "by_payment_detail": cohort_by_payment_detail(conn),
            "heatmap": contract_tenure_heatmap(conn),
            "stories": storytelling_examples(df),
        }
    finally:
        conn.close()
    return result


def build_analysis(path: Path | str | None = None) -> dict:
    """End-to-end pipeline used by the Streamlit app (full dataset)."""
    df = load_and_clean(path)
    return analyze_dataframe(df)


if __name__ == "__main__":
    analysis = build_analysis()
    k = analysis["kpis"]
    print("KPIs:", k)
    print("\nContract cohort:\n", analysis["by_contract"].to_string(index=False))
    print("\nTenure cohort:\n", analysis["by_tenure"].to_string(index=False))
    print("\nInternet cohort:\n", analysis["by_internet"].to_string(index=False))
    print("\nPayment cohort:\n", analysis["by_payment"].to_string(index=False))
