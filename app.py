import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Monte Carlo Simulation for Air Quality (PM2.5)")

# Input sliders
mean_sensor = st.slider("Mean Sensor Value (µg/m³)", 30, 60, 40)
unc_sensor = st.slider("Sensor Uncertainty (σ)", 1, 10, 3)
unc_temporal = st.slider("Temporal Uncertainty (σ)", 1, 10, 2)
unc_spatial = st.slider("Spatial Uncertainty (σ)", 1, 5, 1)
n_runs = st.slider("Number of Runs", 1000, 50000, 10000)

# Correlation sliders
corr_sensor_temporal = st.slider("Correlation: Sensor vs Temporal", 0.0, 1.0, 0.6)
corr_sensor_spatial = st.slider("Correlation: Sensor vs Spatial", 0.0, 1.0, 0.3)
corr_temporal_spatial = st.slider("Correlation: Temporal vs Spatial", 0.0, 1.0, 0.2)

# -----------------------------
# Monte Carlo Simulation
# -----------------------------
means = [mean_sensor, 0, 0]

var_sensor = unc_sensor**2
var_temporal = unc_temporal**2
var_spatial = unc_spatial**2

cov_sensor_temporal = corr_sensor_temporal * (unc_sensor * unc_temporal)
cov_sensor_spatial = corr_sensor_spatial * (unc_sensor * unc_spatial)
cov_temporal_spatial = corr_temporal_spatial * (unc_temporal * unc_spatial)

cov_matrix = [
    [var_sensor, cov_sensor_temporal, cov_sensor_spatial],
    [cov_sensor_temporal, var_temporal, cov_temporal_spatial],
    [cov_sensor_spatial, cov_temporal_spatial, var_spatial]
]

samples = np.random.multivariate_normal(means, cov_matrix, n_runs)
sensor_samples = samples[:,0]
temporal_samples = samples[:,1]
spatial_samples = samples[:,2]

total_concentration = sensor_samples + temporal_samples + spatial_samples

# -----------------------------
# Results
# -----------------------------
mean_value = np.mean(total_concentration)
std_dev = np.std(total_concentration)
conf_interval = np.percentile(total_concentration, [2.5, 97.5])

limit = 40
prob_exceedance = np.mean(total_concentration > limit) * 100

st.subheader("Simulation Results")
st.write(f"**Mean concentration:** {mean_value:.
