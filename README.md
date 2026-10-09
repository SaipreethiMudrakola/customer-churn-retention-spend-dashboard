<div align="center">

# 📡 Customer Churn & Retention Spend Dashboard

### Made by Sai Preethi

**SQL cohort analysis · Revenue at Risk · Dark-mode Streamlit UI**

A telecom retention intelligence dashboard that shows *where limited budget stops the most revenue leakage*.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![SQL](https://img.shields.io/badge/SQL-Cohorts-orange?style=for-the-badge)](#-sql-cohorts)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#-license)



[**[🚀 Live Dashboard](#)**](https://customer-churn-retention-spend-dashboard-saipreethi-m.streamlit.app/)

</div>

---

## ✨ Overview

Telecom teams don’t need more generic churn charts — they need a **spend decision system**.

This project turns the **Telco Customer Churn** dataset into:

| Capability | What you get |
|---|---|
| 🧮 **SQL cohorts** | Churn by contract, tenure, internet, payment |
| 💰 **Revenue at Risk** | `Σ MonthlyCharges` of churned customers |
| 📊 **Executive visuals** | KPI cards, bars, cohort heatmap |
| 📖 **Storytelling** | Real customer examples + retention plays |
| 🌙 **Dark-mode UI** | Clean, high-contrast Streamlit experience |

**Branding:** Made by Sai Preethi (header · sidebar · footer)

---

## 🔑 Key findings (from SQL)

| Insight | Result |
|---|---:|
| Overall churn | **26.54%** (1,869 / 7,043) |
| Month-to-month churn | **42.71%** |
| 1-year / 2-year churn | **11.27%** / **2.83%** |
| 3–6 month danger zone | **45.40%** |
| Electronic check churn | **45.29%** |
| Autopay churn | **15.98%** |
| Monthly revenue at risk | **$139,131** |
| Annualized revenue at risk | **~$1.67M** |

### Business decisions enabled
1. **Contract upgrade incentives** for month-to-month customers  
2. **Focus retention spend** on early tenure (especially 3–6 months)  
3. **Promote autopay adoption** among electronic-check users  


---

## 🧮 Formulas

```text
Churn Rate (%)  = (Churned Customers ÷ Total Customers) × 100
Revenue at Risk = Σ (Monthly Charges of Churned Customers)
Annual Risk     = Revenue at Risk × 12
```

---

## 🛠️ Tech stack

```text
SQL (SQLite)  →  cohort analysis
Python/Pandas →  cleaning & feature engineering
Plotly        →  interactive charts
Streamlit     →  dark-mode dashboard UI
GitHub        →  code hosting
Streamlit Cloud → live deployment
```

---

## 📁 Project structure

```text
customer-churn-dashboard/
│
├── app.py                                 # Streamlit dashboard (main file)
├── data_analysis.py                       # Cleaning + SQL cohorts + KPIs
├── requirements.txt                       # Dependencies for Cloud/local
├── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Dataset (required at runtime)
├── README.md                              # You are here
├── .gitignore                             # Blocks venv/cache/secrets
│
├── sql/
    └── cohort_queries.sql                 # Reference SQL queries
```

---

## ⚡ Quick start (local)

```powershell
# 1) Go to project folder
cd "....\customer-churn-retention-spend-dashboard"

# 2) (Recommended) create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install packages
pip install -r requirements.txt

# 4) Optional: print SQL cohort tables in terminal
python data_analysis.py

# 5) Launch dashboard
streamlit run app.py
```

Open **http://localhost:8501**

---


## 📊 Dashboard tabs

| Tab | Contents |
|---|---|
| **Overview** | Churn & revenue-at-risk bar charts by segment |
| **SQL Cohorts** | Full cohort tables from SQLite queries |
| **Cohort Heatmap** | Contract × tenure churn pressure map |
| **Storytelling & Decisions** | Findings, customer stories, retention plays |
| **Customer table** | Filterable explorer + CSV download |

---

---

## 🧾 Dataset credit

[Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (IBM sample / Kaggle mirror).

---

## 📄 License

MIT — free to use for learning and portfolio purposes.

---

<div align="center">

### Made by Sai Preethi

**Data-driven retention spend decisions**

`SQL` · `Pandas` · `Plotly` · `Streamlit` · `Cohort Analysis`

</div>
