import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64

# --- Streamlit Page Config ---
st.set_page_config(page_title="PFITT - Potential Flow Tool", layout="centered")

# --- Logo Function ---
def show_logo_centered(image_path, width=220):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"<div style='text-align: center;'><img src='data:image/png;base64,{encoded}' width='{width}'></div>",
            unsafe_allow_html=True,
        )

# --- Session State Initialization ---
if "entered" not in st.session_state:
    st.session_state["entered"] = False

# --- Front Page ---
if not st.session_state["entered"]:
    show_logo_centered("pfitt_logo.png")
    st.markdown("<h2 style='text-align: center;'>Potential Flow Interactive Teaching Tool</h2>", unsafe_allow_html=True)

    with st.expander("📘 Learn More about PFITT"):
        st.markdown("""
**PFITT** is a simulation tool designed for visualizing elementary potential flows including:
- Uniform Flow
- Source / Sink
- Vortex
- Doublet
- Superpositions (e.g., Rankine body, flow over cylinder)

Ideal for students learning fluid mechanics, PFITT helps explain streamline patterns and potential functions interactively.
        """)

    if st.button("🚀 Proceed to Simulation"):
        st.session_state["entered"] = True
        st.rerun()

    st.markdown("<hr><p style='text-align: center;'>Developed by A. Abd Razak & S. Suhaime – 2025</p>", unsafe_allow_html=True)
    st.stop()

# === Main Simulation Starts ===
st.markdown("## Potential Flow Interactive Teaching Tool (PFITT)")
st.markdown("Explore streamlines by selecting a predefined case or entering custom flow elements.")
st.markdown("---")

# --- Theory Dropdown (Clean Style) ---
with st.expander("📘 Theory: What Is Potential Flow?"):
    st.markdown(r"""
### ✨ Assumptions
- **Potential Flow** assumes:
  - Inviscid (no viscosity)
  - Incompressible
  - Irrotational

- **Velocity Potential (ϕ)** and **Stream Function (ψ)** satisfy Laplace’s Equation:

$$
\nabla^2 \phi = 0, \quad \nabla^2 \psi = 0
$$

---

### 💨 Elementary Flows

**Uniform Flow**

$$
u = U, \quad v = 0 \quad \Rightarrow \quad \psi = Uy, \quad \phi = Ux
$$

**Source / Sink**

$$
u = \frac{m}{2\pi} \frac{x}{r^2}, \quad v = \frac{m}{2\pi} \frac{y}{r^2}
$$

$$
\psi = \frac{m}{2\pi} \theta, \quad \phi = \frac{m}{2\pi} \ln r
$$

**Vortex**

$$
u = -\frac{\Gamma}{2\pi} \frac{y}{r^2}, \quad v = \frac{\Gamma}{2\pi} \frac{x}{r^2}
$$

$$
\psi = \frac{\Gamma}{2\pi} \ln r, \quad \phi = -\frac{\Gamma}{2\pi} \theta
$$

**Doublet**

$$
u = -\frac{K}{2\pi} \cdot \frac{x^2 - y^2}{r^4}, \quad v = -\frac{K}{2\pi} \cdot \frac{2xy}{r^4}
$$

$$
\psi = -\frac{K}{2\pi} \cdot \frac{y}{r^2}, \quad \phi = -\frac{K}{2\pi} \cdot \frac{x}{r^2}
$$

---

### 🧩 Superposition

- Combine flows by adding:

$$
u_{\text{total}}, \quad v_{\text{total}}, \quad \psi_{\text{total}}, \quad \phi_{\text{total}}
$$

- Examples:
  - **Rankine Half Body** = Uniform + Source  
  - **Flow over Cylinder** = Uniform + Doublet  
  - **Cylinder with Circulation** = Uniform + Doublet + Vortex

---

### 📝 Notes
- **Streamlines** (ψ = const) show flow paths  
- **Equipotential lines** (ϕ = const) are orthogonal to streamlines
""", unsafe_allow_html=True)

# --- Default Flow Values ---
flow_keys = {
    "U": 0.0,
    "source_strength": 0.0, "source_x": 0.0, "source_y": 0.0,
    "sink_strength": 0.0, "sink_x": 0.0, "sink_y": 0.0,
    "vortex_strength": 0.0, "vortex_x": 0.0, "vortex_y": 0.0,
    "doublet_strength": 0.0, "doublet_x": 0.0, "doublet_y": 0.0
}

case_options = {
    "Custom (Manual Input)": flow_keys,
    "Uniform Flow (Straight lines)": {"U": 2.0},
    "Source (Radial lines outward)": {"source_strength": 5.0},
    "Sink (Radial lines inward)": {"sink_strength": 5.0},
    "Vortex (Circular lines around origin)": {"vortex_strength": 5.0},
    "Doublet (Closed loops, stagnation line)": {"doublet_strength": 5.0},
    "Uniform + Source (Rankine half body)": {"U": 2.0, "source_strength": 5.0},
    "Uniform + Doublet (Around a cylinder)": {"U": 2.0, "doublet_strength": 5.0},
    "Uniform + Doublet + Vortex (Cylinder with circulation)": {"U": 2.0, "doublet_strength": 5.0, "vortex_strength": 5.0},
    "Uniform + Source + Sink (Rankine oval)": {"U": 2.0, "source_strength": 5.0, "source_x": -1.0, "sink_strength": 5.0, "sink_x": 1.0}
}

if "selected_case" not in st.session_state:
    st.session_state["selected_case"] = "Custom (Manual Input)"
    st.session_state.update(flow_keys)
if "reset_trigger" not in st.session_state:
    st.session_state["reset_trigger"] = False

# --- Select Case ---
selected_case = st.selectbox("Choose a predefined case:", list(case_options.keys()), index=list(case_options.keys()).index(st.session_state["selected_case"]))
if selected_case != st.session_state["selected_case"] or st.session_state["reset_trigger"]:
    st.session_state["selected_case"] = selected_case
    values = case_options[selected_case]
    for k in flow_keys:
        st.session_state[k] = values.get(k, 0.0)
    st.session_state["reset_trigger"] = False
    st.rerun()

# --- Inputs ---
st.markdown("### 🛠️ Flow Element Inputs")
st.number_input("Uniform Flow Speed (U)", key="U")

st.markdown("#### 🔵 Source and 🔻 Sink")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Source Settings**")
    st.number_input("Source Strength", key="source_strength")
    st.number_input("Source X Location", key="source_x")
    st.number_input("Source Y Location", key="source_y")
with col2:
    st.markdown("**Sink Settings**")
    st.number_input("Sink Strength", key="sink_strength")
    st.number_input("Sink X Location", key="sink_x")
    st.number_input("Sink Y Location", key="sink_y")

st.markdown("#### 🔁 Vortex")
st.number_input("Vortex Strength", key="vortex_strength")
st.number_input("Vortex X Location", key="vortex_x")
st.number_input("Vortex Y Location", key="vortex_y")

st.markdown("#### 💠 Doublet")
st.number_input("Doublet Strength", key="doublet_strength")
st.number_input("Doublet X Location", key="doublet_x")
st.number_input("Doublet Y Location", key="doublet_y")

# --- Options ---
st.markdown("### 📊 Optional Visualizations")
show_psi = st.checkbox("Show Stream Function ψ", value=False)
show_phi = st.checkbox("Show Potential Function ϕ", value=False)

# --- Buttons ---
st.markdown("### ▶️ Actions")
col_enter, col_reset = st.columns(2)
with col_enter:
    run = st.button("✅ Enter Simulation")
with col_reset:
    if st.button("🔁 Reset All to Zero"):
        st.session_state["selected_case"] = "Custom (Manual Input)"
        st.session_state["reset_trigger"] = True
        st.rerun()

# --- Simulation ---
if run:
    x = np.linspace(-4, 4, 200)
    y = np.linspace(-4, 4, 200)
    X, Y = np.meshgrid(x, y)

    u = st.session_state["U"] * np.ones_like(X)
    v = np.zeros_like(Y)
    psi = st.session_state["U"] * Y
    phi = st.session_state["U"] * X

    def safe_r(xc, yc):
        r2 = (X - xc)**2 + (Y - yc)**2
        r2[r2 < 1e-5] = 1e-5
        return r2

    fig1, ax1 = plt.subplots(figsize=(6, 6))
    description_parts = ["This graph shows the streamlines of the fluid flow, indicating the path that fluid particles follow.",
                         "The color represents flow speed—brighter colors mean higher speed."]

    if st.session_state["source_strength"] != 0.0:
        r2 = safe_r(st.session_state["source_x"], st.session_state["source_y"])
        dx = X - st.session_state["source_x"]
        dy = Y - st.session_state["source_y"]
        u += (st.session_state["source_strength"] / (2 * np.pi)) * dx / r2
        v += (st.session_state["source_strength"] / (2 * np.pi)) * dy / r2
        psi += (st.session_state["source_strength"] / (2 * np.pi)) * np.arctan2(dy, dx)
        phi += (st.session_state["source_strength"] / (4 * np.pi)) * np.log(r2)
        ax1.plot(st.session_state["source_x"], st.session_state["source_y"], 'bo', label="Source")
        description_parts.append("Blue dots represent sources where fluid emanates outward.")

    if st.session_state["sink_strength"] != 0.0:
        r2 = safe_r(st.session_state["sink_x"], st.session_state["sink_y"])
        dx = X - st.session_state["sink_x"]
        dy = Y - st.session_state["sink_y"]
        u -= (st.session_state["sink_strength"] / (2 * np.pi)) * dx / r2
        v -= (st.session_state["sink_strength"] / (2 * np.pi)) * dy / r2
        psi -= (st.session_state["sink_strength"] / (2 * np.pi)) * np.arctan2(dy, dx)
        phi -= (st.session_state["sink_strength"] / (4 * np.pi)) * np.log(r2)
        ax1.plot(st.session_state["sink_x"], st.session_state["sink_y"], 'ro', label="Sink")
        description_parts.append("Red dots represent sinks where fluid converges inward.")

    if st.session_state["vortex_strength"] != 0.0:
        r2 = safe_r(st.session_state["vortex_x"], st.session_state["vortex_y"])
        dx = X - st.session_state["vortex_x"]
        dy = Y - st.session_state["vortex_y"]
        u += -(st.session_state["vortex_strength"] / (2 * np.pi)) * dy / r2
        v +=  (st.session_state["vortex_strength"] / (2 * np.pi)) * dx / r2
        psi += (st.session_state["vortex_strength"] / (2 * np.pi)) * np.log(np.sqrt(r2))
        phi += -(st.session_state["vortex_strength"] / (2 * np.pi)) * np.arctan2(dy, dx)
        ax1.plot(st.session_state["vortex_x"], st.session_state["vortex_y"], 'mo', label="Vortex")
        description_parts.append("Magenta dots represent vortices where the flow circulates.")

    if st.session_state["doublet_strength"] != 0.0:
        r2 = safe_r(st.session_state["doublet_x"], st.session_state["doublet_y"])
        dx = X - st.session_state["doublet_x"]
        dy = Y - st.session_state["doublet_y"]
        u -= (st.session_state["doublet_strength"] / (2 * np.pi)) * (dx**2 - dy**2) / (r2**2)
        v -= (st.session_state["doublet_strength"] / (2 * np.pi)) * (2 * dx * dy) / (r2**2)
        psi -= (st.session_state["doublet_strength"] / (2 * np.pi)) * dy / r2
        phi -= (st.session_state["doublet_strength"] / (2 * np.pi)) * dx / r2
        ax1.plot(st.session_state["doublet_x"], st.session_state["doublet_y"], 'go', label="Doublet")
        description_parts.append("Green dots represent doublets, modeling flow around bodies.")

    speed = np.sqrt(u**2 + v**2)
    ax1.streamplot(X, Y, u, v, color=speed, linewidth=1, cmap='coolwarm')
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect("equal")
    ax1.set_title("Velocity Field Streamlines")
    ax1.legend()
    st.pyplot(fig1)
    st.markdown("**Description**: " + " ".join(description_parts))

    if show_psi:
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        cs = ax2.contour(X, Y, psi, levels=50, cmap="viridis")
        ax2.clabel(cs, inline=True, fontsize=8)
        ax2.set_title("Stream Function ψ")
        ax2.set_xlim(-4, 4)
        ax2.set_ylim(-4, 4)
        ax2.set_aspect("equal")
        st.pyplot(fig2)

    if show_phi:
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        cp = ax3.contour(X, Y, phi, levels=50, cmap="plasma")
        ax3.clabel(cp, inline=True, fontsize=8)
        ax3.set_title("Potential Function ϕ")
        ax3.set_xlim(-4, 4)
        ax3.set_ylim(-4, 4)
        ax3.set_aspect("equal")
        st.pyplot(fig3)

    if show_psi and show_phi:
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        cs1 = ax4.contour(X, Y, psi, levels=25, colors='blue', linewidths=1)
        cs2 = ax4.contour(X, Y, phi, levels=25, colors='green', linestyles='--', linewidths=1)
        ax4.clabel(cs1, inline=True, fontsize=8)
        ax4.clabel(cs2, inline=True, fontsize=8)
        ax4.set_title("Overlay of Stream Function (ψ) and Potential Function (ϕ)")
        ax4.set_xlim(-4, 4)
        ax4.set_ylim(-4, 4)
        ax4.set_aspect("equal")
        st.pyplot(fig4)

    # Footer on simulation page
    st.markdown("<hr><p style='text-align: center;'>Developed by A. Abd Razak & S. Suhaime – 2025</p>", unsafe_allow_html=True)
