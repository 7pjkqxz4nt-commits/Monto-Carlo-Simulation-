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
st.write(f"**Mean concentration:** {mean_value:.2f} µg/m³")
st.write(f"**Standard deviation:** {std_dev:.2f} µg/m³")
st.write(f"**95% Confidence Interval:** {conf_interval[0]:.2f} – {conf_interval[1]:.2f} µg/m³")
st.write(f"**Probability of exceeding {limit} µg/m³:** {prob_exceedance:.2f}%")

# -----------------------------
# Visualization
# -----------------------------
fig, ax = plt.subplots()
ax.hist(total_concentration, bins=50, color='skyblue', edgecolor='black')
ax.axvline(limit, color='red', linestyle='--', label=f'Limit = {limit} µg/m³')
ax.axvline(mean_value, color='green', linestyle='-', label=f'Mean = {mean_value:.2f}')
ax.set_title("Monte Carlo Simulation with Correlated Uncertainties")
ax.set_xlabel("Concentration (µg/m³)")
ax.set_ylabel("Frequency")
ax.legend()
st.pyplot(fig)

# -----------------------------
# AI Insights Block
# -----------------------------
def ai_insights(mean_value, std_dev, prob_exceedance, limit, correlations):
    insights = []
    if prob_exceedance > 50:
        insights.append(f"⚠️ High risk: More than {prob_exceedance:.1f}% of scenarios exceed the {limit} µg/m³ limit.")
    else:
        insights.append(f"✅ Moderate risk: Only {prob_exceedance:.1f}% exceed the {limit} µg/m³ limit.")

    if correlations['sensor_temporal'] > 0.5:
        insights.append("Strong correlation between sensor calibration and temporal variability increases exceedance probability.")
    if std_dev > 5:
        insights.append("Wide spread of outcomes indicates high uncertainty in monitoring results.")
    else:
        insights.append("Uncertainty is relatively contained, suggesting stable monitoring conditions.")

    return "\n".join(insights)

correlations = {
    'sensor_temporal': corr_sensor_temporal,
    'sensor_spatial': corr_sensor_spatial,
    'temporal_spatial': corr_temporal_spatial
}

st.subheader("AI Insights")
st.text(ai_insights(mean_value, std_dev, prob_exceedance, limit, correlations))
