import streamlit as st
import pandas as pd
from streamlit import cache_data
from tca_analysis.benchmarks import *
from tca_analysis.metrics import *
from tca_analysis.analysis import TCAAnalysis
from helper.plots import *
import base64
import time
import datetime 

def set_sidebar_background(image_file):
    """Set a background image for the sidebar in Streamlit."""
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
    """
    <style>
        /* Hide the Streamlit sidebar navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Set sidebar width to 30% of the screen when expanded */
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 20% !important;    
            max-width: 20% !important;
            width: 20% !important;
            overflow: hidden;
        }
        
        /* Adjust sidebar width when collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] {
            min-width: 0 !important;
            max-width: 0 !important;
            width: 0 !important;
        }
        
        /* Make main content area take 70% width when sidebar is expanded */
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
            max-width: 80% !important;
            width: 80% !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Make main content area take 100% width and center it when sidebar is collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
            max-width: 80% !important;
            width: 80% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        [data-testid="stMainBlockContainer"]{
            width: 100%;
            padding: 6rem 1rem 10rem;
            max-width: 58rem;
        }
        
        /* Fix for main content container */
        .main .block-container {
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    sidebar_css = f"""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
    </style>
    """
    st.markdown(sidebar_css, unsafe_allow_html=True)
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
class StreamLitVisualisation:
    def __init__(self, market_data_path) -> None:
        st.set_page_config(page_title="TCA", layout="wide")
        hide_expand_icon = """
        <style>
            button[title="View fullscreen"] {display: none !important;}
        </style>
        """
        st.markdown(hide_expand_icon, unsafe_allow_html=True)
        hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                .stDeployButton {display: none;}
            </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        hide_running_stop = """
            <style>
                .st-emotion-cache-klqnuk {display: none !important;} /* Hides "Running..." */
            </style>
            <style>
                [data-testid="stToolbarActions"] {display: none !important;}
            </style>
        """
        st.markdown(hide_running_stop, unsafe_allow_html=True)
        # loading_placeholder = st.empty()
        # with loading_placeholder.container():
        #     st.markdown("<h2 style='text-align: center;'>🔄 Refreshing... Please Wait</h2>", unsafe_allow_html=True)
        # loading_placeholder.empty()
        col1, col2, col3 = st.columns([4, 4, 1])  # Adjust the column width ratios as needed
        with col3:
            img_base64 = get_base64_image("../image/logo24.webp")
            
            st.markdown(
                f"""
                <style>
                    .logo {{
                        width: 80px;
                        margin-top: -40px;
                    }}
                </style>
                <img class="logo" src="data:image/webp;base64,{img_base64}">
                """,
                unsafe_allow_html=True
            )
        set_sidebar_background("../image/background_dark.jpg")
        st.sidebar.markdown("<div style='padding-top: -30px;'></div>", unsafe_allow_html=True)
        st.sidebar.image("../image/White.png",width=200)
        st.sidebar.markdown(
        "<p style='color: white; font-size: 18px; font-weight: bold;margin-bottom: 1px;'> Transaction Cost Analysis</p>",
        unsafe_allow_html=True
        )
        st.sidebar.image("../image/rimage.png",width=150)
        # st.markdown( """ <style> div[data-testid="stMarkdownContainer"] div .st-emotion-cache-uzeiqp.e1nzilvr4 { display:none !important; } </style> """, unsafe_allow_html=True )
        st.markdown(
            """
            <div style="text-align: justify; font-size: 16px;">
                Strobus TCA application - <b>COSTMATIX</b> - has been designed to improve trade execution efficiency, 
                reduce transaction costs, and ensure compliance. By integrating real-time data processing, 
                benchmark analysis, and advanced visualization, institutions can optimize trading strategies 
                and enhance transparency in equity markets.  
            </div>
            """,
            unsafe_allow_html=True
        )
        self.market_data_path = market_data_path
        self.BENCHMARKS = [ArrivalPriceBenchmark, HighBenchmark, LowBenchmark, MarketVWAPBenchmark, MidBenchmark, SpreadBenchmark, BestAskBenchmark, BestBidBenchmark]
        self.METRICS = [VWAPMetric, TWAPMetric, SlippageMetric, BestPrice, WorstPrice, SlippageMarketVWAP, MarketImpactMetric]
        self.TCA = TCAAnalysis(market_data_path)
        st.sidebar.markdown(
        """
        <style>
            /* Center align all text in the file uploader */
            div[data-testid="stFileUploader"] {
                display: flex;
                flex-direction: column;
                align-items: center;
                # justify-content: center;
                text-align: center;
            }

            /* Remove border and background for a cleaner look */
            div[data-testid="stFileUploader"] * {
                border: none;
                color: white;
                background-color: transparent;
            }

            /* Make the section background transparent */
            div[data-testid="stFileUploader"] section {
                background: transparent;
            }

            /* Style the upload button */
            div[data-testid="stFileUploader"] button {
               align-self: center;
                border: 1px solid white;
            }

            /* Hide the default label */
            div[data-testid="stFileUploader"] label {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
        )

        st.sidebar.markdown(
        "<h4 style='color: white;text-align: center;'>Upload a CSV file to start the analysis</h4>", 
        unsafe_allow_html=True
        )

        self.uploaded_file = st.sidebar.file_uploader("", type=['csv'])
        temp = True if self.uploaded_file else False
        if not temp:
            today = datetime.date.today()
            st.sidebar.markdown(
            """
            <style>
                /* Make all text in the sidebar white */
                section[data-testid="stSidebar"] div {
                    color: white;
                    font-weight: bold;
                }
                /* Make input fields text black */
                input[type="date"], input[type="text"], select {
                    color: black;
                }
            </style>
            """,
            unsafe_allow_html=True
            )
            # st.sidebar.date_input("Start Date", today, key="start_date")
            start_date = st.sidebar.date_input("Start Date", today, key=f"start_date_{id(self)}")
            # st.sidebar.date_input("End Date", today, key="end_date")
            end_date = st.sidebar.date_input("End Date", today, key=f"end_date_{id(self)}")
            select_component = st.sidebar.radio(
            "Select the analysis level",
            ("Aggregated", "Company Level"),
            key="analysis_level_1"
            )
            if select_component == "Aggregated":
                st.markdown('<div className="space-y-4">', unsafe_allow_html=True)
                st.markdown('<h1 className="text-2xl font-bold">Summary Analytics of the Trades</h2>', unsafe_allow_html=True)
                st.markdown(
                """
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); font-size: 16px; margin-bottom: 10px; display: block;">
                    Descriptive Analytics
                </div>
                
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); font-size: 16px; margin-bottom: 10px; display: block;">
                    Slippage across Venue, Stock and Currency
                </div>
                
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); font-size: 16px; margin-bottom: 10px; display: block;">
                    Slippage across different timespan
                </div>
                
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); font-size: 16px; display: block;">
                    Slippage across Brokers and Traders
                </div>
                """,
                unsafe_allow_html=True
                )
            if select_component == "Company Level":
                st.markdown('<div className="space-y-4">', unsafe_allow_html=True)
                st.markdown('<h1 className="text-2xl font-bold">Company Level Analytics of the Trades</h2>', unsafe_allow_html=True)
                st.markdown(
                """
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); font-size: 16px; margin-bottom: 10px;">
                    Slippage Analytics
                </div>
                
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); font-size: 16px; margin-bottom: 10px;">
                    Trade Analytics
                </div>
                """,
                unsafe_allow_html=True
                )
            st.sidebar.markdown(
                """
                <style>
                    .sidebar-footer {
                        position: absolute;
                        bottom: -130px;
                        left: 0;
                        width: 100%;
                        text-align: left;
                        font-size: 14px;
                        color: white ;
                        z-index: 999;
                        font-weight: normal;
                        margin-bottom: 0;
                        margin-left: 0%;
                        padding:0%;
                        }
                    .css-1d391kg {
                        position: relative;  /* Ensures the footer stays within the sidebar */
                        min-height: 100vh;  /* Makes sure sidebar expands fully */
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-end; /* Pushes footer to bottom */
                    }
                </style>
                <div class="sidebar-footer">
                    ©STROBUS InfoSoft LLC
                </div>
                """,
                unsafe_allow_html=True
            )    
    def perform_analysis(self):
        if self.uploaded_file:
            trades_df = pd.read_csv(self.uploaded_file)
            tca_result_df = self.tca_analysis(trades_df, 100)
            tca_result_df = self.add_datetime_components(tca_result_df)
            tca_result_df = self.add_latency_duration_components(tca_result_df)
            self.visualise_analysis(tca_result_df)
    # def perform_analysis(self):
    #     if self.uploaded_file:
    #         progress_bar = st.progress(0)
    #         status_text = st.empty()
    #         status_text.text("Processing.........")
    #         # status_text.text("Loading data...")
    #         trades_df = pd.read_csv(self.uploaded_file)
    #         # progress_bar.progress(25)

    #         # status_text.text("Running TCA analysis...")
    #         tca_result_df = self.tca_analysis(trades_df, 100)
    #         # progress_bar.progress(50)

           
    #         tca_result_df = self.add_datetime_components(tca_result_df)
    #         # progress_bar.progress(75)

    #         # status_text.text("Finalizing analysis...")
    #         tca_result_df = self.add_latency_duration_components(tca_result_df)
    #         # progress_bar.progress(100)

    #         # Clear loading elements
    #         progress_bar.empty()
    #         status_text.empty()
    #         self.visualise_analysis(tca_result_df)



    @cache_data
    def tca_analysis(_self, trades_df, arrival_latency):
        result = _self.TCA.run(trades_df, arrival_latency, _self.BENCHMARKS, _self.METRICS)
        result.to_csv('../data/tca_results.csv')
        return result

    def add_datetime_components(self, data):
        data['date'] = pd.to_datetime(data['trade_time']).dt.date
        data['hour'] = pd.to_datetime(data['trade_time']).dt.hour
        data['weekday'] = pd.to_datetime(data['trade_time']).dt.weekday
        data['month'] = pd.to_datetime(data['trade_time']).dt.month
        return data

    def add_latency_duration_components(self, data):
        data['arrival_latency'] = (pd.to_datetime(data['arrival_time']) - pd.to_datetime(data['signal_time']))
        data['execution_latency'] = (pd.to_datetime(data['trade_time']) - pd.to_datetime(data['signal_time']))
        data['arrival_latency_duration'] = data['arrival_latency'].dt.microseconds / 1000 + data['arrival_latency'].dt.seconds * 1000
        data['execution_latency_duration'] = data['execution_latency'].dt.microseconds / 1000 + data['execution_latency'].dt.seconds * 1000
        return data
    
    def visualise_analysis(self, data):

        data_trades = data.dropna(subset=['order_id'])
        min_date, max_date = data_trades['date'].min(), data_trades['date'].max()

        if pd.isnull(min_date) or pd.isnull(max_date):
            st.error("Date range calculation failed due to missing values.")
            return
        st.sidebar.markdown(
        """
        <style>
            /* Make all text in the sidebar white */
            section[data-testid="stSidebar"] div {
                color: white;
                font-weight: bold;
            }
            /* Make input fields text black */
            input[type="date"], input[type="text"], select {
                color: black;
            }
        </style>
        """,
        unsafe_allow_html=True
        )
        start_date = st.sidebar.date_input("Start Date", min_date, key="start_date")
        end_date = st.sidebar.date_input("End Date", max_date, key="end_date")
        select_component = st.sidebar.radio(
            "Select the analysis level",
            ("Aggregated", "Company Level")
        )
        st.sidebar.markdown(
        """
        <style>
            /* Change dropdown text color */
            div[data-baseweb="select"] div {
                color:black !important;
                font-weight: 100;
            }
        </style>
        """,
        unsafe_allow_html=True
        )
        try:
            if select_component == "Company Level":
                selected_company = st.sidebar.selectbox(
                    "Select a Company",
                    data['RIC'].unique(),
                )
                filtered_data_company = data[(data['RIC'] == selected_company) &
                                        (data['date'] >= start_date) &
                                        (data['date'] <= end_date)]    
                if filtered_data_company.empty:
                    st.warning("No trades available for the selected company or date range.")
                else:
                    self.render_company_level_analysis(filtered_data_company)            
                # self.render_company_level_analysis(filtered_data_company)
            
            elif select_component == "Aggregated":
                filtered_data_agg = data[(data['date'] >= start_date) &
                                        (data['date'] <= end_date)]
                self.render_aggregated_analyis(filtered_data_agg)

        except Exception as e:
            st.error(f"An error occurred: {e}")           
    @cache_data
    def render_aggregated_analyis(_self, filtered_data):
        st.title('Summary Analytics of the Trades')
        with st.expander("Descriptive Analytics"):
            col1, col2 = st.columns(2)
            with col1:
                display_desc_stats(filtered_data)
            with col2:
                plot_arrival_latemcy(filtered_data)

        with st.expander("Slippage accorss venue, currency and stock "):
            col1, col2 = st.columns(2)
            with col1:
                plot_slippage_by(filtered_data, 'venue',)
                plot_slippage_by(filtered_data, 'currency')
                plot_slippage_by(filtered_data, 'RIC')

            with col2:
                plot_slippage_dist_by(filtered_data, 'venue')
                plot_slippage_dist_by(filtered_data, 'currency') 
                plot_slippage_dist_by(filtered_data, 'RIC')

        with st.expander("Slippage accorss different timespan"):
            col1, col2 = st.columns(2)
            with col1:
                plot_slippage_by(filtered_data, 'hour')
                plot_slippage_by(filtered_data, 'weekday')
            with col2:
                plot_slippage_by(filtered_data, 'month')

        with st.expander("Slippage accorss brokers and traders"):
            col1, col2 = st.columns(2)
            with col1:
                plot_slippage_by(filtered_data, 'broker_id')

            with col2:
                plot_slippage_by(filtered_data, 'trader_id')
        st.sidebar.markdown(
                    """
                    <style>
                        .sidebar-footer {
                            position: absolute;
                            bottom: -150px;
                            left: 0;
                            width: 100%;
                            text-align: left;
                            font-size: 14px;
                            color: white ;
                            z-index: 999;
                            font-weight: normal;
                            margin-bottom: 0;
                            margin-left: 0%;
                            padding:0%;
                         }
                        .css-1d391kg {
                            position: relative;  /* Ensures the footer stays within the sidebar */
                            min-height: 100vh;  /* Makes sure sidebar expands fully */
                            display: flex;
                            flex-direction: column;
                            justify-content: flex-end; /* Pushes footer to bottom */
                        }
                    </style>
                    <div class="sidebar-footer">
                        ©STROBUS InfoSoft LLC
                    </div>
                    """,
                    unsafe_allow_html=True
            ) 
    def render_company_level_analysis(self,filtered_data):
        st.title('Company Level Analytics of the Trades')
        if filtered_data.empty:
            st.warning("No trades available for the selected company or date range.")
            return
                  
        buy, sell, all = st.tabs(["Buy", "Sell", "All Trades"])

        with buy:
            filtered_data_buy = filtered_data.loc[filtered_data['position']==1]
            with st.expander("Slippage Analytics"):
                col1, col2 = st.columns(2)
                with col1:
                    plot_slippage_through_time(filtered_data_buy)
                    plot_against_trade_volume(filtered_data_buy, 'slippage')
                with col2:
                    plot_slippage_distribution(filtered_data_buy)

            with st.expander("Trade Analytics"):
                col1, col2 = st.columns(2)
                with col1:
                    plot_prices(filtered_data_buy, 'buy')                   

                with col2:
                    order_id = st.selectbox('order_id', filtered_data_buy.order_id.unique())
                    plot_trade_recap(filtered_data, order_id)
                    

        with sell:
            col1, col2 = st.columns(2)
            filtered_data_sell = filtered_data.loc[filtered_data['position']==-1]

            with st.expander("Slippage Analytics"):
                col1, col2 = st.columns(2)
                with col1:
                    plot_slippage_through_time(filtered_data_sell)
                    plot_against_trade_volume(filtered_data_sell, 'slippage')
                with col2:
                    plot_slippage_distribution(filtered_data_sell)

            with st.expander("Trade Analytics"):
                col1, col2 = st.columns(2)
                with col1:
                    order_id = st.selectbox('order_id', filtered_data_sell.order_id.unique())
                    plot_trade_recap(filtered_data, order_id)
                    
                with col2:
                    plot_prices(filtered_data_sell, 'sell')                   

        with all:
            col1, col2 = st.columns(2)
            with col1:
                plot_slippage_distribution(filtered_data)
                order_id = st.selectbox('order_id', filtered_data.dropna(subset = 'order_id').order_id.unique())
                plot_trade_recap(filtered_data, order_id)
            with col2:
                plot_against_trade_volume(filtered_data, 'market_impact')
                plot_arrival_latemcy(filtered_data)
        st.sidebar.markdown(
                    """
                    <style>
                        .sidebar-footer {
                            position: absolute;
                            bottom: -130px;
                            left: 0;
                            width: 100%;
                            text-align: left;
                            font-size: 14px;
                            color: white ;
                            z-index: 999;
                            font-weight: normal;
                            margin-bottom: 0;
                            margin-left: 0%;
                            padding:0%;
                         }
                        .css-1d391kg {
                            position: relative;  /* Ensures the footer stays within the sidebar */
                            min-height: 100vh;  /* Makes sure sidebar expands fully */
                            display: flex;
                            flex-direction: column;
                            justify-content: flex-end; /* Pushes footer to bottom */
                        }
                    </style>
                    <div class="sidebar-footer">
                        ©STROBUS InfoSoft LLC
                    </div>
                    """,
                    unsafe_allow_html=True
            )  
        # st.sidebar.markdown(
        #         """
        #         <div class="sidebar-credits" style="font-size: 20px;">
        #             <footer>©STROBUS InfoSoft LLC</footer>
        #         </div>
        #         """,
        #         unsafe_allow_html=True
        # )