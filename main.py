import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define available weight plates
PLATES_LBS = [45, 35, 25, 10, 5, 2.5]
PLATES_KG = [20, 15, 10, 5, 2.5, 1.25]

# Define barbell weights
BARBELL_LBS = 45
BARBELL_KG = 20

# Define common lift types
LIFT_TYPES = ["Custom", "Squat", "Bench Press", "Deadlift", "Overhead Press", "Barbell Row"]

def calculate_plates(target_weight, unit_system):
    """Calculate the optimal combination of weight plates"""
    plates = PLATES_LBS if unit_system == "lbs" else PLATES_KG
    barbell_weight = BARBELL_LBS if unit_system == "lbs" else BARBELL_KG
    
    remaining_weight = target_weight - barbell_weight
    if remaining_weight < 0:
        return []
    
    combination = []
    for plate in plates:
        count = remaining_weight // (2 * plate)
        if count > 0:
            combination.extend([plate] * int(count))
            remaining_weight -= 2 * plate * count
    
    return combination

def create_barbell_visual(plates, unit_system):
    """Create a visual representation of the loaded barbell"""
    barbell_length = 2.2  # meters
    sleeve_length = 0.4  # meters
    
    fig = go.Figure()
    
    # Add barbell
    fig.add_shape(type="line", x0=-barbell_length/2, y0=0, x1=barbell_length/2, y1=0,
                  line=dict(color="gray", width=10))
    
    # Add sleeves
    fig.add_shape(type="line", x0=-barbell_length/2, y0=0, x1=-barbell_length/2+sleeve_length, y1=0,
                  line=dict(color="darkgray", width=20))
    fig.add_shape(type="line", x0=barbell_length/2-sleeve_length, y0=0, x1=barbell_length/2, y1=0,
                  line=dict(color="darkgray", width=20))
    
    # Add plates
    plate_positions = [-barbell_length/2+sleeve_length, barbell_length/2-sleeve_length]
    plate_colors = ['red', 'blue', 'yellow', 'green', 'white', 'black']
    
    for side in [0, 1]:
        position = plate_positions[side]
        direction = 1 if side == 1 else -1
        for i, plate in enumerate(plates):
            plate_width = 0.02 + (plate / max(PLATES_LBS if unit_system == "lbs" else PLATES_KG)) * 0.03
            fig.add_shape(type="line",
                          x0=position, y0=-0.2, x1=position, y1=0.2,
                          line=dict(color=plate_colors[i % len(plate_colors)], width=plate_width*100))
            # Add plate weight label
            fig.add_annotation(x=position, y=0.25, text=f"{plate} {unit_system}",
                               showarrow=False, font=dict(size=10))
            position += direction * plate_width
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[-barbell_length/2-0.1, barbell_length/2+0.1]),
        yaxis=dict(visible=False, range=[-0.3, 0.3]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=250
    )
    
    return fig

def main():
    st.title("Weightlifting Plate Calculator")
    st.write("Optimize your barbell setup for weightlifting and strength training exercises.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lift_type = st.selectbox("Select lift type:", LIFT_TYPES)
    
    with col2:
        target_weight = st.number_input("Enter target weight:", min_value=0.0, step=0.5, value=100.0)
    
    with col3:
        unit_system = st.selectbox("Select unit system:", ["lbs", "kg"])
    
    if st.button("Calculate"):
        plates = calculate_plates(target_weight, unit_system)
        
        if not plates:
            st.warning(f"The target weight is less than or equal to the barbell weight ({BARBELL_LBS if unit_system == 'lbs' else BARBELL_KG} {unit_system}).")
        else:
            st.subheader("Optimal plate combination:")
            plate_counts = pd.Series(plates).value_counts().sort_index()
            for plate, count in plate_counts.items():
                st.write(f"{count}x {plate} {unit_system}")
            
            total_weight = sum(plates) * 2 + (BARBELL_LBS if unit_system == "lbs" else BARBELL_KG)
            st.write(f"Total weight: {total_weight} {unit_system}")
            
            st.subheader("Visual representation:")
            fig = create_barbell_visual(plates, unit_system)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Tips")
    st.write("1. Warm-up sets: Start with 2-3 sets at 50-60% of your target weight.")
    st.write("2. Progressive loading: Increase weight gradually by 5-10% each week.")
    st.write("3. Rest between sets: Take 2-3 minutes for compound exercises like squats and deadlifts.")
    
    st.markdown("---")
    st.write("Note: This calculator assumes a standard Olympic barbell weight of 45 lbs (20 kg).")

if __name__ == "__main__":
    main()
