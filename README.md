# EDUPRO_2.0_Modern_UI
EDUPRO 2.0 — Predictive Intelligence for Education

<p align="center">
  <strong>A machine-learning dashboard for exploring course demand and revenue forecasts.</strong>
</p>

<p align="center">
  <a href="https://utkarsh-sengar-edupro-2.streamlit.app/">Live Demo</a>
  ·
  <a href="https://github.com/Utkarsh-sengar3/EDUPRO_2.0">GitHub Repository</a>
</p>

Live Demo

Try EDUPRO: https://utkarsh-sengar-edupro-2.streamlit.app/

EDUPRO is a predictive analytics application built to explore how historical education/course data can support demand forecasting, revenue analysis, and data-informed planning.

Overview

The project brings data exploration, machine-learning predictions, forecasting, and model evaluation together in an interactive Streamlit application. It is designed to make analytical results easier to inspect through charts, metrics, and interactive controls.

Features

Executive overview — a summary of available course and forecasting information.

Exploratory data analysis — explore patterns and relationships in the available dataset.

Demand prediction — generate demand estimates using the project's trained model and supported inputs.

Revenue forecasting — inspect revenue forecasts and, where available, test scenario assumptions.

Category analysis — compare course categories using the available data.

Model performance — review model evaluation results and diagnostic visualizations.

Feature importance — inspect the features associated with the model's predictions.

Dark/light appearance — switch the interface theme.

Research and project information — review the project methodology and development context.

Note: Forecasts are model estimates, not guarantees of future enrollment or revenue. Results depend on the dataset, feature definitions, and validation approach used by the project.

Technology Stack

Python

Streamlit — interactive web application

Pandas / NumPy — data processing

Scikit-learn — machine-learning workflows

Plotly — interactive visualizations

Joblib — loading serialized model artifacts, where used

Run Locally

1. Clone the repository

git clone https://github.com/Utkarsh-sengar3/EDUPRO_3.0.git
cd EDUPRO_3.0

2. Create and activate a virtual environment

Windows (Command Prompt):

python -m venv venv
venv\Scripts\activate

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

4. Start the application

streamlit run app.py

Open the local URL printed in the terminal, usually http://localhost:8501.

Repository Notes

The application may rely on local datasets and trained model artifacts. Make sure all required files are available in your local project before running it.

For a public repository, only publish datasets, model artifacts, notebooks, and documentation that you are authorized to share. If any source data was provided by an internship company, keep it private unless you have explicit permission to publish it. Never commit API keys, passwords, access tokens, .env files, or Streamlit secrets.

Developer

Utkarsh Sengar

AI/ML Engineering Student | Machine Learning & Data Analytics

I work on applied machine-learning projects that combine data processing, model evaluation, predictive analytics, and usable interfaces. EDUPRO is a project exploring how education-related data can be transformed into forecasts and insights that support better planning.

Areas of focus

Machine learning and predictive modelling

Data analysis and visualization

Python application development

Model evaluation and explainability

Building practical interfaces for data-driven workflows

Profiles

GitHub: https://github.com/Utkarsh-sengar3

LinkedIn: https://www.linkedin.com/in/utkarsh-sengar-a995a4334/?isSelfProfile=true

Project Workflow

Data
  ↓
Exploratory Analysis
  ↓
Feature Preparation
  ↓
Model Training / Evaluation
  ↓
Demand & Revenue Forecasting
  ↓
Interactive Analytics

Limitations

Predictions depend on the quality, coverage, and relevance of the available historical data.

Model outputs should be interpreted alongside evaluation metrics and domain knowledge.

This application is an analytical prototype; its forecasts should not be treated as guaranteed business outcomes.

Some pages or outputs may require local data and model artifacts that are not included in a public distribution.

Future Improvements

More comprehensive automated model monitoring

Stronger uncertainty estimates for forecasts

Expanded model explainability

Improved data validation and reproducible evaluation

Additional export and reporting options

License

No license is specified yet. Unless a license is added, standard copyright restrictions apply. Add a license only after confirming that you have the right to publish and license all included code and assets.

<p align="center">
  Built by <strong>Utkarsh Sengar</strong>
</p>
