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

# ✅ Define float input helper here
def safe_float_input(label, default="1.0", key=None):
    raw = st.text_input(label, default, key=key)
    try:
        return float(raw)
    except ValueError:
        st.warning(f"⚠️ Please enter a valid number for {label}.")
        return 0.0

# --- Session State Initialization ---
if "entered" not in st.session_state:
    st.session_state["entered"] = False
if "entered_simulation" not in st.session_state:
    st.session_state["entered_simulation"] = False
if "show_point_output" not in st.session_state:
    st.session_state["show_point_output"] = False

# --- Front Page ---
if not st.session_state["entered"]:
    show_logo_centered("pfitt_logo.png")
    st.markdown("<h2 style='text-align: center;'>Potential Flow Interactive Teaching Tool</h2>", unsafe_allow_html=True)

    with st.expander("📘 Learn More about PFITT"):
        st.markdown("""
**PFITT** (Potential Flow Interactive Teaching Tool) is a web-based simulation platform developed to help students understand the fundamentals of inviscid, incompressible, and irrotational flow in fluid mechanics. It allows users to visualize classical *potential flow patterns* interactively through various elementary flow elements.

🔹 **Key Flow Elements Visualized**:
- **Uniform Flow** – Represents constant straight-line flow across the domain.
- **Source / Sink** – Models radial outward (source) or inward (sink) flow centered at a point.
- **Vortex** – Simulates circular motion around a central point to represent rotational flow behavior.
- **Doublet** – Used to model flow around objects such as cylinders or stagnation points.

🔹 **Superposition Capabilities**:
PFITT supports **superposition of flows**, allowing users to combine multiple elements to form complex patterns like:
- **Rankine Half Body** = Uniform Flow + Source  
- **Flow Over a Cylinder** = Uniform Flow + Doublet  
- **Cylinder with Circulation** = Uniform Flow + Doublet + Vortex  
- **Rankine Oval** = Uniform Flow + Source + Sink

🎯 **Educational Purpose**:
- Designed for **students and educators** in fluid mechanics.
- Helps illustrate how **streamlines (ψ)** and **potential lines (ϕ)** interact.
- Makes abstract theory **tangible and engaging** through visual learning.

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

# --- Theory Dropdown (Precise, Structured Style) ---
with st.expander("📘 Theory: What Is Potential Flow?"):
    st.markdown(r"""
🔵 **GENERAL CONCEPTS**

**1. Stream Function (ψ) and Velocity Potential (φ)**  
For incompressible 2D flow:  
$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0
$$

Stream function definition:  
$$
u = \frac{\partial \psi}{\partial y}, \quad v = -\frac{\partial \psi}{\partial x}
$$

Velocity potential definition:  
$$
u = \frac{\partial \phi}{\partial x}, \quad v = \frac{\partial \phi}{\partial y}
$$

Orthogonality:  
$$
\nabla \phi \cdot \nabla \psi = 0
$$

Both ψ and φ satisfy the Laplace equation:  
$$
\nabla^2 \psi = 0, \quad \nabla^2 \phi = 0
$$

---

🔶 **ELEMENTARY PLANE IRROTATIONAL FLOWS**

**2. Uniform Flow (in x-direction or at angle α)**  
Velocity components:  
$$
u = U, \quad v = 0 \quad \text{(if along x-axis)}
$$

Stream function:  
$$
\psi = Uy
$$

Velocity potential:  
$$
\phi = Ux
$$

If inclined at angle α:  
$$
u = U\cos\alpha, \quad v = U\sin\alpha
$$  
$$
\psi = U(y\cos\alpha - x\sin\alpha), \quad \phi = U(x\cos\alpha + y\sin\alpha)
$$

---

**3. Source / Sink**  
Located at origin, strength \( m \)  
Radial symmetry (polar coordinates \( r, \theta \))  

Velocity components:  
$$
v_r = \frac{m}{2\pi r}, \quad v_\theta = 0
$$

Stream function:  
$$
\psi = \frac{m}{2\pi} \theta
$$

Velocity potential:  
$$
\phi = \frac{m}{2\pi} \ln r
$$

---

**4. Free Vortex**  
Circulation strength \( \Gamma \)  

Velocity components:  
$$
v_r = 0, \quad v_\theta = \frac{\Gamma}{2\pi r}
$$

Stream function:  
$$
\psi = -\frac{\Gamma}{2\pi} \ln r
$$

Velocity potential:  
$$
\phi = \frac{\Gamma}{2\pi} \theta
$$

---

**5. Doublet (strength K)**  
Formed by a source–sink pair  

Velocity components:  
$$
v_r = -\frac{K \cos \theta}{r^2}, \quad v_\theta = -\frac{K \sin \theta}{r^2}
$$

Stream function:  
$$
\psi = -\frac{K \sin \theta}{r}
$$

Velocity potential:  
$$
\phi = \frac{K \cos \theta}{r}
$$

---

🔷 **SUPERPOSITION CASES**

**6. Uniform Flow + Source → Rankine Half Body**

Combine:  
Uniform flow:  
$$
\phi = Ux, \quad \psi = Uy
$$  
Source:  
$$
\phi = \frac{m}{2\pi} \ln r, \quad \psi = \frac{m}{2\pi} \theta
$$  
Resultant:  
$$
\phi = Ux + \frac{m}{2\pi} \ln r, \quad \psi = Uy + \frac{m}{2\pi} \theta
$$

---

**7. Uniform Flow + Doublet → Flow Around Cylinder**

Combine:  
Uniform:  
$$
\phi = Urcos\theta
$$  
Doublet:  
$$
\phi = \frac{K \cos \theta}{r}
$$  
Resultant:  
$$
\phi = Urcos\theta + \frac{K \cos \theta}{r}
$$  
$$
\psi = Ursin\theta - \frac{K \sin \theta}{r}
$$

---

**8. Uniform Flow + Doublet + Vortex → Cylinder with Circulation**

Add vortex:  
Vortex stream function:  
$$
\psi = -\frac{\Gamma}{2\pi} \ln r
$$  
Velocity potential:  
$$
\phi = \frac{\Gamma}{2\pi} \theta
$$  
Total:  
$$
\phi = Urcos\theta + \frac{K \cos \theta}{r} + \frac{\Gamma}{2\pi} \theta
$$  
$$
\psi = Ursin\theta - \frac{K \sin \theta}{r} - \frac{\Gamma}{2\pi} \ln r
$$

---

🔴 **BONUS: IMPORTANT REMARKS**  
- **Streamlines** (ψ = constant) indicate flow direction  
- **Equipotential lines** (ϕ = constant) are always orthogonal to streamlines  
- All equations assume **2D, steady, incompressible, irrotational flow**
""", unsafe_allow_html=True)

with st.expander("🧠 Example Practice Questions"):
    st.markdown("""
Test your understanding of potential flow theory using the following example scenarios:

1. **Stream Function of a Uniform Flow**  
   A uniform flow has a velocity of **U = 2 m/s**.  
   - Write down the expressions for the **velocity components (u, v)**, **stream function (ψ)**, and **potential function (ϕ)**.  
   - Sketch how the streamlines would appear.

2. **Effect of a Source**  
   A point source is located at the origin with a strength of **5 m²/s**.  
   - Determine the velocity field components **(u, v)** at a point (2, 2).  
   - Describe the pattern of streamlines near the origin.

3. **Superposition: Rankine Half Body**  
   Combine a uniform flow (**U = 2 m/s**) with a source (**m = 5 m²/s**) placed at the origin.  
   - What kind of body shape does this flow simulate?  
   - Identify the location of the stagnation point.

4. **Flow Over a Cylinder (Doublet + Uniform)**  
   A doublet with strength **K = 5 m²/s** is superimposed on a uniform flow of **U = 2 m/s**.  
   - Describe the streamline pattern around the cylinder.  
   - Is there a stagnation point? If yes, where is it located?

5. **Vortex with Uniform Flow (Circulating Cylinder)**  
   A uniform flow of **U = 2 m/s** is combined with a doublet (**K = 5 m²/s**) and a vortex of **Γ = 3 m²/s**.  
   - Explain how the vortex affects the symmetry of the flow.  
   - Does circulation cause a lift force on the simulated cylinder? Why or why not?
    """)

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
    st.session_state["entered_simulation"] = False
    st.session_state["show_point_output"] = False
    st.rerun()

# --- Inputs ---
st.markdown("### 🛠️ Flow Element Inputs")
st.number_input("Uniform Flow Speed (U) [m/s]", key="U")

st.markdown("#### 🔵 Source and 🔻 Sink")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Source Settings**")
    st.number_input("Source Strength [m²/s]", key="source_strength")
    st.number_input("Source X Location [m]", key="source_x", min_value=-4.0, max_value=4.0)
    st.number_input("Source Y Location [m]", key="source_y", min_value=-4.0, max_value=4.0)
with col2:
    st.markdown("**Sink Settings**")
    st.number_input("Sink Strength [m²/s]", key="sink_strength")
    st.number_input("Sink X Location [m]", key="sink_x", min_value=-4.0, max_value=4.0)
    st.number_input("Sink Y Location [m]", key="sink_y", min_value=-4.0, max_value=4.0)

st.markdown("#### 🔁 Vortex")
st.number_input("Vortex Strength (Γ) [m²/s]", key="vortex_strength")
st.number_input("Vortex X Location [m]", key="vortex_x", min_value=-4.0, max_value=4.0)
st.number_input("Vortex Y Location [m]", key="vortex_y", min_value=-4.0, max_value=4.0)

st.markdown("#### 💠 Doublet")
st.number_input("Doublet Strength (K) [m²/s]", key="doublet_strength")
st.number_input("Doublet X Location [m]", key="doublet_x", min_value=-4.0, max_value=4.0)
st.number_input("Doublet Y Location [m]", key="doublet_y", min_value=-4.0, max_value=4.0)

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
        st.session_state["entered_simulation"] = False
        st.session_state["show_point_output"] = False
        st.rerun()
# === Proceed to Simulation ===
if run:
    flow_values = [st.session_state[k] for k in flow_keys]
    if all(abs(v) < 1e-6 for v in flow_values):
        st.warning("⚠️ Please enter at least one non-zero flow element to simulate (e.g., Uniform flow, Source, etc.).")
        st.session_state["entered_simulation"] = False
        st.session_state["show_point_output"] = False
        st.stop()
    else:
        st.session_state["entered_simulation"] = True
        st.session_state["show_point_output"] = True

# === Run Simulation if Entered ===
if st.session_state["entered_simulation"]:

    # --- Grid Setup ---
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

    def safe_r_point(xc, yc):
        r2 = (px - xc)**2 + (py - yc)**2
        return max(r2, 1e-5), px - xc, py - yc

    # === Set Default Point (x, y) ===
    if "point_x" not in st.session_state:
        st.session_state["point_x"] = 1.0
    if "point_y" not in st.session_state:
        st.session_state["point_y"] = 1.0
    px = st.session_state["point_x"]
    py = st.session_state["point_y"]

    # --- Initial Values at Point
    u_p = st.session_state["U"]
    v_p = 0.0
    psi_p = st.session_state["U"] * py
    phi_p = st.session_state["U"] * px

    description_parts = [
        "This graph shows the streamlines of the fluid flow, indicating the path that fluid particles follow.",
        "The color represents flow speed—brighter colors mean higher speed."
    ]
    # --- Flow elements ---
    for element in ["source", "sink", "vortex", "doublet"]:
        strength = st.session_state[f"{element}_strength"]
        if strength != 0.0:
            x0 = st.session_state.get(f"{element}_x", 0.0)
            y0 = st.session_state.get(f"{element}_y", 0.0)
            r2 = safe_r(x0, y0)
            dx = X - x0
            dy = Y - y0

            if element == "source":
                u += (strength / (2 * np.pi)) * dx / r2
                v += (strength / (2 * np.pi)) * dy / r2
                psi += (strength / (2 * np.pi)) * np.arctan2(dy, dx)
                phi += (strength / (4 * np.pi)) * np.log(r2)
                description_parts.append("Blue dots represent sources where fluid emanates outward.")
            elif element == "sink":
                u -= (strength / (2 * np.pi)) * dx / r2
                v -= (strength / (2 * np.pi)) * dy / r2
                psi -= (strength / (2 * np.pi)) * np.arctan2(dy, dx)
                phi -= (strength / (4 * np.pi)) * np.log(r2)
                description_parts.append("Red dots represent sinks where fluid converges inward.")
            elif element == "vortex":
                u += -(strength / (2 * np.pi)) * dy / r2
                v +=  (strength / (2 * np.pi)) * dx / r2
                psi += (strength / (2 * np.pi)) * np.log(np.sqrt(r2))
                phi -= (strength / (2 * np.pi)) * np.arctan2(dy, dx)
                description_parts.append("Magenta dots represent vortices where the flow circulates.")
            elif element == "doublet":
                u -= (strength / (2 * np.pi)) * (dx**2 - dy**2) / (r2**2)
                v -= (strength / (2 * np.pi)) * (2 * dx * dy) / (r2**2)
                psi -= (strength / (2 * np.pi)) * dy / r2
                phi -= (strength / (2 * np.pi)) * dx / r2
                description_parts.append("Green dots represent doublets, modeling flow around bodies.")

            # Compute point-based values
            r2p, dxp, dyp = safe_r_point(x0, y0)
            if element == "source":
                u_p += (strength / (2 * np.pi)) * dxp / r2p
                v_p += (strength / (2 * np.pi)) * dyp / r2p
                psi_p += (strength / (2 * np.pi)) * np.arctan2(dyp, dxp)
                phi_p += (strength / (4 * np.pi)) * np.log(r2p)
            elif element == "sink":
                u_p -= (strength / (2 * np.pi)) * dxp / r2p
                v_p -= (strength / (2 * np.pi)) * dyp / r2p
                psi_p -= (strength / (2 * np.pi)) * np.arctan2(dyp, dxp)
                phi_p -= (strength / (4 * np.pi)) * np.log(r2p)
            elif element == "vortex":
                u_p += -(strength / (2 * np.pi)) * dyp / r2p
                v_p +=  (strength / (2 * np.pi)) * dxp / r2p
                psi_p += (strength / (2 * np.pi)) * np.log(np.sqrt(r2p))
                phi_p -= (strength / (2 * np.pi)) * np.arctan2(dyp, dxp)
            elif element == "doublet":
                u_p -= (strength / (2 * np.pi)) * (dxp**2 - dyp**2) / (r2p**2)
                v_p -= (strength / (2 * np.pi)) * (2 * dxp * dyp) / (r2p**2)
                psi_p -= (strength / (2 * np.pi)) * dyp / r2p
                phi_p -= (strength / (2 * np.pi)) * dxp / r2p

    # === Streamline Plot ===
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    speed = np.sqrt(u**2 + v**2)
    ax1.streamplot(X, Y, u, v, color=speed, linewidth=1, cmap='coolwarm')
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect("equal")
    ax1.set_title("Velocity Field Streamlines")
    st.pyplot(fig1)
    st.markdown("**🌀 Description**: This plot displays the velocity streamlines of the resulting potential flow field. Each line represents the path that a fluid particle would follow. The color gradient reflects flow speed — warmer colors indicate higher velocity regions. Streamlines visually demonstrate the interaction between superimposed flow elements.")


    # --- Stream Function Plot ---
    if show_psi:
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        cs = ax2.contour(X, Y, psi, levels=50, cmap="viridis")
        ax2.clabel(cs, inline=True, fontsize=8)
        ax2.set_title("Stream Function ψ")
        ax2.set_aspect("equal")
        st.pyplot(fig2)
        st.markdown("**🔷 Description**: The stream function (ψ) contours represent constant-flow paths. These lines are equivalent to streamlines in the flow field. This plot is especially useful for identifying symmetry, separation zones, and the qualitative structure of the flow.")

    # --- Potential Function Plot ---
    if show_phi:
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        cp = ax3.contour(X, Y, phi, levels=50, cmap="plasma")
        ax3.clabel(cp, inline=True, fontsize=8)
        ax3.set_title("Potential Function ϕ")
        ax3.set_aspect("equal")
        st.pyplot(fig3)
        st.markdown("**🟣 Description**: This plot shows contours of the velocity potential (ϕ), where each line represents a constant value of ϕ. These lines are orthogonal to streamlines in ideal flows and help illustrate changes in velocity magnitude across the domain.")

    # --- Overlay Plot ---
    if show_psi and show_phi:
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        cs1 = ax4.contour(X, Y, psi, levels=25, colors='blue', linewidths=1)
        cs2 = ax4.contour(X, Y, phi, levels=25, colors='green', linestyles='--', linewidths=1)
        ax4.clabel(cs1, inline=True, fontsize=8)
        ax4.clabel(cs2, inline=True, fontsize=8)
        ax4.set_title("Overlay of Stream Function (ψ) and Potential Function (ϕ)")
        ax4.set_aspect("equal")
        st.pyplot(fig4)
        st.markdown("**🔀 Description**: This overlay visualizes both stream function (ψ) and potential function (ϕ) simultaneously. The blue solid lines (ψ) represent streamlines, and the green dashed lines (ϕ) represent equipotential lines. Their orthogonal intersections are a key signature of irrotational flow, validating the assumptions of potential flow theory.")
    # === Point-Based Output Section ===
    if st.session_state["show_point_output"]:
        st.markdown("### 📍 Point-Based Output at (x, y)")
        with st.expander("🧮 Show Numerical Result at Selected Point", expanded=True):
            px = st.number_input("X-coordinate [m]", value=st.session_state["point_x"], min_value=-4.0, max_value=4.0, step=0.1, key="px_input")
            py = st.number_input("Y-coordinate [m]", value=st.session_state["point_y"], min_value=-4.0, max_value=4.0, step=0.1, key="py_input")

            if st.button("📍 Compute Result at This Point"):
                st.session_state["point_x"] = px
                st.session_state["point_y"] = py
                st.rerun()

            # === Show Result Values at Selected Point ===
            st.markdown("#### 📌 Computed Result at Selected Point:")
            st.write(f"**u (velocity-x):** {u_p:.4f} m/s")
            st.write(f"**v (velocity-y):** {v_p:.4f} m/s")
            st.write(f"**Stream Function ψ:** {psi_p:.4f} m²/s")
            st.write(f"**Potential Function ϕ:** {phi_p:.4f} m²/s")

# --- Footer ---
st.markdown("<hr><p style='text-align: center;'>© Developed by A. Abd Razak & S. Suhaime – 2025</p>", unsafe_allow_html=True)
