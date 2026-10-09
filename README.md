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

**[🚀 Live Dashboard](#)** · **[📘 Deployment Guide](docs/05_DEPLOYMENT_GUIDE.md)** · **[📖 Case Study](docs/01_case_study_storytelling.md)**

> 🔗 After deploy, replace the Live Dashboard `#` with your Streamlit Cloud URL  
> Example: `https://your-app-name.streamlit.app`

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

### Storytelling example
> Customer A churned in **month 4** with a **$70** monthly charge → **$840** annual revenue at risk.  
> A $90 upgrade incentive that saves them returns roughly **9×** on that single account.

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
│   └── cohort_queries.sql                 # Reference SQL queries
│
└── docs/
    ├── 01_case_study_storytelling.md      # Business narrative
    ├── 02_project_overview.md             # Dataset + formulas + flow
    ├── 03_technology_execution.md         # Stack + runbook
    ├── 04_polishing.md                    # Portfolio positioning
    └── 05_DEPLOYMENT_GUIDE.md             # GitHub + Streamlit deploy help
```

### What goes to GitHub?

| Upload ✅ | Do **not** upload ❌ |
|---|---|
| `app.py`, `data_analysis.py` | `.venv/` / `venv/` |
| `requirements.txt` | `__pycache__/` |
| Dataset CSV | `.streamlit/secrets.toml` |
| `README.md`, `docs/`, `sql/` | Local exports (`filtered_customers.csv`) |
| `.gitignore` | Editor/OS junk |

Full details → **[docs/05_DEPLOYMENT_GUIDE.md](docs/05_DEPLOYMENT_GUIDE.md)**

---

## ⚡ Quick start (local)

```powershell
# 1) Go to project folder
cd "D:\001sep\dep projects\customer churn dashboard"

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

## 🚀 Deploy (short version)

### 1) Push to GitHub
```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/customer-churn-dashboard.git
git push -u origin main
```

### 2) Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub  
2. **New app** → select this repository  
3. Branch: `main`  
4. **Main file path:** `app.py`  
5. Click **Deploy**  
6. Copy the public URL into this README  

**Need the full checklist (must-upload files, do-not-upload list, troubleshooting)?**  
→ Read **[Deployment Guide](docs/05_DEPLOYMENT_GUIDE.md)**

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

## 📚 Documentation

| Document | Use it for |
|---|---|
| [🚀 Deployment Guide](docs/05_DEPLOYMENT_GUIDE.md) | What to upload, what to skip, GitHub + Cloud steps |
| [📖 Case Study & Storytelling](docs/01_case_study_storytelling.md) | Business context & interview narrative |
| [🔎 Project Overview](docs/02_project_overview.md) | Dataset, formulas, project flow |
| [🛠️ Technology & Execution](docs/03_technology_execution.md) | Stack details & runbook |
| [✨ Polishing](docs/04_polishing.md) | Portfolio / LinkedIn positioning |

---

## 🎯 Portfolio one-liner

> Built a dark-mode Streamlit churn dashboard with SQL cohort analysis that quantifies **$139K+/month revenue at risk** and prioritizes telecom retention spend by contract, tenure, internet service, and payment method.

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
