import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="KEC Competitor Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS to match the desired design
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --color-blue-50: #e3f2fd;
        --color-blue-100: #bbdefb;
        --color-blue-200: #90caf9;
        --color-blue-300: #64b5f6;
        --color-blue-400: #42a5f5;
        --color-blue-500: #2196f3;
        --color-blue-600: #1e88e5;
        --color-blue-700: #1976d2;
        --color-blue-800: #1565c0;
        --color-blue-900: #0d47a1;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background */
    .stApp {
        background: linear-gradient(to bottom, #e3f2fd 0%, #ffffff 100%);
    }
    
    /* Blue header band */
    .blue-header-band {
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 50%, #2196f3 100%);
        padding: 20px 40px;
        margin: -80px -80px 30px -80px;
        border-radius: 0;
        box-shadow: 0 4px 12px rgba(21, 101, 192, 0.3);
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .header-text {
        color: white;
    }
    
    .header-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-caption {
        font-size: 14px;
        margin: 4px 0 0 0;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #90caf9;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: #2196f3;
        box-shadow: 0 8px 20px rgba(33, 150, 243, 0.25);
        transform: translateY(-4px);
    }
    
    .kpi-label {
        font-size: 12px;
        color: #1565c0;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #1565c0, #2196f3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .kpi-subtext {
        font-size: 12px;
        color: #1976d2;
        font-weight: 500;
    }
    
    /* Filter section */
    .stSelectbox, .stTextInput {
        background-color: white;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 13px;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        background: linear-gradient(135deg, #bbdefb, #90caf9);
        color: #1565c0;
        border: 1px solid #64b5f6;
    }
    
    .badge-competitor {
        background: linear-gradient(135deg, #1e88e5, #2196f3);
        color: white;
        border: 1px solid #1976d2;
    }
    
    /* Status indicator */
    .sync-status {
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.2), rgba(100, 181, 246, 0.1));
        color: #1976d2;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        border: 2px solid #90caf9;
    }
    
    .sync-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1976d2, #2196f3);
        animation: pulse 2s infinite;
        margin-right: 8px;
        box-shadow: 0 0 8px rgba(33, 150, 243, 0.6);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1976d2, #2196f3);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
    }
    
    /* Section headers */
    h3 {
        color: #1565c0 !important;
        font-weight: 700 !important;
        margin-top: 24px !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #1976d2, #2196f3);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(135deg, #1565c0, #1976d2);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(25, 118, 210, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None

# Header WITHOUT logo
st.markdown("""
<div class="blue-header-band">
    <div class="header-content">
        <div class="header-left">
            <div class="header-text">
                <h1 class="header-title">KEC Competitor Intelligence Dashboard</h1>
                <p class="header-caption">Competition & industry updates</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# FILE UPLOADER AT TOP (ALWAYS VISIBLE)
# ═════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Excel file with competitor data", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Process data
        processed_data = []
        for _, row in df.iterrows():
            sbu_list = str(row.get('SBU', '')).split(',') if pd.notna(row.get('SBU')) else []
            sbu_list = [s.strip() for s in sbu_list if s.strip()]
            
            comp_list = str(row.get('Competitor', '')).split(',') if pd.notna(row.get('Competitor')) else []
            comp_list = [c.strip() for c in comp_list if c.strip()]
            
            processed_data.append({
                'keyword': str(row.get('keyword', '')).strip(),
                'newstitle': str(row.get('newstitle', 'No title'))[:200],
                'sbu_list': sbu_list,
                'competitor_list': comp_list,
                'publishedate': pd.to_datetime(row.get('publishedate', datetime.now())),
                'source': str(row.get('source', 'Unknown')).strip()
            })
        
        st.session_state.raw_data = pd.DataFrame(processed_data)
        st.session_state.filtered_data = st.session_state.raw_data.copy()
        
        st.success(f"✅ File uploaded successfully! {len(processed_data)} articles loaded.")
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

# Function to apply powder blue alternating row colors (including index)
def style_alternating_rows(row):
    """Apply alternating powder blue colors to rows including index"""
    if row.name % 2 == 0:
        return ['background-color: #e3f2fd'] * len(row)  # Powder Blue
    else:
        return ['background-color: #f5f9ff'] * len(row)  # Very Light Powder Blue

# Main dashboard - ONLY SHOWS IF DATA IS LOADED
if st.session_state.raw_data is not None:
    df = st.session_state.raw_data
    
    # Filters section
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    filter_cols = st.columns(5)
    
    with filter_cols[0]:
        # Get unique SBUs
        all_sbus = set()
        for sbu_list in df['sbu_list']:
            all_sbus.update(sbu_list)
        sbu_filter = st.selectbox("SBU", ["All SBUs"] + sorted(list(all_sbus)))
    
    with filter_cols[1]:
        # Get unique competitors
        all_competitors = set()
        for comp_list in df['competitor_list']:
            all_competitors.update(comp_list)
        competitor_filter = st.selectbox("Competitor", ["All Competitors"] + sorted(list(all_competitors)))
    
    with filter_cols[2]:
        keyword_filter = st.text_input("Keyword", placeholder="Search keywords...")
    
    with filter_cols[3]:
        all_sources = df['source'].unique().tolist()
        source_filter = st.selectbox("Source", ["All Sources"] + sorted(all_sources))
    
    with filter_cols[4]:
        st.write("")
        st.write("")
        if st.button("Reset Filters", use_container_width=True):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if sbu_filter != "All SBUs":
        filtered_df = filtered_df[filtered_df['sbu_list'].apply(lambda x: sbu_filter in x)]
    
    if competitor_filter != "All Competitors":
        filtered_df = filtered_df[filtered_df['competitor_list'].apply(lambda x: competitor_filter in x)]
    
    if keyword_filter:
        filtered_df = filtered_df[filtered_df['keyword'].str.contains(keyword_filter, case=False, na=False)]
    
    if source_filter != "All Sources":
        filtered_df = filtered_df[filtered_df['source'] == source_filter]
    
    st.session_state.filtered_data = filtered_df
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Cards
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        total_articles = len(filtered_df)
        if len(filtered_df) > 0:
            min_date = filtered_df['publishedate'].min().strftime('%m/%d/%Y')
            max_date = filtered_df['publishedate'].max().strftime('%m/%d/%Y')
            date_range = f"{min_date} to {max_date}"
        else:
            date_range = "No data"
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Articles</div>
            <div class="kpi-value">{total_articles:,}</div>
            <div class="kpi-subtext">{date_range}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        unique_keywords = filtered_df['keyword'].nunique()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Unique Keywords</div>
            <div class="kpi-value">{unique_keywords}</div>
            <div class="kpi-subtext">Keywords tracked</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        all_comps = set()
        for comp_list in filtered_df['competitor_list']:
            all_comps.update(comp_list)
        competitors_mentioned = len(all_comps)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Competitors Mentioned</div>
            <div class="kpi-value">{competitors_mentioned}</div>
            <div class="kpi-subtext">Active in period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        news_sources = filtered_df['source'].nunique()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">News Sources</div>
            <div class="kpi-value">{news_sources}</div>
            <div class="kpi-subtext">Media channels</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Articles Table
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📰 Recent Articles")
    
    if len(filtered_df) > 0:
        display_df = filtered_df.head(50).copy()
        display_df['SBU'] = display_df['sbu_list'].apply(lambda x: x[0] if len(x) > 0 else 'N/A')
        display_df['Competitor'] = display_df['competitor_list'].apply(lambda x: x[0] if len(x) > 0 else 'N/A')
        display_df['Date'] = display_df['publishedate'].dt.strftime('%m/%d/%Y')
        
        # Remove Keyword column
        table_df = display_df[['newstitle', 'SBU', 'Competitor', 'source', 'Date']]
        table_df.columns = ['Title', 'SBU', 'Competitor', 'Source', 'Date']
        
        # Apply powder blue alternating row styling using Pandas Styler (includes index)
        def style_all_including_index(row):
            """Style all columns including the index"""
            if row.name % 2 == 0:
                return ['background-color: #e3f2fd'] * len(row)
            else:
                return ['background-color: #f5f9ff'] * len(row)
        
        styled_df = table_df.style.apply(style_all_including_index, axis=1)
        styled_df.index.name = None  # Remove index name if present
        
        st.dataframe(styled_df, use_container_width=True, height=400)
    else:
        st.info("No articles match your filters")
    
    # Charts
    st.markdown("<br><br>", unsafe_allow_html=True)
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        if len(filtered_df) > 0:
            date_counts = filtered_df.groupby(filtered_df['publishedate'].dt.date).size().reset_index()
            date_counts.columns = ['Date', 'Count']
            date_counts = date_counts.sort_values('Date')
            
            fig_date = px.line(date_counts, x='Date', y='Count', 
                              markers=True,
                              color_discrete_sequence=['#1976d2'])
            fig_date.update_traces(fill='tozeroy', fillcolor='rgba(25, 118, 210, 0.2)')
            fig_date.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_date, use_container_width=True)
    
    with chart_cols[1]:
        if len(filtered_df) > 0:
            keyword_counts = filtered_df['keyword'].value_counts().head(10).reset_index()
            keyword_counts.columns = ['Keyword', 'Count']
            
            fig_keywords = px.bar(keyword_counts, y='Keyword', x='Count',
                                 orientation='h',
                                 color_discrete_sequence=['#2196f3'])
            fig_keywords.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_keywords, use_container_width=True)
    
    chart_cols2 = st.columns(2)
    
    with chart_cols2[0]:
        if len(filtered_df) > 0:
            sbu_counts = {}
            for sbu_list in filtered_df['sbu_list']:
                for sbu in sbu_list:
                    sbu_counts[sbu] = sbu_counts.get(sbu, 0) + 1
            
            if sbu_counts:
                sbu_df = pd.DataFrame(list(sbu_counts.items()), columns=['SBU', 'Count'])
                
                fig_sbu = px.pie(sbu_df, values='Count', names='SBU',
                                color_discrete_sequence=['#1976d2', '#2196f3', '#42a5f5', '#64b5f6', '#90caf9', '#bbdefb', '#1565c0'])
                fig_sbu.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_sbu, use_container_width=True)
    
    with chart_cols2[1]:
        if len(filtered_df) > 0:
            comp_counts = {}
            for comp_list in filtered_df['competitor_list']:
                for comp in comp_list:
                    comp_counts[comp] = comp_counts.get(comp, 0) + 1
            
            if comp_counts:
                comp_df = pd.DataFrame(list(comp_counts.items()), columns=['Competitor', 'Count'])
                comp_df = comp_df.sort_values('Count', ascending=False).head(10)
                
                fig_comp = px.bar(comp_df, y='Competitor', x='Count',
                                 orientation='h',
                                 color_discrete_sequence=['#1e88e5'])
                fig_comp.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_comp, use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.raw_data is not None:
        st.markdown('<div class="sync-status"><span class="sync-indicator"></span>Data Synced</div>', unsafe_allow_html=True)
