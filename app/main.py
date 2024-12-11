import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import base64

# Function to read and encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        data = img_file.read()
    encoded = base64.b64encode(data).decode()
    return encoded

image_path = 'app/higheye_logo.png'  # Replace 'logo.png' with your image file path

# Encode the image
image_base64 = get_base64_image(image_path)

banner_html = f"""
<style>
.banner {{
    background-color: rgb(38, 89, 128);
    padding: 10px;
    display: flex;
    align-items: center;
}}
.banner img {{
    max-height: 50px;
    margin-right: 20px;
}}
.banner-text {{
    color: white;
    font-size: 24px;
    text-align: center;
    flex-grow: 1;
}}
</style>
<div class="banner">
    <img src="data:image/png;base64,{image_base64}" alt="Logo">
    <div class="banner-text">Payload distributor</div>
</div>
"""

st.markdown(banner_html, unsafe_allow_html=True)
with st.sidebar:
    banner_html = f"""
    <style>
    .banner {{
        background-color: rgb(38, 89, 128);
        padding: 10px;
        display: flex;
        align-items: center;
    }}
    .banner img {{
        max-height: 50px;
        margin-right: 20px;
    }}
    </style>
    <div class="banner">
        <img src="data:image/png;base64,{image_base64}" alt="Logo">
        <div class="banner-text"> </div>
    </div>
    """
    st.write("")
    st.markdown(banner_html, unsafe_allow_html=True)
    st.header("Payload details")
    weight = st.number_input('Weight (kg)', min_value=0.0, format="%.2f")
    arm = st.number_input('Arm (m)', format="%.2f")

    if st.button('Update'):
        st.session_state.weight = weight
        st.session_state.arm = arm
    
    st.write(f"**Input Table**")
    st.write('Add rows with **Weight** and **Arm** values:')

    st.session_state.df = pd.DataFrame({
        'Component': ['Tail Gearbox', 'Engine', 'Exhaust', 'Heli', "Payload"],
        'Weight (kg)': [0.32, 4.7, 0.78, 26, weight],
        'Arm (m)': [1.12, -0.05, 0.43, 0.09, arm]
    })
    
    st.dataframe(st.session_state.df, use_container_width=True)
    
    

# Main content
df = st.session_state.df.copy()
# Perform calculations
df['Moment'] = df['Weight (kg)'] * df['Arm (m)']
total_weight = df['Weight (kg)'].sum()
total_moment = df['Moment'].sum()
center_of_gravity = total_moment / total_weight * 1000 if total_weight != 0 else 0


# Display calculation results in columns
st.write("")
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Weight (kg)", value=f"{total_weight:.2f}")
col2.metric(label="Total Moment (m*Kg)", value=f"{total_moment:.2f}")
col3.metric(label="Center of Gravity [mm]", value=f"{center_of_gravity:.2f}", help="Recommended position")

# Visual representation using Plotly
st.write("")
st.write("")
st.subheader('Visualization')

if center_of_gravity > 0:
    st.metric(label="Move camera right (mm)", value=f"{center_of_gravity:.2f}", help="Recommended distance")
    move_distance = center_of_gravity
    move_text = f"Move camera to the right: {move_distance:.2f}"
else:
    st.metric(label="Move camera left (mm)", value=f"{center_of_gravity:.2f}", help="Recommended distance")
    move_distance = -1 * center_of_gravity
    move_text = f"Move camera to the left: {move_distance:.2f}"



image1_path = "app/drone.png"
image2_path = "app/camera.png"
image3_path = "app/cog.png"
image1 = Image.open(image1_path)
image2 = Image.open(image2_path)
image3 = Image.open(image3_path)

# Convert images to numpy arrays
image1_array = np.asarray(image1)
image2_array = np.asarray(image2)
image3_array = np.asarray(image3)

# Create the Plotly figure
fig = go.Figure()

# Add the first image
fig.add_trace(
    go.Image(
        z=image1_array,
        opacity=1.0 
    )
)

fig.add_trace(
    go.Image(
        z=image2_array,
        opacity=0.6,
        dx=0.4,
        dy=0.4,
        x0=650+move_distance,
        y0=217
    ),
)

fig.add_trace(
    go.Image(
        z=image3_array,
        dx=.04,
        dy=.04,
        x0=300,
        y0=217
    ),
)

fig.add_trace(
    go.Image(
        z=image3_array,
        dx=.04,
        dy=.04,
        x0=692+move_distance,
        y0=220
    ),
)

# Add a line between the two images
fig.add_shape(
    type="line",
    x0=330,
    y0=233,
    x1=692+move_distance,
    y1=233,
    line=dict(
        color="red",
        width=2,
    ))

# Add annotation
fig.add_annotation(
    x=500, y=290,
    text=move_text,
    showarrow=False,
    arrowhead=0
)


# Customize the layout
fig.update_layout(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig)