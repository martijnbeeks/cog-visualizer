import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

# st.set_page_config(page_title="Enhanced Calculation App", layout="wide")
# st.title('📐 Center of Gravity distribution app')
# Add company logo and banner
col1, col2 = st.columns([1, 5])
with col1:
    st.image("app/high_eye.jpeg", width=100)
with col2:
    st.markdown("<h1 style='text-align: center; color: grey;'>Payload distributor</h1>", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    
    component = st.write("Payload details")
    weight = st.number_input('Weight (kg)', min_value=0.0, format="%.2f")
    arm = st.number_input('Arm (m)', format="%.2f")

    if st.button('Update'):
        st.session_state.weight = weight
        st.session_state.arm = arm
    
    st.header('Input Table')
    st.write('Add rows with **Weight** and **Arm** values:')
    # Initialize the DataFrame in session state if not already

    st.session_state.df = pd.DataFrame({
        'Component': ['Tail Gearbox', 'Engine', 'Exhaust', 'Heli', 'Payload'],
        'Weight (kg)': [0.32, 4.7, 0.78, 26, weight],
        'Arm (m)': [1.12, -0.05, 0.43, 0.09, arm]
    })
    
    st.dataframe(st.session_state.df, use_container_width=True)
    
    

# Main content
# st.header('Results')
df = st.session_state.df.copy()
# if not df.empty and df['Weight'].notnull().all() and df['Arm'].notnull().all():
# Perform calculations
df['Moment'] = df['Weight (kg)'] * df['Arm (m)']
total_weight = df['Weight (kg)'].sum()
total_moment = df['Moment'].sum()
center_of_gravity = total_moment / total_weight * 1000 if total_weight != 0 else 0


# Display calculation results in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Weight (kg)", value=f"{total_weight:.2f}")
col2.metric(label="Total Moment (m*Kg)", value=f"{total_moment:.2f}")
col3.metric(label="Center of Gravity [mm]", value=f"{center_of_gravity:.2f}", help="Recommended position")
# col4.metric(label="Distance of camera", value=f"{distance:.2f}", delta="4%", help="Recommended distance")

# Visual representation using Plotly
# add some space
st.write("")
st.write("")
st.subheader('Visualization')

if center_of_gravity > 0:
    st.metric(label="Move camera left (mm)", value=f"{center_of_gravity:.2f}", help="Recommended distance")
    move_distance = -1 * center_of_gravity
    move_text = "Move camera to the left"
else:
    st.metric(label="Move camera right (mm)", value=f"{center_of_gravity:.2f}", help="Recommended distance")
    move_distance = center_of_gravity
    move_text = "Move camera to the left"



image1_path = "app/drone.png"
image2_path = "app/camera.png"
image1 = Image.open(image1_path)
image2 = Image.open(image2_path)

# Convert images to numpy arrays
image1_array = np.asarray(image1)
image2_array = np.asarray(image2)

# Create the Plotly figure
fig = go.Figure()

# Add the first image
fig.add_trace(
    go.Image(
        z=image1_array,
        opacity=1.0  # Full opacity
    )
)

# Add the second image with slight transparency and a slight offset for the overlay
fig.add_trace(
    go.Image(
        z=image2_array,
        opacity=0.6,  # Slight transparency
        dx=0.4,  # Adjust x position
        dy=0.4,   # Adjust y position
        x0=650+move_distance,  # Adjust x position
        y0=217   # Adjust y position
    ),
)

# Add small leged with moved distance

fig.add_annotation(
    x=0.5,
    y=0.9,
    xref="paper",
    yref="paper",
    text=move_text,
    showarrow=False,
    font=dict(
        size=16,
        color="black"
    )
)

# Customize the layout
fig.update_layout(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig)