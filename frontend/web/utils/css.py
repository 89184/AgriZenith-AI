import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* Main background */
        .main {
            background-color: #fafafa;
        }
        
        /* Header is now styled inline, so this class is kept as fallback */
        .hero {
            background: linear-gradient(135deg, #FF9933 0%, #FFB347 50%, #138808 100%);
            padding: 2rem 2rem 1.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .hero h1 {
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .hero p {
            font-size: 1.2rem;
            opacity: 0.95;
            margin-top: 0.2rem;
            font-weight: 300;
        }
        
        /* Result card – used in results_display.py */
        .result-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 5px solid #138808;
        }
        .intent-badge {
            display: inline-block;
            background: #e8f5e9;
            color: #1b5e20;
            padding: 0.2rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .entity-tag {
            display: inline-block;
            background: #e3f2fd;
            color: #0d47a1;
            padding: 0.1rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin: 0.2rem 0.2rem;
        }
        
        /* Answer box – clean, consistent */
        .answer-box {
            background: #f8fff4;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #138808;
            font-size: 1.1rem;
            line-height: 1.7;
            color: #1a1a1a;
        }
        
        /* Buttons – Indian green */
        .stButton button {
            background: #138808 !important;
            color: white !important;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            border: none;
            transition: 0.3s;
        }
        .stButton button:hover {
            background: #0d6b05 !important;
            box-shadow: 0 4px 12px rgba(19,136,8,0.3);
            transform: translateY(-2px);
        }
        
        /* Text area – green focus */
        .stTextArea textarea {
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        .stTextArea textarea:focus {
            border-color: #138808;
            box-shadow: 0 0 0 2px rgba(19,136,8,0.2);
        }
        
        /* History items */
        .history-item {
            background: #f5f5f5;
            border-radius: 8px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            border-left: 3px solid #138808;
        }
        .history-item .q {
            font-weight: 500;
        }
        .history-item .a {
            font-size: 0.9rem;
            color: #333;
        }
        
        /* Footer */
        .footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.85rem;
        }
        .footer span {
            font-size: 0.75rem;
            color: #999;
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True)