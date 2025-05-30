import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Streamlit Page Config ---
st.set_page_config(page_title="Potential Flow Simulator", layout="centered")

# --- Page Title ---
st.markdown("## 💧 Potential Flow Simulator")
st.markdown("Explore streamlines for ideal flows: **Uniform Flow**, **Source**, **Sink**, and **Vortex**.")

st.markdown("---")
st.markdown("### 🛠️ Flow Element Inputs")

# === Uniform Flow ===
st.markdown("#### 🌬️ Uniform Flow")
U = st.slider("Uniform Flow Speed (U)", -5.0, 5.0, 1.0)

# === Source & Sink ===
st.markdown("#### 🔵 Source and 🔻 Sink")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Source Settings**")
    source_strength = st.slider("Source Strength", 0.0, 10.0, 5.0)
    source_x = st.number_input("Source X Location", value=-1.0)
    source_y = st.number_input("Source Y Location", value=0.0)

with col2:
    st.markdown("**Sink Settings**")
    sink_strength = st.slider("Sink Strength", 0.0, 10.0, 5.0)
    sink_x = st.number_input("Sink X Location", value=1.0)
    sink_y = st.number_input("Sink Y Location", value=0.0)

# === Vortex ===
st.markdown("#### 🔁 Vortex")
vortex_strength = st.slider("Vortex Strength", -10.0, 10.0, 0.0)
vortex_x = st.number_input("Vortex X Location", value=0.0)
vortex_y = st.number_input("Vortex Y Location", value=0.0)

# === Flow Field Grid ===
x = np.linspace(-4, 4, 100)
y = np.linspace(-4, 4, 100)
X, Y = np.meshgrid(x, y)

# === Velocity Components ===
u = U * np.ones_like(X)
v = np.zeros_like(Y)

# Source contribution
r_source = np.sqrt((X - source_x)**2 + (Y - source_y)**2)
u += (source_strength / (2 * np.pi)) * (X - source_x) / (r_source**2 + 1e-10)
v += (source_strength / (2 * np.pi)) * (Y - source_y) / (r_source**2 + 1e-10)

# Sink contribution
r_sink = np.sqrt((X - sink_x)**2 + (Y - sink_y)**2)
u -= (sink_strength / (2 * np.pi)) * (X - sink_x) / (r_sink**2 + 1e-10)
v -= (sink_strength / (2 * np.pi)) * (Y - sink_y) / (r_sink**2 + 1e-10)

# Vortex contribution
r_vortex = np.sqrt((X - vortex_x)**2 + (Y - vortex_y)**2)
u += -(vortex_strength / (2 * np.pi)) * (Y - vortex_y) / (r_vortex**2 + 1e-10)
v += (vortex_strength / (2 * np.pi)) * (X - vortex_x) / (r_vortex**2 + 1e-10)

# === Plot Streamlines ===
st.markdown("---")
st.markdown("### 🌀 Streamline Visualization")

fig, ax = plt.subplots(figsize=(6, 6))
speed = np.sqrt(u**2 + v**2)

# Streamplot with velocity magnitude color
stream = ax.streamplot(X, Y, u, v, color=speed, linewidth=1, cmap='coolwarm', arrowstyle='->')

# Mark flow elements
ax.scatter(source_x, source_y, color='red', label='Source', s=60)
ax.scatter(sink_x, sink_y, color='blue', label='Sink', s=60)
ax.scatter(vortex_x, vortex_y, color='green', label='Vortex', s=60)

# Lock axis and legend position
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Flow Field")

# Fixed position for legend
ax.legend(loc="upper right", frameon=True)

# Render plot
st.pyplot(fig)
