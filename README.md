# PIE (Personal Inflation Engine)
Personal Inflation Engine for analyzing customized inflation metrics.

## Overview
PIE computes monthly personal inflation rates based on individual transaction histories and Consumer Price Index (CPI) data. It allows users to understand how macroeconomic inflation affects their specific spending habits.

## Architecture & Tools
- **Core Engine**: Python, Pandas, NumPy
- **Visualizations / Dashboard**: Streamlit, Plotly
- **Data**: Mock transaction data and raw CPI indices

## Installation

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### 1. Terminal Demo
Run the core engine logic and print the results to the terminal:
```bash
python3 run_demo.py
```

### 2. Interactive Web Dashboard
Launch the interactive Streamlit application to visualize inflation rates and spending category weights dynamically:
```bash
streamlit run streamlit_app.py
```
After running the command, your browser will automatically open the dashboard (usually at `http://localhost:8501`).
