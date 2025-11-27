# Competitor-Dashboard_Streamlit
Python code for competitor dashboard hosted on streamlit
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Page configuration
st.set_page_config(
    page_title="Interactive Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Interactive Data Dashboard")
st.markdown("Upload an Excel file to explore your data with dynamic filters and visualizations")

# File uploader widget
uploaded_file = st.file_uploader("Choose an Excel file (.xlsx)", type=['xlsx'])

if uploaded_file is not None:
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Store original dataframe for reference
        if 'original_df' not in st.session_state:
            st.session_state.original_df = df.copy()
        
        st.success(f"✅ File uploaded successfully! Loaded {len(df)} rows and {len(df.columns)} columns.")
        
        # Sidebar for filters
        st.sidebar.header("🔍 Filters")
        
        # Initialize filtered dataframe
        filtered_df = df.copy()
        
        # Create filters for each column based on data type
        for column in df.columns:
            st.sidebar.markdown(f"**{column}**")
            
            # Determine column data type and create appropriate filter
            
            # Check if column is numeric (int or float)
            if pd.api.types.is_numeric_dtype(df[column]):
                # Get min and max values
                min_val = float(df[column].min())
                max_val = float(df[column].max())
                
                # Only create slider if min != max
                if min_val != max_val:
                    # Create slider for numeric columns
                    selected_range = st.sidebar.slider(
                        f"Range",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        key=f"slider_{column}"
                    )
                    # Filter data based on slider selection
                    filtered_df = filtered_df[
                        (filtered_df[column] >= selected_range[0]) & 
                        (filtered_df[column] <= selected_range[1])
                    ]
                else:
                    st.sidebar.info(f"Single value: {min_val}")
            
            # Check if column is datetime
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                # Get min and max dates
                min_date = df[column].min()
                max_date = df[column].max()
                
                if pd.notna(min_date) and pd.notna(max_date) and min_date != max_date:
                    # Create date range selector
                    selected_date_range = st.sidebar.date_input(
                        f"Date Range",
                        value=(min_date.date(), max_date.date()),
                        min_value=min_date.date(),
                        max_value=max_date.date(),
                        key=f"date_{column}"
                    )
                    # Filter data based on date selection
                    if len(selected_date_range) == 2:
                        start_date, end_date = selected_date_range
                        filtered_df = filtered_df[
                            (filtered_df[column].dt.date >= start_date) & 
                            (filtered_df[column].dt.date <= end_date)
                        ]
            
            # Categorical columns (string or object type with limited unique values)
            else:
                unique_values = df[column].dropna().unique()
                
                # Use multiselect if reasonable number of unique values (< 50)
                if len(unique_values) <= 50:
                    selected_values = st.sidebar.multiselect(
                        f"Select values",
                        options=sorted(unique_values.astype(str)),
                        default=sorted(unique_values.astype(str)),
                        key=f"multiselect_{column}"
                    )
                    # Filter data based on multiselect selection
                    if selected_values:
                        filtered_df = filtered_df[filtered_df[column].astype(str).isin(selected_values)]
                else:
                    st.sidebar.info(f"Too many unique values ({len(unique_values)})")
            
            st.sidebar.markdown("---")
        
        # Display filtered data count
        st.subheader(f"📋 Filtered Data ({len(filtered_df)} rows)")
        
        # Display filtered dataframe
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button for filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Filtered Data (CSV)",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
        
        # Visualizations section
        st.subheader("📈 Visualizations")
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        # Find numeric and categorical columns for visualization
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = filtered_df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Chart 1: Bar chart for categorical data
        if categorical_cols and len(filtered_df) > 0:
            with col1:
                st.markdown("#### Distribution by Category")
                # Select first categorical column
                cat_col = categorical_cols[0]
                
                # Count occurrences of each category
                category_counts = filtered_df[cat_col].value_counts().reset_index()
                category_counts.columns = [cat_col, 'Count']
                
                # Create bar chart
                fig_bar = px.bar(
                    category_counts.head(10),  # Show top 10 categories
                    x=cat_col,
                    y='Count',
                    title=f"Top 10 {cat_col} Distribution",
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Chart 2: Line or scatter chart for numeric data
        if len(numeric_cols) >= 2 and len(filtered_df) > 0:
            with col2:
                st.markdown("#### Numeric Relationship")
                # Select first two numeric columns
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                
                # Create scatter plot
                fig_scatter = px.scatter(
                    filtered_df,
                    x=x_col,
                    y=y_col,
                    title=f"{y_col} vs {x_col}",
                    color=categorical_cols[0] if categorical_cols else None,
                    trendline="ols" if len(filtered_df) > 2 else None
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        elif len(numeric_cols) >= 1 and len(filtered_df) > 0:
            with col2:
                st.markdown("#### Numeric Distribution")
                # Create histogram for single numeric column
                num_col = numeric_cols[0]
                
                fig_hist = px.histogram(
                    filtered_df,
                    x=num_col,
                    title=f"Distribution of {num_col}",
                    nbins=30,
                    color_discrete_sequence=['#1f77b4']
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        # Additional chart: Time series if datetime column exists
        datetime_cols = filtered_df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if datetime_cols and numeric_cols and len(filtered_df) > 0:
            st.markdown("#### Time Series Analysis")
            date_col = datetime_cols[0]
            value_col = numeric_cols[0]
            
            # Sort by date
            time_series_df = filtered_df.sort_values(by=date_col)
            
            # Create line chart
            fig_line = px.line(
                time_series_df,
                x=date_col,
                y=value_col,
                title=f"{value_col} Over Time",
                markers=True
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Summary statistics
        if numeric_cols:
            st.subheader("📊 Summary Statistics")
            st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.info("Please ensure the file is a valid Excel (.xlsx) file.")

else:
    # Display instructions when no file is uploaded
    st.info("👆 Upload an Excel file to get started")
    st.markdown("""
    ### How to use this dashboard:
    1. **Upload** your Excel file using the file uploader above
    2. **Filter** your data using the controls in the left sidebar
    3. **Explore** the filtered data and visualizations that update automatically
    4. **Download** the filtered data as a CSV file
    
    ### Supported features:
    - 🔢 Numeric columns: Range sliders
    - 📅 Date columns: Date range selectors
    - 📝 Categorical columns: Multi-select dropdowns
    - 📊 Dynamic charts that update with filters
    - ⬇️ Export filtered data
    """)
```
```
# requirements.txt
streamlit==1.31.0
pandas==2.2.0
openpyxl==3.1.2
plotly==5.18.0
