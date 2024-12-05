import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Enhanced Calculation App", layout="wide")
st.title('📐 Center of Gravity distribution app')

# Sidebar for inputs
with st.sidebar:
    st.header('Input Table')
    st.write('Add rows with **Weight** and **Arm** values:')
    # Initialize the DataFrame in session state if not already
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=['Component','Weight', 'Arm'])
    # Display the editable data table
    st.session_state.df = st.data_editor(
        st.session_state.df,
        num_rows='dynamic',
        use_container_width=True,
        hide_index=True,
        column_config={
            "Component": st.column_config.TextColumn(
                label="Component",
            ),
            "Weight": st.column_config.NumberColumn(
                "Weight",
                help="Enter the weight value",
                min_value=0.0,
                step=0.1,
                format="%.2f",
            ),
            "Arm": st.column_config.NumberColumn(
                "Arm",
                help="Enter the arm value",
                min_value=0.0,
                step=0.1,
                format="%.2f",
            ),
        },
    )

# Main content
st.header('Results')
df = st.session_state.df.copy()
if not df.empty and df['Weight'].notnull().all() and df['Arm'].notnull().all():
    # Perform calculations
    df['Moment'] = df['Weight'] * df['Arm']
    total_weight = df['Weight'].sum()
    total_moment = df['Moment'].sum()
    center_of_gravity = total_moment / total_weight if total_weight != 0 else 0
    distance = center_of_gravity*1.1  # Fixed distance for camera

    # Display calculation results in columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Total Weight", value=f"{total_weight:.2f}")
    col2.metric(label="Total Moment", value=f"{total_moment:.2f}")
    col3.metric(label="Center of Gravity", value=f"{center_of_gravity:.2f}")
    col4.metric(label="Distance of camera", value=f"{distance:.2f}", delta="4%", help="Recommended distance")

    # Visual representation using Plotly
    # add some space
    st.write("")
    st.write("")
    st.subheader('Visualization')
    main_block_width = 2
    main_block_height = 1
    main_block_x0 = 1  # Fixed position for main block
    main_block_x1 = main_block_x0 + main_block_width

    small_block_width = 0.5
    small_block_height = 0.5
    distance = center_of_gravity  # Distance based on calculation
    x0_small = main_block_x1 + distance  # Position of small block depends on distance

    # Create figure
    fig = go.Figure()

    # Add main block at fixed position
    fig.add_shape(
        type="rect",
        x0=main_block_x0,
        y0=0,
        x1=main_block_x1,
        y1=main_block_height,
        line=dict(color='RoyalBlue'),
        fillcolor='LightSkyBlue',
    )
    # Add small block at variable distance
    fig.add_shape(
        type="rect",
        x0=x0_small,
        y0=0,
        x1=x0_small + small_block_width,
        y1=small_block_height,
        line=dict(color='Crimson'),
        fillcolor='LightCoral',
    )

    # Add annotations
    fig.add_annotation(
        x=(main_block_x0 + main_block_x1) / 2,
        y=main_block_height + 0.1,
        text="Drone",
        showarrow=False,
        font=dict(size=14),
    )
    fig.add_annotation(
        x=x0_small + small_block_width / 2,
        y=small_block_height + 0.1,
        text="Camera",
        showarrow=False,
        font=dict(size=14),
    )

    # Update layout with fixed x-axis range
    fig.update_layout(
        width=800,
        height=400,
        xaxis=dict(
            range=[0, 20],  # Fixed x-axis range
            showgrid=False,
            zeroline=False,
            visible=False,
        ),
        yaxis=dict(
            range=[-1, main_block_height + 1],
            showgrid=False,
            zeroline=False,
            visible=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    # Display figure
    st.plotly_chart(fig, use_container_width=True)

    # Optionally, display the data table
    with st.expander("See Data Table and calculations"):
        st.dataframe(df[['Component', 'Weight', 'Arm', 'Moment']], use_container_width=True)
else:
    st.info('Please add data to the table with valid "Weight" and "Arm" values.')
