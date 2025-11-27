# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Competitor Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS to match the desired design
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --color-cream-50: #fcfcf9;
        --color-teal-500: #21808d;
        --color-teal-400: #2da6b2;
        --color-red-400: #ff5459;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Background */
    .stApp {
        background-color: #fcfcf9;
    }
    
    /* Header styling */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        border-bottom: 1px solid rgba(94, 82, 64, 0.2);
        margin-bottom: 32px;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #fffffe 0%, rgba(33, 128, 141, 0.08) 100%);
        border: 1px solid rgba(94, 82, 64, 0.12);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: #21808d;
        box-shadow: 0 4px 12px rgba(33, 128, 141, 0.15);
        transform: translateY(-2px);
    }
    
    .kpi-label {
        font-size: 12px;
        color: #626c71;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #21808d, #2da6b2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .kpi-subtext {
        font-size: 12px;
        color: #626c71;
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
        background: linear-gradient(135deg, rgba(33, 128, 141, 0.2), rgba(50, 184, 198, 0.1));
        color: #21808d;
        border: 1px solid rgba(33, 128, 141, 0.3);
    }
    
    .badge-competitor {
        background: linear-gradient(135deg, rgba(255, 84, 89, 0.2), rgba(168, 75, 47, 0.1));
        color: #ff5459;
        border: 1px solid rgba(255, 84, 89, 0.3);
    }
    
    /* Chart containers */
    .chart-container {
        background: linear-gradient(135deg, #fffffe 0%, rgba(50, 184, 198, 0.05) 100%);
        border: 1px solid rgba(94, 82, 64, 0.12);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    /* Status indicator */
    .sync-status {
        display: inline-block;
        padding: 8px 16px;
        background-color: rgba(33, 128, 141, 0.1);
        color: #21808d;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .sync-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #21808d;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 📊 Competitor Intelligence Dashboard")
with col2:
    uploaded_file = st.file_uploader("📁 Upload Excel", type=['xlsx', 'xls'], label_visibility="collapsed")
    if st.session_state.raw_data is not None:
        st.markdown('<div class="sync-status"><span class="sync-indicator"></span>Live - Data Synced</div>', unsafe_allow_html=True)

# Process uploaded file
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
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

# Main dashboard
if st.session_state.raw_data is not None:
    df = st.session_state.raw_data
    
    # Filters section
    st.markdown("---")
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
    
    # KPI Cards
    st.markdown("---")
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
    st.markdown("---")
    st.markdown("### 📰 Recent Articles")
    
    if len(filtered_df) > 0:
        display_df = filtered_df.head(50).copy()
        display_df['SBU'] = display_df['sbu_list'].apply(lambda x: x[0] if len(x) > 0 else 'N/A')
        display_df['Competitor'] = display_df['competitor_list'].apply(lambda x: x[0] if len(x) > 0 else 'N/A')
        display_df['Date'] = display_df['publishedate'].dt.strftime('%m/%d/%Y')
        
        table_df = display_df[['newstitle', 'keyword', 'SBU', 'Competitor', 'source', 'Date']]
        table_df.columns = ['Title', 'Keyword', 'SBU', 'Competitor', 'Source', 'Date']
        
        st.dataframe(table_df, use_container_width=True, height=400)
    else:
        st.info("No articles match your filters")
    
    # Charts
    st.markdown("---")
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📅 Articles by Date")
        
        if len(filtered_df) > 0:
            date_counts = filtered_df.groupby(filtered_df['publishedate'].dt.date).size().reset_index()
            date_counts.columns = ['Date', 'Count']
            date_counts = date_counts.sort_values('Date')
            
            fig_date = px.line(date_counts, x='Date', y='Count', 
                              markers=True,
                              color_discrete_sequence=['#21808d'])
            fig_date.update_traces(fill='tozeroy', fillcolor='rgba(33, 128, 141, 0.1)')
            fig_date.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_date, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🔑 Top Keywords")
        
        if len(filtered_df) > 0:
            keyword_counts = filtered_df['keyword'].value_counts().head(10).reset_index()
            keyword_counts.columns = ['Keyword', 'Count']
            
            fig_keywords = px.bar(keyword_counts, y='Keyword', x='Count',
                                 orientation='h',
                                 color_discrete_sequence=['#21808d'])
            fig_keywords.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_keywords, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    chart_cols2 = st.columns(2)
    
    with chart_cols2[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏢 Articles by SBU")
        
        if len(filtered_df) > 0:
            sbu_counts = {}
            for sbu_list in filtered_df['sbu_list']:
                for sbu in sbu_list:
                    sbu_counts[sbu] = sbu_counts.get(sbu, 0) + 1
            
            if sbu_counts:
                sbu_df = pd.DataFrame(list(sbu_counts.items()), columns=['SBU', 'Count'])
                
                fig_sbu = px.pie(sbu_df, values='Count', names='SBU',
                                color_discrete_sequence=['#21808d', '#32b8c6', '#1d7480', '#2da6b2', '#a84b2f', '#ff5459', '#5e5240'])
                fig_sbu.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_sbu, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols2[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 👥 Top Competitors Mentioned")
        
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
                                 color_discrete_sequence=['#ff5459'])
                fig_comp.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Upload an Excel file to get started")
    st.markdown("""
    ### Expected Excel Format:
    Your Excel file should contain these columns:
    - **keyword**: The search keyword or topic
    - **newstitle**: Article title
    - **SBU**: Strategic Business Unit (comma-separated if multiple)
    - **Competitor**: Competitor names (comma-separated if multiple)
    - **publishedate**: Publication date
    - **source**: News source/publication
    """)
