import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define available weight plates
PLATES_LBS = [45, 35, 25, 10, 5, 2.5]
PLATES_KG = [20, 15, 10, 5, 2.5, 1.25]

def calculate_plates(target_weight, bar_weight):
    """Calculate the optimal combination of weight plates"""
    plates = PLATES_LBS  # We'll use lbs for simplicity in this version
    
    remaining_weight = (target_weight - bar_weight) / 2  # Divide by 2 to get weight per side
    if remaining_weight < 0:
        return []
    
    combination = []
    for plate in plates:
        count = int(remaining_weight // plate)
        if count > 0:
            combination.extend([plate] * count)
            remaining_weight -= plate * count
    
    return combination

def create_barbell_visual(final_plates, drop_plates):
    """Create a visual representation of the loaded barbell for final and drop sets"""
    barbell_length = 2.2  # meters
    sleeve_length = 0.4  # meters
    
    fig = go.Figure()
    
    # Add barbell for final set
    fig.add_shape(type="line", x0=-barbell_length/2, y0=0.2, x1=barbell_length/2, y1=0.2,
                  line=dict(color="gray", width=10))
    
    # Add barbell for drop set
    fig.add_shape(type="line", x0=-barbell_length/2, y0=-0.2, x1=barbell_length/2, y1=-0.2,
                  line=dict(color="gray", width=10))
    
    # Add sleeves
    for y in [0.2, -0.2]:
        fig.add_shape(type="line", x0=-barbell_length/2, y0=y, x1=-barbell_length/2+sleeve_length, y1=y,
                      line=dict(color="darkgray", width=20))
        fig.add_shape(type="line", x0=barbell_length/2-sleeve_length, y0=y, x1=barbell_length/2, y1=y,
                      line=dict(color="darkgray", width=20))
    
    # Add plates
    plate_positions = [-barbell_length/2+sleeve_length, barbell_length/2-sleeve_length]
    plate_colors = ['red', 'blue', 'yellow', 'green', 'white', 'black']
    
    for plates, y_offset in [(final_plates, 0.2), (drop_plates, -0.2)]:
        for side in [0, 1]:
            position = plate_positions[side]
            direction = 1 if side == 1 else -1
            for i, plate in enumerate(plates):
                plate_width = 0.02 + (plate / max(PLATES_LBS)) * 0.03
                fig.add_shape(type="line",
                              x0=position, y0=y_offset-0.15, x1=position, y1=y_offset+0.15,
                              line=dict(color=plate_colors[i % len(plate_colors)], width=plate_width*100))
                fig.add_annotation(x=position, y=y_offset+0.2, text=f"{plate}",
                                   showarrow=False, font=dict(size=10))
                position += direction * plate_width
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[-barbell_length/2-0.1, barbell_length/2+0.1]),
        yaxis=dict(visible=False, range=[-0.5, 0.5]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    
    return fig

def main():
    st.title("Advanced Weightlifting Plate Calculator")
    st.write("Optimize your barbell setup for weightlifting and strength training exercises, including drop sets.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        final_side_weight = st.number_input("Final Side Weight (lbs):", min_value=0.0, step=2.5, value=70.0)
    
    with col2:
        bar_weight = st.number_input("Bar Weight (lbs):", min_value=0.0, step=5.0, value=45.0)
    
    with col3:
        percent_drop = st.number_input("Percent Drop (%):", min_value=0.0, max_value=100.0, step=5.0, value=75.0) / 100

    if st.button("Calculate"):
        final_set_weight = (final_side_weight * 2) + bar_weight
        drop_side_weight = final_set_weight * (1 - percent_drop)
        remaining_weight = final_set_weight - drop_side_weight
        remaining_weight_per_side = (remaining_weight - bar_weight) / 2
        
        st.subheader("Calculated Weights:")
        st.write(f"Final Set Weight: {final_set_weight:.2f} lbs")
        st.write(f"Weight 2 Remove: {drop_side_weight:.2f} lbs")
        st.write(f"Drop Set Weight: {remaining_weight:.2f} lbs")
        st.write(f"Weight Per Side, Drop: {remaining_weight_per_side:.2f} lbs")
        
        st.subheader("Calculation Breakdown:")
        st.write("Here's how we calculate the weights for your workout:")
        
        st.latex(r"FinalSetWeight = (FinalSideWeight \times 2) + BarWeight")
        st.latex(f"FinalSetWeight = ({final_side_weight:.2f} \times 2) + {bar_weight:.2f} = {final_set_weight:.2f}")
        st.write("This is the total weight for your heaviest set, including the bar and all plates.")
        
        st.latex(r"DropSideWeight = FinalSetWeight \times (1 - PercentDrop)")
        st.latex(f"DropSideWeight = {final_set_weight:.2f} \times (1 - {percent_drop:.2f}) = {drop_side_weight:.2f}")
        st.write("This is the total weight to remove from the bar for your drop set.")
        
        st.latex(r"RemainingWeight = FinalSetWeight - DropSideWeight")
        st.latex(f"RemainingWeight = {final_set_weight:.2f} - {drop_side_weight:.2f} = {remaining_weight:.2f}")
        st.write("This is the weight that remains on the bar after removing the drop weight.")
        
        st.latex(r"RemainingWeightPerSide = (RemainingWeight - BarWeight) \div 2")
        st.latex(f"RemainingWeightPerSide = ({remaining_weight:.2f} - {bar_weight:.2f}) \div 2 = {remaining_weight_per_side:.2f}")
        st.write("This is the weight that remains on each side of the bar after removing the drop weight.")
        
        final_plates = calculate_plates(final_set_weight, bar_weight)
        drop_plates = calculate_plates(remaining_weight_per_side * 2 + bar_weight, bar_weight)
        
        st.subheader("Plate Combinations:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Final Set (per side):")
            plate_counts = pd.Series(final_plates).value_counts().sort_index()
            for plate, count in plate_counts.items():
                st.write(f"{count}x {plate} lbs")
        
        with col2:
            st.write("Drop Set (per side):")
            plate_counts = pd.Series(drop_plates).value_counts().sort_index()
            for plate, count in plate_counts.items():
                st.write(f"{count}x {plate} lbs")
        
        st.subheader("Visual Representation:")
        fig = create_barbell_visual(final_plates, drop_plates)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Top: Final Set, Bottom: Drop Set")
    
    st.markdown("---")
    st.subheader("How to use this calculator:")
    st.write("1. Enter the weight you want on each side of the bar for your final (heaviest) set.")
    st.write("2. Specify the weight of the barbell you're using.")
    st.write("3. Set the percentage you want to drop for your drop set.")
    st.write("4. Click 'Calculate' to see the optimal plate combinations and weights for both sets.")
    
    st.markdown("---")
    st.write("Note: This calculator uses pounds (lbs) and assumes standard weight plate increments.")

if __name__ == "__main__":
    main()
