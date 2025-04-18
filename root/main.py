# import streamlit as st
# import json
# import os
# import sys
# from werkzeug.security import generate_password_hash, check_password_hash
# from tca_analysis.streamlit import StreamLitVisualisation
# # Check if logged in before setting page config
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.username = ""
#     st.session_state.app_executed = False

# # Set page config with sidebar expanded if already logged in
# st.set_page_config(
#     page_title="Login",
#     layout="centered",
#     initial_sidebar_state="expanded" if st.session_state.logged_in else "collapsed"
# )

# # Path to JSON file for users
# USERS_FILE = 'users.json'

# # Create users.json file if it doesn't exist
# if not os.path.exists(USERS_FILE):
#     initial_users = [
#         {
#             "username": "karthi",
#             "password": generate_password_hash("1")
#         },
#         {
#             "username": "kumar",
#             "password": generate_password_hash("1")
#         }
#     ]
#     with open(USERS_FILE, 'w') as f:
#         json.dump(initial_users, f, indent=4)

# def get_users():
#     """Load users from JSON file"""
#     with open(USERS_FILE, 'r') as f:
#         return json.load(f)

# def authenticate_user(username, password):
#     """Check if username and password match"""
#     users = get_users()
#     for user in users:
#         if user["username"] == username and check_password_hash(user["password"], password):
#             return True
#     return False

# def run_tca_analysis():
#     """Run TCA analysis functionality directly"""
#     try:
#         # Update sys.path to include parent directory for imports
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         parent_dir = os.path.dirname(current_dir)
        
#         if parent_dir not in sys.path:
#             sys.path.insert(0, parent_dir)
#         if current_dir not in sys.path:
#             sys.path.insert(0, current_dir)
        
#         # Try to import the TCA module
#         try:
#             # Monkey patch st.set_page_config to prevent it from being called again
#             original_set_page_config = st.set_page_config
#             st.set_page_config = lambda *args, **kwargs: None
            
#             # Import and run TCA analysis
#             from tca_analysis.streamlit import StreamLitVisualisation
#             file_path = '../data/tick_data'
#             StreamLitVisualisation(file_path).perform_analysis()
            
#             # Restore original function
#             st.set_page_config = original_set_page_config
            
#             st.session_state.app_executed = True
#             return True
#         except ImportError as e:
#             st.error(f"Import error: {str(e)}")
#             st.error("Could not import tca_analysis.streamlit module. Make sure it's installed or in the Python path.")
#             return False
#         finally:
#             # Always restore the original function in case of any error
#             if 'original_set_page_config' in locals():
#                 st.set_page_config = original_set_page_config
#     except Exception as e:
#         st.error(f"Error executing application: {str(e)}")
#         st.error(f"Full error details: {type(e).__name__}")
#         return False

# # Custom CSS for styling
# def local_css():
#     st.markdown("""
#     <style>
#         /* Page background - comprehensive targeting */
#         html, body, .stApp, .stApp > div, .login-page, 
#         .block-container, .main > div, .main > div > div {
#             background-color: #000000 !important;
#         }
        
#         /* Main container styling */
#         div.block-container {
#                 max-width: 866px;
#                 padding: 2rem;
#                 margin: auto;
#                 border: 1px solid black;
#                 box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3), 
#                             0 15px 12px rgba(0, 0, 0, 0.22);
#                 position: relative;
#                 background: linear-gradient(90deg, rgb(226 226 231) 31%, rgb(251 251 251) 77%, rgb(253 253 253) 100%);
#         }

        
#         /* Card styling */
#         .login-card {
#             background-color: white;
#             border-radius: 12px;
#             padding: 2rem;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
#             width: 100%;
#             max-width: 450px;
#             margin: 2rem auto;
#             text-align: center;
#         }
        
#         /* Purple gradient background */
#         .card-header {
#             background: linear-gradient(135deg, #424143 0%, #000000 100%);
#             padding: 1.5rem;
#             border-radius: 12px 12px 0 0;
#             color: white;
#         }
        
#         /* Purple button styling */
#         .stButton > button {
#             background-color: #0e0c0e;
#             color: white;
#             border-radius: 5px;
#             border: none;
#             padding: 10px 20px;
#             font-weight: bold;
#             width: 100%;
#             margin-top: 10px;
#             transition: all 0.3s ease;
#         }
        
#         .stButton > button:hover {
#             background-color: #0e0c0e;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#         }
        
#         /* Input fields styling */
#         div[data-baseweb="input"] > div {
#             padding: 8px;
#         }
        
#         /* Headers */
#         h1 {
#             font-weight: bold;
#             font-size: 2rem;
#             margin-bottom: 0.5rem;
#             color: white;
#         }
        
#         h3 {
#             font-weight: normal;
#             font-size: 1rem;
#             color: rgba(255, 255, 255, 0.8);
#             margin-top: 0;
#             margin-bottom: 0.5rem;
#         }
        
#         /* Logo styling */
#         .logo {
#             color: white;
#             font-weight: bold;
#             font-size: 1.2rem;
#             margin-bottom: 1rem;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#         }
        
#         .logo span {
#             margin-left: 8px;
#         }
        
#         /* Sign up link */
#         .signup-link {
#             color: #9900ff;
#             text-decoration: none;
#             font-weight: bold;
#         }
        
#         /* Hide default header */
#         header {
#             visibility: hidden;
#         }
        
#         /* Footer styling */
#         footer {
#             visibility: hidden;
#         }
        
#         /* Hide hamburger menu on login page */
#         .login-page [data-testid="stSidebarNav"] {
#             display: none;
#         }
        
#         /* Responsive adjustments */
#         @media (max-width: 768px) {
#             .login-card {
#                 padding: 1.5rem;
#                 margin: 1rem auto;
#             }
            
#             .card-header {
#                 padding: 1rem;
#                 margin: -1.5rem -1.5rem 1rem -1.5rem;
#             }
            
#             h1 {
#                 font-size: 1.5rem;
#             }
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # Login page
# def login_page():
#     # Add login-page class to body for CSS targeting
#     st.markdown('<div class="login-page">', unsafe_allow_html=True)
    
#     local_css()
    
#     # Card header with gradient
#     st.markdown('''
#     <div class="card-header">
#         <div class="logo">🟣 <span>Costmatix</span></div>
#         <h1>Holla, Welcome Back</h1>
#         <h3>Hey, welcome back to your special place</h3>
#     </div>
#     ''', unsafe_allow_html=True)
    
#     # Login form
#     username = st.text_input("", placeholder="stanley@gmail.com")
#     password = st.text_input("", placeholder="Password", type="password")
    
#     if st.button("Sign In"):
#         if authenticate_user(username, password):
#             st.session_state.logged_in = True
#             st.session_state.username = username
#             # Force page reload with expanded sidebar
#             st.rerun()
#         else:
#             st.error("Invalid username or password")
        
#     # Close the card container
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Close the login-page wrapper
#     st.markdown('</div>', unsafe_allow_html=True)

# # Main application
# # def main_app():
# #     

#     # st.title(f"Welcome, {st.session_state.username}!")
    
#     # Add a sidebar with logout option
#     # st.markdown("""
#     #     <style>
#     #     div[data-testid="stSidebar"] button[kind="primary"] {
#     #         background-color: black;
#     #         color: white;
#     #     }
#     #     </style>
#     # """, unsafe_allow_html=True)

#     # with st.sidebar:
#     #     if st.button("Logout", key="logout_button", type="primary", use_container_width=True):
#     #         st.session_state.logged_in = False
#     #         st.session_state.username = ""
#     #         st.session_state.app_executed = False
#     #         st.rerun()
    
#     # # Run the TCA analysis app directly
#     # if not st.session_state.app_executed or st.button("Reload Analysis"):
#     #     with st.spinner("Loading TCA Analysis..."):
#     #         success = run_tca_analysis()
#     #         if not success:
#     #             st.error("Failed to load TCA Analysis application")
#     #             st.info("If you're seeing import errors, check that the tca_analysis module is correctly installed or in the Python path.")

# def main_app():
#     # Monkey patch st.set_page_config before import
#     original_set_page_config = st.set_page_config
#     st.set_page_config = lambda *args, **kwargs: None
    
#     # Now import the module and run the analysis
#     from tca_analysis.streamlit import StreamLitVisualisation
#     file_path = '../data/tick_data'
    
#     try:
#         StreamLitVisualisation(file_path).perform_analysis()
#     finally:
#         # Restore the original function
#         st.set_page_config = original_set_page_config
#     with st.sidebar:
#         if st.button("Logout", key="logout_button", type="primary", use_container_width=True):
#             st.session_state.logged_in = False
#             st.session_state.username = ""
#             st.session_state.app_executed = False
#             st.rerun()

# # Main app logic
# if st.session_state.logged_in:
#     main_app()
# else:
#     login_page()

import streamlit as st
import json
import os
import sys
from werkzeug.security import generate_password_hash, check_password_hash

# Check if logged in before setting page config
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.app_executed = False
    st.session_state.current_page = "dashboard"

# Set page config with sidebar expanded if already logged in
st.set_page_config(page_title="Financial TCA Platform",
                   layout="centered",
                   initial_sidebar_state="expanded"
                   if st.session_state.logged_in else "collapsed")

# Path to JSON file for users
USERS_FILE = 'users.json'

# Create users.json file if it doesn't exist
if not os.path.exists(USERS_FILE):
    initial_users = [{
        "username": "karthi",
        "password": generate_password_hash("1")
    }, {
        "username": "kumar",
        "password": generate_password_hash("1")
    }]
    with open(USERS_FILE, 'w') as f:
        json.dump(initial_users, f, indent=4)


def get_users():
    """Load users from JSON file"""
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def authenticate_user(username, password):
    """Check if username and password match"""
    users = get_users()
    for user in users:
        if user["username"] == username and check_password_hash(
                user["password"], password):
            return True
    return False


def run_tca_analysis():
    """Run TCA analysis functionality directly"""
    try:
        # Update sys.path to include parent directory for imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        # Try to import the TCA module
        try:
            # Monkey patch st.set_page_config to prevent it from being called again
            original_set_page_config = st.set_page_config
            st.set_page_config = lambda *args, **kwargs: None

            # Import and run TCA analysis
            from tca_analysis.streamlit import StreamLitVisualisation
            file_path = './data/tick_data'
            StreamLitVisualisation(file_path).perform_analysis()

            # Restore original function
            st.set_page_config = original_set_page_config

            st.session_state.app_executed = True
            return True
        except ImportError as e:
            st.error(f"Import error: {str(e)}")
            st.error(
                "Could not import tca_analysis.streamlit module. Make sure it's installed or in the Python path."
            )
            return False
        finally:
            # Always restore the original function in case of any error
            if 'original_set_page_config' in locals():
                st.set_page_config = original_set_page_config
    except Exception as e:
        st.error(f"Error executing application: {str(e)}")
        st.error(f"Full error details: {type(e).__name__}")
        return False


# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
        /* Page background - comprehensive targeting */
        html, body, .stApp, .stApp > div, .login-page, 
        .block-container, .main > div, .main > div > div {
            background-color: #000000 !important;
        }
        
        /* Main container styling */
        div.block-container {
                max-width: 900px;
                padding: 1.5rem;
                margin: auto;
                border: none;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0), 
                            0 15px 12px rgba(0, 0, 0, 0);
                position: relative;
                background: linear-gradient(90deg, rgb(24, 24, 27) 31%, rgb(36, 36, 40) 77%, rgb(42, 42, 46) 100%);
        }
        
        /* Remove streamlit default elements */
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        [data-testid="stToolbar"] {display:none !important;}
        [data-testid="stDecoration"] {display:none !important;}
        [data-testid="stStatusWidget"] {visibility:hidden;}
        
        /* Card styling with animation */
        .login-card {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            width: 100%;
            max-width: 450px;
            margin: 2rem auto;
            text-align: center;
            animation: fadeIn 0.8s ease-in-out;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        /* Purple gradient background */
        .card-header {
            background: linear-gradient(135deg, #424143 0%, #000000 100%);
            padding: 1.5rem;
            border-radius: 12px 12px 0 0;
            color: white;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        /* Button styling with animation */
        .stButton > button {
            background-color: #0e0c0e;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            width: 100%;
            margin-top: 10px;
            transition: all 0.3s ease;
            animation: fadeIn 0.8s ease-in-out;
        }
        
        .stButton > button:hover {
            background-color: #1E1E1E;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }
        
        /* Input fields styling with animation */
        div[data-baseweb="input"] {
            animation: fadeIn 0.6s ease-in-out;
        }
        
        div[data-baseweb="input"] > div {
            padding: 8px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        div[data-baseweb="input"]:focus-within > div {
            box-shadow: 0 0 0 2px rgba(66, 65, 67, 0.5);
            transform: translateY(-1px);
        }
        
        /* Headers with animation */
        h1 {
            font-weight: bold;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: white;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        h3 {
            font-weight: normal;
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0;
            margin-bottom: 0.5rem;
            animation: fadeIn 0.7s ease-in-out;
        }
        
        /* Logo styling with animation */
        .logo {
            color: white;
            font-weight: bold;
            font-size: 1.6rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        .logo span {
            background: linear-gradient(90deg, #8a8aff, #c2c2ff);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 3s infinite ease-in-out;
            letter-spacing: 1px;
        }
        
        /* Sign up link */
        .signup-link {
            color: #9900ff;
            text-decoration: none;
            font-weight: bold;
        }
        
        /* Hide default header */
        header {
            visibility: hidden;
        }
        
        /* Footer styling */
        footer {
            visibility: hidden;
        }
        
        /* Hide hamburger menu on login page */
        .login-page [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #121212;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            div.block-container {
                padding: 1rem;
            }
            
            .login-card {
                padding: 1.5rem;
                margin: 1rem auto;
            }
            
            .card-header {
                padding: 1rem;
            }
            
            h1 {
                font-size: 1.5rem;
            }
        }
        
        @media (max-width: 480px) {
            div.block-container {
                padding: 0.5rem;
            }
            
            .login-card {
                padding: 1rem;
            }
        }
    </style>
    """,
                unsafe_allow_html=True)


# Login page
def login_page():
    # Add login-page class to body for CSS targeting
    st.markdown('<div class="login-page">', unsafe_allow_html=True)

    local_css()

    # Card header with gradient
    st.markdown('''
    <div class="card-header">
        <div class="logo"><span>Costmatix</span></div>
        <h1>Welcome Back</h1>
        <h3>Your financial insights await</h3>
    </div>
    ''',
                unsafe_allow_html=True)

    # Login form with enhanced styling
    st.markdown("""
    <style>
        /* Style the error message with animation */
        .stAlert {
            border: none !important;
            animation: fadeIn 0.5s ease-in-out;
        }
        .st-bq {
            
            border-left-color: #ff3860 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Form with improved placeholders and hidden labels for accessibility
    st.markdown("""
    <style>
        /* Custom styling for input boxes */
        div[data-baseweb="input"] > div {
            color: black;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 8px;
        }
        div[data-baseweb="input"]:focus-within > div {
            border-color: white;
            box-shadow: 0 0 0 2px rgba(138, 138, 255, 0.5);
        }
        input {
            color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)

    username = st.text_input("", placeholder="Username or Email", label_visibility="collapsed")
    password = st.text_input("", placeholder="Password", type="password", label_visibility="collapsed")
    
  
    
    # Enhanced button
    if st.button("SIGN IN"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            # Force page reload with expanded sidebar
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Close the login-page wrapper
    st.markdown('</div>', unsafe_allow_html=True)


def main_app():
    # Monkey patch st.set_page_config before import
    original_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None

    # Now import the module and run the analysis
    from tca_analysis.streamlit import StreamLitVisualisation
    file_path = '../data/tick_data'

    try:
        StreamLitVisualisation(file_path).perform_analysis()
    finally:
        # Restore the original function
        st.set_page_config = original_set_page_config

    # Enhanced sidebar with better styling
    with st.sidebar:
        # Add sidebar styling
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #121212 0%, #1a1a1a 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            [data-testid="stSidebar"] hr {
                margin-top: 1rem;
                margin-bottom: 1rem;
                border: 0;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            .user-info {
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                background-color: rgba(255, 255, 255, 0.05);
                animation: fadeIn 0.5s ease-in-out;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        </style>
        """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Logout button at the bottom
        if st.button("Logout",
                     key="logout_button",
                     type="primary",
                     use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.app_executed = False
            st.rerun()


# Main app logic
if st.session_state.logged_in:
    main_app()
else:
    login_page()
