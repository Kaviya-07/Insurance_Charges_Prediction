import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

from io import BytesIO
from datetime import datetime
from streamlit_option_menu import option_menu


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="InsureAI | Insurance Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL UI STYLING
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F5F9FF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #142B4F;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] .stMarkdown p {
    color: #aab4c5;
}

section[data-testid="stSidebar"] hr {
    display: none;
}

/* Hide Streamlit's sidebar collapse buttons and resize grip. */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarExpandButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarResizeHandle"],
[data-testid="baseButton-header"],
[data-testid="stSidebarHeader"] button,
[data-testid="stSidebarHeader"] [role="button"],
[data-testid="stSidebar"] [aria-label="Collapse sidebar"],
[data-testid="stSidebar"] [aria-label="Expand sidebar"] {
    display: none !important;
    visibility: hidden !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarResizeHandle"] {
    width: 0 !important;
    min-width: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Brand */

.brand-container {
    padding: 20px 12px 28px 12px;
    margin-bottom: 20px;
}

.brand-name {
    color: #ffffff;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
}

.brand-name span {
    color: #93C5FD;
}

.brand-subtitle {
    color: #b5c7df;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 5px;
}

/* Sidebar menu */

.nav-link {
    font-size: 14px !important;
    font-weight: 500 !important;
    border-radius: 0 !important;
    margin: 0 !important;
}

.nav-link-selected {
    background-color: #4A90E2 !important;
    color: white !important;
}

.nav-link:hover {
    background-color: #29466d !important;
}

/* Page headings */

.page-title {
    color: #142B4F;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.page-subtitle {
    color: #71839B;
    font-size: 14px;
    margin-bottom: 25px;
}

/* Section headings */

.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #142B4F;
    font-size: 18px;
    font-weight: 700;
    margin-top: 22px;
    margin-bottom: 15px;
}

.section-heading i {
    color: #4A90E2;
    font-size: 20px;
}

/* Hero */

.hero-card {
    background: linear-gradient(120deg, #142B4F, #315F96);
    padding: 30px;
    border-radius: 16px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(20, 43, 79, 0.12);
}

.hero-card h1 {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-card p {
    color: #DCEBFA;
    font-size: 14px;
    margin-bottom: 0;
}

/* Metric cards */

.metric-card {
    background: white;
    border: 1px solid #DCE8F6;
    border-radius: 13px;
    padding: 19px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(20, 43, 79, 0.04);
    transition: 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(20, 43, 79, 0.09);
}

.metric-label {
    color: #71839B;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    color: #142B4F;
    font-size: 25px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-icon {
    color: #4A90E2;
    font-size: 20px;
}

/* Information cards */

.info-card {
    background: white;
    border: 1px solid #DCE8F6;
    border-radius: 13px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(20, 43, 79, 0.035);
}

.info-card h4 {
    color: #142B4F;
    font-size: 16px;
    font-weight: 700;
}

.info-card p {
    color: #71839B;
    font-size: 13px;
}

/* Result card */

.result-card {
    background: linear-gradient(120deg, #EAF3FF, #DCEBFA);
    border: 1px solid #BBD5F2;
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 6px 18px rgba(74, 144, 226, 0.08);
}

.result-label {
    color: #475569;
    font-size: 13px;
    font-weight: 600;
}

.result-value {
    color: #142B4F;
    font-size: 34px;
    font-weight: 800;
    margin-top: 8px;
}

/* Buttons */

.stButton > button {
    background: #142B4F;
    color: white;
    border: 1px solid #142B4F;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #315F96;
    color: white;
    border: 1px solid #315F96;
}

/* Download buttons */

.stDownloadButton > button {
    background: #ffffff;
    color: #142B4F;
    border: 1px solid #4A90E2;
    border-radius: 8px;
    font-weight: 600;
    transition: 0.2s;
}

.stDownloadButton > button:hover {
    background: #EAF3FF;
    color: #142B4F;
    border-color: #315F96;
}

/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid #DCE8F6;
    border-radius: 10px;
}

/* Input fields */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    border-radius: 8px;
}

/* Chart containers */

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #DCE8F6;
    border-radius: 14px;
    padding: 10px 10px 2px 10px;
    box-shadow: 0 3px 14px rgba(20, 43, 79, 0.045);
    margin-bottom: 16px;
    overflow: hidden;
}

/* Footer */

.footer {
    text-align: center;
    color: #71839B;
    font-size: 12px;
    padding: 25px 0 5px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FILE PATHS
# ============================================================

MODEL_PATH = "insurance_charges_model.pkl"
DATA_PATH = "insurance.csv"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return None
    except Exception as error:
        st.error(f"Unable to load model: {error}")
        return None


model = load_model()


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():
    try:
        data = pd.read_csv(DATA_PATH)
        data = data.drop_duplicates()
        return data
    except FileNotFoundError:
        return None
    except Exception as error:
        st.error(f"Unable to load dataset: {error}")
        return None


df = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def section(title, icon):
    st.markdown(
        f"""
        <div class="section-heading">
            <i class="bi bi-{icon}"></i>
            <span>{title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="display:flex;justify-content:space-between;">
                <div class="metric-label">{label}</div>
                <i class="bi bi-{icon} metric-icon"></i>
            </div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def make_excel(dataframe, sheet_name="Report"):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(
            writer,
            index=False,
            sheet_name=sheet_name
        )

    output.seek(0)
    return output.getvalue()


def format_currency(value):
    return f"${value:,.2f}"


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity range"


# ============================================================
# PLOTLY CHART STYLING
# ============================================================

def style_chart(fig, height=390):

    fig.update_layout(
        template="plotly_white",
        height=height,
        autosize=True,

        font=dict(
            family="Inter, sans-serif",
            size=12,
            color="#52657D"
        ),

        title=dict(
            font=dict(
                family="Inter, sans-serif",
                size=17,
                color="#142B4F"
            ),
            x=0.03,
            xanchor="left",
            y=0.96,
            yanchor="top"
        ),

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        margin=dict(
            l=28,
            r=24,
            t=72,
            b=42
        ),

        hoverlabel=dict(
            bgcolor="#142B4F",
            bordercolor="#142B4F",
            font=dict(
                family="Inter, sans-serif",
                size=12,
                color="#FFFFFF"
            )
        ),

        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.75)",
            font=dict(
                size=11,
                color="#52657D"
            )
        )
    )

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linecolor="#DCE8F6",
        linewidth=1,
        ticks="outside",
        tickcolor="#C7D7EA",
        tickfont=dict(
            size=11,
            color="#71839B"
        ),
        title_font=dict(
            size=12,
            color="#52657D"
        ),
        zeroline=False,
        automargin=True
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EAF0F8",
        gridwidth=1,
        showline=False,
        ticks="outside",
        tickcolor="#C7D7EA",
        tickfont=dict(
            size=11,
            color="#71839B"
        ),
        title_font=dict(
            size=12,
            color="#52657D"
        ),
        zeroline=False,
        automargin=True
    )

    return fig


# ============================================================
# PREDICTION HISTORY
# ============================================================

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="brand-container">
        <div class="brand-name">INSURE<span>AI</span></div>
        <div class="brand-subtitle">INSURANCE ANALYTICS PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    page = option_menu(
        menu_title=None,
        options=[
            "Executive Dashboard",
            "Insurance Prediction",
            "Dataset Explorer",
            "Reports & Downloads",
            "About Project"
        ],
        icons=[
            "grid-1x2-fill",
            "calculator-fill",
            "database-fill",
            "file-earmark-bar-graph-fill",
            "info-circle-fill"
        ],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#142B4F"
            },
            "icon": {
                "color": "#93c5fd",
                "font-size": "17px"
            },
            "nav-link": {
                "font-size": "13px",
                "text-align": "left",
                "margin": "0px",
                "padding": "12px",
                "border-radius": "0px",
                "color": "#cbd5e1"
            },
            "nav-link-selected": {
                "background-color": "#4A90E2",
                "color": "#ffffff",
                "font-weight": "600"
            }
        }
    )

# ============================================================
# CHECK DATASET
# ============================================================

if df is None:

    st.error(
        "Dataset not found. Please place insurance.csv "
        "in the same folder as app.py."
    )

    st.stop()


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    page_header(
        "Executive Dashboard",
        "Monitor insurance charges, customer demographics and key business insights."
    )

    st.markdown("""
    <div class="hero-card">
        <h1>Insurance Analytics Overview</h1>
        <p>
            Analyze customer insurance charges, explore important patterns,
            and understand the factors associated with insurance costs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section("Dashboard Filters", "sliders")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_sex = st.multiselect(
            "Gender",
            options=sorted(df["sex"].dropna().unique()),
            default=sorted(df["sex"].dropna().unique())
        )

    with col2:
        selected_smoker = st.multiselect(
            "Smoking Status",
            options=sorted(df["smoker"].dropna().unique()),
            default=sorted(df["smoker"].dropna().unique())
        )

    with col3:
        selected_region = st.multiselect(
            "Region",
            options=sorted(df["region"].dropna().unique()),
            default=sorted(df["region"].dropna().unique())
        )

    filtered_df = df[
        df["sex"].isin(selected_sex)
        & df["smoker"].isin(selected_smoker)
        & df["region"].isin(selected_region)
    ].copy()

    if filtered_df.empty:

        st.warning("No records match the selected filters.")

    else:

        section("Key Performance Indicators", "speedometer2")

        total_customers = len(filtered_df)
        average_charges = filtered_df["charges"].mean()
        highest_charges = filtered_df["charges"].max()

        smoker_percentage = (
            filtered_df["smoker"].eq("yes").mean() * 100
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card(
                "Total Customers",
                f"{total_customers:,}",
                "people-fill"
            )

        with c2:
            metric_card(
                "Average Charges",
                format_currency(average_charges),
                "cash-stack"
            )

        with c3:
            metric_card(
                "Highest Charges",
                format_currency(highest_charges),
                "graph-up-arrow"
            )

        with c4:
            metric_card(
                "Smoker Percentage",
                f"{smoker_percentage:.1f}%",
                "person-fill"
            )

        # ====================================================
        # CHART 1: DISTRIBUTION OF INSURANCE CHARGES
        # ====================================================

        section("Insurance Data Analysis", "bar-chart-line")

        col1, col2 = st.columns(2)

        with col1:

            fig = px.histogram(
                filtered_df,
                x="charges",
                nbins=30,
                title="Distribution of Insurance Charges",
                color_discrete_sequence=["#4A90E2"]
            )

            fig.update_layout(
                xaxis_title="Insurance Charges ($)",
                yaxis_title="Number of Customers"
            )

            fig.update_traces(
                marker=dict(
                    color="#4A90E2",
                    line=dict(
                        color="#FFFFFF",
                        width=1
                    )
                ),
                opacity=0.88
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 2: AVERAGE CHARGES BY SMOKING STATUS
        # ====================================================

        with col2:

            smoker_data = (
                filtered_df.groupby("smoker")["charges"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                smoker_data,
                x="smoker",
                y="charges",
                color="smoker",
                title="Average Charges by Smoking Status",
                text_auto=".2s",
                color_discrete_map={
                    "yes": "#142B4F",
                    "no": "#4A90E2"
                }
            )

            fig.update_layout(
                xaxis_title="Smoking Status",
                yaxis_title="Average Charges ($)",
                showlegend=False
            )

            fig.update_traces(
                marker_line_color="#FFFFFF",
                marker_line_width=1,
                textposition="outside",
                cliponaxis=False
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        col3, col4 = st.columns(2)

        # ====================================================
        # CHART 3: AVERAGE CHARGES BY REGION
        # ====================================================

        with col3:

            region_data = (
                filtered_df.groupby("region")["charges"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                region_data,
                x="region",
                y="charges",
                color="region",
                title="Average Insurance Charges by Region",
                text_auto=".2s",
                color_discrete_sequence=[
                    "#142B4F",
                    "#315F96",
                    "#4A90E2",
                    "#9CC8F2"
                ]
            )

            fig.update_layout(
                xaxis_title="Region",
                yaxis_title="Average Charges ($)",
                showlegend=False
            )

            fig.update_traces(
                marker_line_color="#FFFFFF",
                marker_line_width=1,
                textposition="outside",
                cliponaxis=False
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 4: AGE VS INSURANCE CHARGES
        # ====================================================

        with col4:

            fig = px.scatter(
                filtered_df,
                x="age",
                y="charges",
                color="smoker",
                size="bmi",
                hover_data=["sex", "region", "children"],
                title="Age vs Insurance Charges",
                color_discrete_map={
                    "yes": "#142B4F",
                    "no": "#4A90E2"
                }
            )

            fig.update_layout(
                xaxis_title="Age",
                yaxis_title="Insurance Charges ($)"
            )

            fig.update_traces(
                marker=dict(
                    opacity=0.76,
                    line=dict(
                        color="#FFFFFF",
                        width=0.7
                    )
                )
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 5: BMI VS INSURANCE CHARGES
        # ====================================================

        section("BMI and Insurance Charges", "activity")

        fig = px.scatter(
            filtered_df,
            x="bmi",
            y="charges",
            color="smoker",
            hover_data=["age", "sex", "region"],
            title="BMI vs Insurance Charges",
            color_discrete_map={
                "yes": "#142B4F",
                "no": "#4A90E2"
            }
        )

        fig.update_layout(
            xaxis_title="BMI",
            yaxis_title="Insurance Charges ($)"
        )

        fig.update_traces(
            marker=dict(
                size=9,
                opacity=0.76,
                line=dict(
                    color="#FFFFFF",
                    width=0.7
                )
            )
        )

        style_chart(fig, height=430)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ====================================================
        # CHART 6: AVERAGE CHARGES BY AGE GROUP
        # ====================================================

        section("Age Group Analysis", "people")

        age_data = filtered_df.copy()

        age_data["Age Group"] = pd.cut(
            age_data["age"],
            bins=[17, 25, 35, 45, 55, 65, 101],
            labels=[
                "18-25",
                "26-35",
                "36-45",
                "46-55",
                "56-65",
                "66+"
            ]
        )

        age_group_data = (
            age_data.groupby(
                "Age Group",
                observed=True
            )["charges"]
            .mean()
            .reset_index()
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                age_group_data,
                x="Age Group",
                y="charges",
                title="Average Insurance Charges by Age Group",
                text_auto=".2s",
                color="charges",
                color_continuous_scale=[
                    "#DCEBFA",
                    "#4A90E2",
                    "#142B4F"
                ]
            )

            fig.update_layout(
                xaxis_title="Age Group",
                yaxis_title="Average Charges ($)",
                coloraxis_showscale=False
            )

            fig.update_traces(
                marker_line_color="#FFFFFF",
                marker_line_width=1,
                textposition="outside",
                cliponaxis=False
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 7: AVERAGE CHARGES BY NUMBER OF CHILDREN
        # ====================================================

        children_data = (
            filtered_df.groupby("children")["charges"]
            .mean()
            .reset_index()
        )

        with col2:

            fig = px.bar(
                children_data,
                x="children",
                y="charges",
                title="Average Charges by Number of Children",
                text_auto=".2s",
                color_discrete_sequence=["#315F96"]
            )

            fig.update_layout(
                xaxis_title="Number of Children",
                yaxis_title="Average Charges ($)"
            )

            fig.update_traces(
                marker_line_color="#FFFFFF",
                marker_line_width=1,
                textposition="outside",
                cliponaxis=False
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 8: CHARGES DISTRIBUTION BY SMOKING STATUS
        # ====================================================

        section("Smoking Impact Analysis", "activity")

        col1, col2 = st.columns(2)

        with col1:

            fig = px.box(
                filtered_df,
                x="smoker",
                y="charges",
                color="smoker",
                title="Insurance Charges Distribution by Smoking Status",
                points="outliers",
                color_discrete_map={
                    "yes": "#142B4F",
                    "no": "#4A90E2"
                }
            )

            fig.update_layout(
                xaxis_title="Smoking Status",
                yaxis_title="Insurance Charges ($)",
                showlegend=False
            )

            fig.update_traces(
                marker=dict(
                    size=5,
                    opacity=0.65
                ),
                line=dict(width=2)
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 9: AVERAGE CHARGES BY BMI CATEGORY
        # ====================================================

        bmi_data = filtered_df.copy()

        bmi_data["BMI Category"] = pd.cut(
            bmi_data["bmi"],
            bins=[0, 18.5, 25, 30, float("inf")],
            labels=[
                "Underweight",
                "Normal",
                "Overweight",
                "Obese"
            ],
            right=False
        )

        bmi_category_data = (
            bmi_data.groupby(
                "BMI Category",
                observed=True
            )["charges"]
            .mean()
            .reset_index()
        )

        with col2:

            fig = px.bar(
                bmi_category_data,
                x="BMI Category",
                y="charges",
                title="Average Charges by BMI Category",
                text_auto=".2s",
                color_discrete_sequence=["#4A90E2"]
            )

            fig.update_layout(
                xaxis_title="BMI Category",
                yaxis_title="Average Charges ($)"
            )

            fig.update_traces(
                marker_line_color="#FFFFFF",
                marker_line_width=1,
                textposition="outside",
                cliponaxis=False
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # CHART 10: CORRELATION HEATMAP
        # ====================================================

        section("Correlation Analysis", "diagram-3")

        numeric_df = filtered_df.select_dtypes(
            include=np.number
        )

        correlation = numeric_df.corr()

        fig = px.imshow(
            correlation,
            text_auto=".2f",
            color_continuous_scale=[
                "#142B4F",
                "#FFFFFF",
                "#9CC8F2"
            ],
            aspect="auto",
            title="Correlation Between Numerical Features"
        )

        fig.update_traces(
            xgap=3,
            ygap=3
        )

        style_chart(fig, height=470)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ====================================================
        # BUSINESS INSIGHTS
        # ====================================================

        section("Business Insights", "lightbulb")

        non_smoker_avg = filtered_df.loc[
            filtered_df["smoker"] == "no",
            "charges"
        ].mean()

        smoker_avg = filtered_df.loc[
            filtered_df["smoker"] == "yes",
            "charges"
        ].mean()

        insight1, insight2 = st.columns(2)

        with insight1:

            if pd.notna(smoker_avg) and pd.notna(non_smoker_avg):

                st.markdown(f"""
                <div class="info-card">
                    <h4><i class="bi bi-activity"></i> Smoking Analysis</h4>
                    <p>
                        Average charges for smokers:
                        <b>{format_currency(smoker_avg)}</b>
                    </p>
                    <p>
                        Average charges for non-smokers:
                        <b>{format_currency(non_smoker_avg)}</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.info("Insufficient smoking-status data for comparison.")

        with insight2:

            highest_region = (
                filtered_df.groupby("region")["charges"]
                .mean()
                .idxmax()
            )

            st.markdown(f"""
            <div class="info-card">
                <h4><i class="bi bi-geo-alt"></i> Regional Analysis</h4>
                <p>
                    Region with the highest average insurance charges:
                </p>
                <h4>{highest_region.title()}</h4>
            </div>
            """, unsafe_allow_html=True)

        section("Export Dashboard Data", "download")

        st.download_button(
            "Download Filtered Dashboard Data (CSV)",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="insurance_dashboard_data.csv",
            mime="text/csv"
        )
        # ============================================================
# INSURANCE PREDICTION
# ============================================================

elif page == "Insurance Prediction":

    page_header(
        "Insurance Charges Prediction",
        "Enter customer information to estimate insurance charges using the trained machine learning model."
    )

    if model is None:

        st.error(
            "Model file not found. Run your Jupyter Notebook "
            "and save the trained model as insurance_charges_model.pkl."
        )

        st.stop()

    section("Customer Information", "person-vcard")

    with st.form("prediction_form"):

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=30,
                step=1
            )

            sex = st.selectbox(
                "Gender",
                ["male", "female"]
            )

            bmi = st.number_input(
                "BMI",
                min_value=10.0,
                max_value=60.0,
                value=25.0,
                step=0.1
            )

        with col2:

            children = st.number_input(
                "Number of Children",
                min_value=0,
                max_value=10,
                value=0,
                step=1
            )

            smoker = st.selectbox(
                "Smoking Status",
                ["no", "yes"]
            )

            region = st.selectbox(
                "Region",
                [
                    "southwest",
                    "southeast",
                    "northwest",
                    "northeast"
                ]
            )

        submitted = st.form_submit_button(
            "Predict Insurance Charges",
            use_container_width=True
        )

    if submitted:

        input_data = pd.DataFrame({
            "age": [age],
            "sex": [sex],
            "bmi": [bmi],
            "children": [children],
            "smoker": [smoker],
            "region": [region]
        })

        try:

            prediction = float(model.predict(input_data)[0])

            if not np.isfinite(prediction):
                raise ValueError("The model returned an invalid prediction.")

            prediction = max(0, prediction)

            bmi_category = get_bmi_category(bmi)

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">
                    <i class="bi bi-currency-dollar"></i>
                    ESTIMATED INSURANCE CHARGES
                </div>
                <div class="result-value">
                    {format_currency(prediction)}
                </div>
                <p style="color:#475569;font-size:13px;margin-top:10px;">
                    This is a machine learning estimate, not an actual insurance quote.
                </p>
            </div>
            """, unsafe_allow_html=True)

            section("Prediction Summary", "clipboard-data")

            result1, result2, result3 = st.columns(3)

            with result1:
                metric_card(
                    "BMI",
                    f"{bmi:.1f}",
                    "activity"
                )

            with result2:
                metric_card(
                    "BMI Category",
                    bmi_category,
                    "heart-pulse"
                )

            with result3:
                metric_card(
                    "Smoking Status",
                    smoker.title(),
                    "person"
                )

            prediction_record = {
                "Date and Time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Age": age,
                "Gender": sex,
                "BMI": bmi,
                "BMI Category": bmi_category,
                "Children": children,
                "Smoker": smoker,
                "Region": region,
                "Predicted Charges": round(prediction, 2)
            }

            st.session_state.prediction_history.append(
                prediction_record
            )

            st.success("Prediction completed successfully.")

        except Exception as error:

            st.error(f"Prediction failed: {error}")

    # Prediction history

    section("Prediction History", "clock-history")

    history = st.session_state.prediction_history

    if history:

        history_df = pd.DataFrame(history)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Prediction History (Excel)",
            data=make_excel(history_df, "Predictions"),
            file_name="insurance_prediction_history.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        if st.button("Clear Prediction History"):

            st.session_state.prediction_history = []
            st.rerun()

    else:

        st.info("No predictions have been generated in this session yet.")


# ============================================================
# DATASET EXPLORER
# ============================================================

elif page == "Dataset Explorer":

    page_header(
        "Dataset Explorer",
        "Explore, filter, inspect and download the insurance dataset."
    )

    section("Dataset Overview", "database")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Total Records",
            f"{len(df):,}",
            "table"
        )

    with col2:
        metric_card(
            "Total Features",
            str(len(df.columns)),
            "columns-gap"
        )

    with col3:
        metric_card(
            "Missing Values",
            str(int(df.isnull().sum().sum())),
            "exclamation-circle"
        )

    # Dataset filters

    section("Filter Dataset", "funnel")

    col1, col2, col3 = st.columns(3)

    with col1:

        gender_filter = st.multiselect(
            "Gender",
            options=sorted(df["sex"].dropna().unique()),
            default=sorted(df["sex"].dropna().unique())
        )

    with col2:

        smoker_filter = st.multiselect(
            "Smoking Status",
            options=sorted(df["smoker"].dropna().unique()),
            default=sorted(df["smoker"].dropna().unique())
        )

    with col3:

        region_filter = st.multiselect(
            "Region",
            options=sorted(df["region"].dropna().unique()),
            default=sorted(df["region"].dropna().unique())
        )

    min_age = int(df["age"].min())
    max_age = int(df["age"].max())

    age_range = st.slider(
        "Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    filtered_data = df[
        (df["sex"].isin(gender_filter))
        & (df["smoker"].isin(smoker_filter))
        & (df["region"].isin(region_filter))
        & (df["age"] >= age_range[0])
        & (df["age"] <= age_range[1])
    ].copy()

    section("Filtered Dataset", "table")

    st.caption(f"Showing {len(filtered_data):,} records")

    st.dataframe(
        filtered_data,
        use_container_width=True,
        hide_index=True
    )

    # Dataset downloads

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "Download Filtered Data (CSV)",
            data=filtered_data.to_csv(index=False).encode("utf-8"),
            file_name="filtered_insurance_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        st.download_button(
            "Download Filtered Data (Excel)",
            data=make_excel(filtered_data, "Insurance Data"),
            file_name="filtered_insurance_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # Statistical summary

    section("Descriptive Statistics", "calculator")

    if not filtered_data.empty:
        st.dataframe(
            filtered_data.describe(),
            use_container_width=True
        )
    else:
        st.info("No data available for descriptive statistics.")

    # Data types

    section("Column Information", "list-columns")

    info_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        info_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# REPORTS AND DOWNLOADS
# ============================================================

elif page == "Reports & Downloads":

    page_header(
        "Reports & Downloads",
        "Generate and export insurance dataset reports in CSV and Excel formats."
    )

    section("Available Reports", "file-earmark-spreadsheet")

    # Summary report

    summary = df.describe().T.reset_index()

    summary.rename(
        columns={"index": "Feature"},
        inplace=True
    )

    section("Dataset Summary Report", "clipboard-data")

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Summary Report (Excel)",
        data=make_excel(summary, "Summary"),
        file_name="insurance_summary_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Full dataset

    section("Complete Dataset", "database")

    st.write(
        f"Total records available: **{len(df):,}**"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "Download Complete Dataset (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="complete_insurance_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        st.download_button(
            "Download Complete Dataset (Excel)",
            data=make_excel(df, "Insurance Data"),
            file_name="complete_insurance_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # Smoking analysis

    section("Smoking Analysis Report", "activity")

    smoking_report = (
        df.groupby("smoker")
        .agg(
            Total_Customers=("charges", "count"),
            Average_Charges=("charges", "mean"),
            Minimum_Charges=("charges", "min"),
            Maximum_Charges=("charges", "max")
        )
        .reset_index()
    )

    st.dataframe(
        smoking_report,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Smoking Analysis (CSV)",
        data=smoking_report.to_csv(index=False).encode("utf-8"),
        file_name="smoking_analysis_report.csv",
        mime="text/csv"
    )

    # Regional analysis

    section("Regional Analysis Report", "geo-alt")

    region_report = (
        df.groupby("region")
        .agg(
            Total_Customers=("charges", "count"),
            Average_Charges=("charges", "mean"),
            Maximum_Charges=("charges", "max")
        )
        .reset_index()
    )

    st.dataframe(
        region_report,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Regional Analysis (Excel)",
        data=make_excel(region_report, "Regional Analysis"),
        file_name="regional_analysis_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Prediction history report

    section("Prediction History Report", "clock-history")

    if st.session_state.prediction_history:

        history_df = pd.DataFrame(
            st.session_state.prediction_history
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Prediction History (Excel)",
            data=make_excel(history_df, "Predictions"),
            file_name="prediction_history_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:

        st.info(
            "Prediction history will appear here after you generate predictions."
        )


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "About Project":

    page_header(
        "About the Project",
        "Learn about the Insurance Charges Prediction machine learning project."
    )

    st.markdown("""
    <div class="hero-card">
        <h1>Insurance Charges Prediction</h1>
        <p>
            A machine learning regression application designed to estimate
            individual medical insurance charges based on customer information.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section("Project Overview", "info-circle")

    st.markdown("""
    <div class="info-card">
        <h4>Problem Statement</h4>
        <p>
            Insurance charges vary depending on factors such as age, BMI,
            smoking habits, number of children and geographical region.
            This project uses regression algorithms to estimate insurance
            charges based on these features.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section("Project Objectives", "bullseye")

    objectives = [
        "Understand and analyze the insurance dataset.",
        "Perform data cleaning and preprocessing.",
        "Explore relationships between customer features and insurance charges.",
        "Build and compare machine learning regression models.",
        "Evaluate model performance using regression metrics.",
        "Develop an interactive prediction application."
    ]

    for item in objectives:
        st.markdown(
            f"""
            <div style="
                background:white;
                padding:12px 16px;
                border-radius:8px;
                margin-bottom:8px;
                border:1px solid #DCE8F6;
                color:#475569;
                font-size:14px;">
                <i class="bi bi-check-circle-fill"
                   style="color:#4A90E2;margin-right:10px;"></i>
                {item}
            </div>
            """,
            unsafe_allow_html=True
        )

    section("Dataset Features", "database")

    feature_info = pd.DataFrame({
        "Feature": [
            "age",
            "sex",
            "bmi",
            "children",
            "smoker",
            "region",
            "charges"
        ],
        "Description": [
            "Age of the customer",
            "Gender of the customer",
            "Body Mass Index",
            "Number of dependent children",
            "Whether the customer smokes",
            "Customer residential region",
            "Individual medical insurance charges"
        ],
        "Type": [
            "Numerical",
            "Categorical",
            "Numerical",
            "Numerical",
            "Categorical",
            "Categorical",
            "Target"
        ]
    })

    st.dataframe(
        feature_info,
        use_container_width=True,
        hide_index=True
    )

    section("Machine Learning Algorithms", "cpu")

    algorithms = [
        "Linear Regression",
        "Ridge Regression",
        "Lasso Regression",
        "Decision Tree Regression",
        "Random Forest Regression",
        "Gradient Boosting Regression",
        "XGBoost Regression (optional)"
    ]

    col1, col2 = st.columns(2)

    for index, algorithm in enumerate(algorithms):

        with col1 if index % 2 == 0 else col2:

            st.markdown(
                f"""
                <div class="info-card">
                    <i class="bi bi-cpu"
                       style="color:#4A90E2;font-size:18px;"></i>
                    <span style="
                        color:#334155;
                        font-size:14px;
                        font-weight:600;
                        margin-left:8px;">
                        {algorithm}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    section("Evaluation Metrics", "clipboard2-data")

    metrics = pd.DataFrame({
        "Metric": [
            "R² Score",
            "Mean Absolute Error (MAE)",
            "Mean Squared Error (MSE)",
            "Root Mean Squared Error (RMSE)"
        ],
        "Purpose": [
            "Measures how much variation in the target is explained by the model.",
            "Measures the average absolute prediction error.",
            "Measures the average squared prediction error.",
            "Measures prediction error in the target's original units."
        ]
    })

    st.dataframe(
        metrics,
        use_container_width=True,
        hide_index=True
    )

    section("Technologies Used", "tools")

    technologies = [
        "Python",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Scikit-learn",
        "Streamlit",
        "Plotly",
        "Jupyter Notebook"
    ]

    st.write(" | ".join(technologies))


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    INSUREAI | Insurance Charges Prediction
    <br>
    Machine Learning Regression Application
</div>
""", unsafe_allow_html=True)
