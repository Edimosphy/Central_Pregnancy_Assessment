import plotly.graph_objs as go
import pandas as pd

def plot_monthly_risks(risk_data):
    # Convert anc_date to month name
    months = [
        pd.to_datetime(r.get('anc_date', ''), errors='coerce').strftime('%b')
        if r.get('anc_date') else ''
        for r in risk_data
    ]
    weeks_pregnant = [r.get('weeks_pregnant', 0) for r in risk_data]
    bp = [r.get('high_bp', 0) for r in risk_data]
    systolic_bp = [r.get('SystolicBP', 0) for r in risk_data]
    diastolic_bp = [r.get('DiastolicBP', 0) for r in risk_data]
    heartrate = [r.get('HeartRate', 0) for r in risk_data]
    body_weight = [r.get('body_weight', 0) for r in risk_data]
    body_temp = [r.get('body_temp', 0) for r in risk_data]
    blood_sugar = [r.get('BS', 0) for r in risk_data]

    # Convert ENUMs to numeric for plotting
    diabetes = [1 if r.get('diabetes') == 'yes' else 0 for r in risk_data]
    protein_urine = [1 if r.get('protein_urine') == 'yes' else 0 for r in risk_data]
    # Map fetal_movement to numbers (example mapping)
    fetal_movement_map = {
        'normal_pattern': 0,
        'no_movement': 1,
        'reduced_movement': 2,
        'fast_movement': 3
    }
    fetal_movement = [
        fetal_movement_map.get(r.get('fetal_movement', ''), 0) for r in risk_data
    ]
    other_tests = [r.get('other_clinical_tests', 0) for r in risk_data]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="BP", x=months, y=bp))
    fig.add_trace(go.Bar(name="Weeks Pregnant", x=months, y=weeks_pregnant))
    fig.add_trace(go.Bar(name="Diabetes", x=months, y=diabetes))
    fig.add_trace(go.Bar(name="Blood Sugar", x=months, y=blood_sugar))
    fig.add_trace(go.Bar(name="Heart Rate", x=months, y=heartrate))
    fig.add_trace(go.Bar(name="Body Weight", x=months, y=body_weight))
    fig.add_trace(go.Bar(name="Body Temp", x=months, y=body_temp))
    fig.add_trace(go.Bar(name="Protein Urine", x=months, y=protein_urine))
    fig.add_trace(go.Bar(name="Systolic BP", x=months, y=systolic_bp))
    fig.add_trace(go.Bar(name="Diastolic BP", x=months, y=diastolic_bp))
    fig.add_trace(go.Bar(name="Fetal Movement", x=months, y=fetal_movement))
    fig.add_trace(go.Bar(name="Other Tests", x=months, y=other_tests))

    fig.update_layout(barmode='group', title="Monthly Risk Exposure")
    return fig

def plot_weekly_antenatal_visits(attended):
    weeks = [v.get('week', '') for v in attended]
    visits = [v.get('visits', 0) for v in attended]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=weeks, y=visits, name="Antenatal Visits"))

    fig.update_layout(
        title="Weekly Antenatal Visits",
        xaxis_title="Week",
        yaxis_title="Number of Visits"
    )
    return fig