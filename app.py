import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Automatic Clutch Calculator", layout="centered")
st.title("⚙️ Automatic Clutch Plate Calculator")

# -----------------------------
# Display Image
# -----------------------------
try:
    image = Image.open("clutch.png")
    st.image(image, caption="Clutch Plate Assembly", use_container_width=True)
except:
    st.warning("Upload an image named 'clutch.png' in project folder.")

st.divider()

# -----------------------------
# Input Section
# -----------------------------
st.subheader("🔢 Enter Design Inputs")

col1, col2 = st.columns(2)

with col1:
    mu = st.slider("Friction Coefficient (μ)", 0.2, 0.6, 0.35, 0.01)
    n = st.number_input("Number of Friction Surfaces", 1, 6, 2)

with col2:
    Ro = st.number_input("Outer Radius Ro (m)", value=0.12, format="%.3f")
    Ri = st.number_input("Inner Radius Ri (m)", value=0.06, format="%.3f")
    p = st.number_input("Allowable Pressure p (Pa)", value=200000.0)

theory = st.selectbox("Clutch Theory", ["Uniform Wear", "Uniform Pressure"])

# -----------------------------
# Automatic Validation
# -----------------------------
if Ri >= Ro:
    st.error("Inner radius must be smaller than outer radius.")
    st.stop()

# -----------------------------
# Automatic Calculations
# -----------------------------
area = np.pi * (Ro**2 - Ri**2)
W = p * area

if theory == "Uniform Wear":
    T = mu * W * n * (Ro + Ri) / 2
else:
    T = (2/3) * mu * W * n * ((Ro**3 - Ri**3) / (Ro**2 - Ri**2))

# -----------------------------
# Display Results
# -----------------------------
st.subheader("📊 Live Results (Auto Calculated)")

c1, c2, c3 = st.columns(3)
c1.metric("Contact Area (m²)", f"{area:.4f}")
c2.metric("Axial Force (N)", f"{W:.0f}")
c3.metric("Torque Capacity (N·m)", f"{T:.1f}")

# -----------------------------
# Graph
# -----------------------------
st.subheader("📈 Torque vs Axial Force")

W_range = np.linspace(0.2 * W, 2 * W, 60)

if theory == "Uniform Wear":
    T_range = mu * W_range * n * (Ro + Ri) / 2
else:
    T_range = (2/3) * mu * W_range * n * ((Ro**3 - Ri**3) / (Ro**2 - Ri**2))

fig, ax = plt.subplots()
ax.plot(W_range, T_range)
ax.set_xlabel("Axial Force (N)")
ax.set_ylabel("Torque (N·m)")
ax.grid(True)

st.pyplot(fig)

# -----------------------------
# AI Recommendations
# -----------------------------
st.subheader("🤖 Smart Design Suggestions")

tips = []

if T < 300:
    tips.append("Torque capacity is low — increase friction surfaces or radius.")

if mu < 0.3:
    tips.append("Low friction coefficient — select better lining material.")

if p > 300000:
    tips.append("High pressure — verify wear and thermal safety.")

if (Ro - Ri) < 0.03:
    tips.append("Small friction width — consider increasing disc width.")

if not tips:
    tips.append("Design parameters are well optimized.")

for tip in tips:
    st.info("✔️ " + tip)
