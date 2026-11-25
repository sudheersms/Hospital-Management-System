"""Premium visual theme for MediCare HMS."""
import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
      --ink: #17213d;
      --muted: #78839c;
      --violet: #7158e8;
      --blue: #4388f5;
      --mint: #27c6b2;
      --coral: #ff8c79;
      --surface: rgba(255,255,255,.88);
      --line: #e8eaf4;
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
      background:
        radial-gradient(ellipse at 88% 4%, rgba(39,198,178,.13), transparent 28%),
        radial-gradient(ellipse at 4% 18%, rgba(113,88,232,.12), transparent 30%),
        linear-gradient(135deg,#f7f8ff 0%,#f6f9ff 48%,#f3fbfa 100%);
      color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(247,248,255,.72); }
    [data-testid="stToolbar"] { right: 1rem; }
    [data-testid="stMainBlockContainer"] { padding-top: 2rem; padding-bottom: 3rem; max-width: 1500px; }

    /* Sidebar */
    [data-testid="stSidebar"] {
      background: linear-gradient(165deg,#171d3c 0%,#242654 48%,#263c62 100%);
      border-right: 1px solid rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    [data-testid="stSidebar"] * { color: #eef1ff; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#b9c2e2; }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
      color:#9fa9d0; font-size:11px; letter-spacing:2px; font-weight:800;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] { gap:7px; }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
      background:rgba(255,255,255,.035); border:1px solid transparent;
      border-radius:13px; padding:9px 12px; transition:all .2s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
      background:rgba(255,255,255,.11); border-color:rgba(255,255,255,.12);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
      background:linear-gradient(100deg,rgba(113,88,232,.48),rgba(67,136,245,.28));
      border-color:rgba(180,176,255,.35);
      box-shadow:inset 3px 0 0 #8c7bff, 0 7px 20px rgba(0,0,0,.12);
    }
    [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.12); }

    /* Typography */
    h1,h2,h3 { color:var(--ink); font-family:'Manrope',sans-serif; letter-spacing:-.7px; font-weight:800; }
    h1 { font-size:2.25rem !important; }
    h2 { font-size:1.55rem !important; }
    h3 { font-size:1.15rem !important; }
    p, label, .stCaption { color:#59647e; }

    /* Hero / cards */
    .hero {
      position:relative; overflow:hidden;
      background:linear-gradient(112deg,#5145cd 0%,#6f5be8 43%,#328fe7 76%,#25bcae 100%);
      padding:30px 34px; border-radius:25px; color:#fff; margin:2px 0 24px;
      box-shadow:0 18px 44px rgba(82,79,190,.22);
    }
    .hero:after {
      content:""; position:absolute; width:250px; height:250px; border-radius:50%;
      right:-65px; top:-120px; border:1px solid rgba(255,255,255,.24);
      box-shadow:0 0 0 24px rgba(255,255,255,.055),0 0 0 50px rgba(255,255,255,.035);
    }
    .hero h1 { color:#fff !important; font-size:30px !important; margin:0 0 7px; }
    .hero p { color:rgba(255,255,255,.86) !important; margin:0; }
    .metric-card {
      position:relative; overflow:hidden; min-height:137px;
      background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(247,248,255,.92));
      border:1px solid rgba(225,228,244,.95); border-radius:21px;
      padding:20px 21px; box-shadow:0 10px 28px rgba(43,55,105,.065);
      transition:transform .2s ease,box-shadow .2s ease;
    }
    .metric-card:before {
      content:""; position:absolute; width:90px; height:90px; border-radius:50%;
      right:-30px; top:-35px; background:linear-gradient(135deg,rgba(113,88,232,.12),rgba(39,198,178,.12));
    }
    .metric-label { color:#78839c; font-size:12px; font-weight:800; letter-spacing:.45px; text-transform:uppercase; }
    .metric-value { color:#20294a; font-family:'Manrope',sans-serif; font-size:35px; font-weight:800; margin-top:10px; line-height:1.1; }
    .metric-note { color:#9aa3b7; font-size:11px; margin-top:7px; }
    .section-card {
      background:var(--surface); border:1px solid var(--line); border-radius:20px;
      padding:20px 22px; margin-bottom:17px; box-shadow:0 8px 25px rgba(43,55,105,.045);
    }

    /* Forms and controls */
    div[data-testid="stForm"] {
      background:rgba(255,255,255,.92); padding:22px; border-radius:19px;
      border:1px solid var(--line); box-shadow:0 9px 28px rgba(43,55,105,.055);
    }
    [data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,[data-testid="stTimeInput"] input,
    [data-testid="stTextArea"] textarea,[data-testid="stSelectbox"] > div > div {
      border-radius:12px !important; border-color:#dfe3f1 !important; background:#fff;
    }
    [data-testid="stTextInput"] input:focus,[data-testid="stNumberInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus { border-color:#8878f1 !important; box-shadow:0 0 0 3px rgba(113,88,232,.12) !important; }
    .stButton>button,.stFormSubmitButton>button,.stDownloadButton>button {
      border-radius:12px; font-weight:800; border:1px solid #e5e7f2;
      padding:.55rem 1rem; transition:all .18s ease;
      box-shadow:0 4px 12px rgba(44,57,111,.06);
    }
    .stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"] {
      background:linear-gradient(100deg,#6857e8,#4388f5 62%,#24bcae);
      color:#fff; border:0;
    }
    .stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover {
      transform:translateY(-1px); box-shadow:0 8px 18px rgba(72,86,170,.14);
    }

    /* Tables, tabs, metrics, alerts */
    [data-testid="stMetric"] {
      background:rgba(255,255,255,.9); border:1px solid var(--line);
      padding:15px 17px; border-radius:17px; box-shadow:0 7px 22px rgba(43,55,105,.045);
    }
    [data-testid="stMetricLabel"] { color:#78839c; font-weight:700; }
    [data-testid="stMetricValue"] { color:#20294a; font-family:'Manrope',sans-serif; font-weight:800; }
    [data-testid="stTabs"] button { font-weight:800; }
    [data-testid="stTabs"] button[aria-selected="true"] { color:#6857e8; }
    [data-testid="stDataFrame"],[data-testid="stTable"] { border:1px solid var(--line); border-radius:15px; overflow:hidden; }
    [data-testid="stExpander"] { background:rgba(255,255,255,.88); border:1px solid var(--line); border-radius:15px; }
    [data-testid="stAlert"] { border-radius:14px; }
    .small-muted { color:#929bb0; font-size:12px; }
    .eyebrow { color:#7d72dc; font-size:11px; font-weight:900; letter-spacing:2px; text-transform:uppercase; }
    @media (max-width: 700px) {
      [data-testid="stMainBlockContainer"] { padding:1rem .8rem 2rem; }
      .hero { padding:23px; border-radius:19px; }
      .hero h1 { font-size:24px !important; }
      .metric-value { font-size:29px; }
    }
    </style>
    """, unsafe_allow_html=True)
