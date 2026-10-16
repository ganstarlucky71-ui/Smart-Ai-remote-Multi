import streamlit as st
import requests
import re
import urllib3
from urllib.parse import quote

# InsecureRequestWarning chupane ke liye
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# ⚙️ TERA BOT SERVER URL (RENDER/VPS)
# ==========================================
# Ise update karein apna actual server link daalkar agar render pe ho,
# Example: "https://smartai-f1ju.onrender.com"
BOT_SERVER_URL = "https://smartai-f1ju.onrender.com" 

# Kitne bots aap run kar rahe ho (Aapne 8 bole hain)
TOTAL_BOTS = 8

def extract_cid_from_link(text):
    match = re.search(r'(https?://api\.olaparty\.com/d/[\w-]+)', text)
    if match: return match.group(1)
    match = re.search(r'(https?://[\w\.]+/d/[\w-]+)', text)
    if match: return match.group(1)
    match = re.search(r'(https?://[^\s]+)', text)
    if match: return match.group(1)
    return None

def resolve_link_to_cid(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True, verify=False)
        combined_text = response.url + " " + response.text
        cid_match = re.search(r'(C_\d+_V[12]_[A-Z]+_\d+_[A-Z]+|C_\d{10,})', combined_text, re.IGNORECASE)
        if cid_match: 
            return cid_match.group(1).upper()
        return None
    except Exception as e:
        return None

def smart_resolve_input(input_str):
    cid_match = re.search(r'(C_\d+_V[12]_[A-Za-z0-9_]+)', input_str, re.IGNORECASE)
    if cid_match:
        return cid_match.group(1).upper()
    if "http" in input_str:
        link = extract_cid_from_link(input_str)
        if link:
            return link # Ab server khud resolve karega API se
    clean_str = input_str.strip()
    if clean_str.isdigit():
        return clean_str # Server khud resolve karega UID/VID ko
    return None

# ==========================================
# 🌐 STREAMLIT UI DESIGN (RGB DISCO & BLACK BACKGROUND)
# ==========================================
st.set_page_config(page_title="LUCKY GODFATHER | FLEET COMMAND", page_icon="🎮", layout="wide")

st.markdown(
    """
    <style>
    /* Dark Background */
    .stApp { 
        background-color: #050505; 
        background-image: radial-gradient(circle, #0a0a0a 0%, #000000 90%); 
        color: #ffffff; 
        font-family: 'Courier New', Courier, monospace; 
    }
    
    /* 🌈 RGB KEYFRAME ANIMATION FOR TEXT (Red, Yellow, Green, Blue, Pink) */
    @keyframes discoText {
        0% { color: #ff0040; text-shadow: 0 0 10px #ff0040, 0 0 20px #ff0040; }
        20% { color: #ffff00; text-shadow: 0 0 10px #ffff00, 0 0 20px #ffff00; }
        40% { color: #00ff00; text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
        60% { color: #0088ff; text-shadow: 0 0 10px #0088ff, 0 0 20px #0088ff; }
        80% { color: #ff00ff; text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff; }
        100% { color: #ff0040; text-shadow: 0 0 10px #ff0040, 0 0 20px #ff0040; }
    }
    .disco-lucky {
        animation: discoText 1.5s infinite linear;
        font-weight: 900;
        display: inline-block;
    }

    /* GENERAL TEXT STYLING */
    h1, h2, h3, h4 { 
        color: #ffffff !important; 
        font-family: 'Courier New', Courier, monospace; 
        position: relative;
        z-index: 10;
    }
    p { position: relative; z-index: 10; }
    
    /* RGB GAMING BORDER ANIMATION FOR INPUT BOXES AND BUTTONS */
    @keyframes rgbBorder {
        0% { border-color: #ff0040; box-shadow: 0 0 15px #ff0040; }
        20% { border-color: #ffff00; box-shadow: 0 0 15px #ffff00; }
        40% { border-color: #00ff00; box-shadow: 0 0 15px #00ff00; }
        60% { border-color: #0088ff; box-shadow: 0 0 15px #0088ff; }
        80% { border-color: #ff00ff; box-shadow: 0 0 15px #ff00ff; }
        100% { border-color: #ff0040; box-shadow: 0 0 15px #ff0040; }
    }

    /* INPUT BOX HACKER STYLE */
    .stTextInput input { 
        background-color: rgba(10, 10, 10, 0.9) !important; 
        color: #ffffff !important; 
        border-radius: 4px; 
        font-weight: bold; 
        border: 2px solid transparent !important;
        animation: rgbBorder 3s infinite linear;
        position: relative;
        z-index: 10;
    }
    .stTextInput input:focus {
        outline: none !important;
        background-color: #111111 !important;
    }
    
    /* BUTTON RGB GAMING STYLE */
    .stButton>button { 
        background-color: #111111 !important; 
        color: #ffffff !important; 
        border: 2px solid transparent !important; 
        border-radius: 8px; 
        width: 100%; 
        height: 42px; 
        font-weight: bold; 
        transition: 0.3s; 
        animation: rgbBorder 2s infinite linear;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        z-index: 10;
    }
    .stButton>button:hover { 
        background-color: rgba(255,255,255,0.1) !important; 
        transform: scale(1.05); 
    }
    
    /* Status Messages */
    .stAlert {
        background-color: rgba(10, 10, 10, 0.8) !important;
        border: 1px solid #ffffff !important;
        color: #ffffff !important;
        z-index: 10;
        position: relative;
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# HTML Title 
st.markdown("<h1 style='text-align: center;'>☠️ <span class='disco-lucky'>𝐋𝐔𝐂𝐊𝐘</span> 🌎 <span class='disco-lucky'>𝙂𝙤𝙙𝙛𝙖𝙩𝙝𝙚𝙧</span> 🖥️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.5rem; font-weight: bold;'> <span class='disco-lucky'>FLEET CONTROL CENTER</span></p><hr style='border:1px solid #333; position:relative; z-index:10;'>", unsafe_allow_html=True)

# ALL BOTS AT ONCE CONTROL
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.markdown(f"<h3 style='margin-top: 5px; color: #ff3366;'>🚀 ALL BOTS</h3>", unsafe_allow_html=True)
with col2:
    all_target_input = st.text_input("Target", key="input_all", label_visibility="collapsed", placeholder="Sabh bots ke liye Room Link / ID...")
with col3:
    if st.button("🔥 SEND ALL", key="btn_all"):
        if not all_target_input:
            st.warning("⚠️ Link ya ID daalo!")
        else:
            with st.spinner(f"⏳ Sabko bhej raha hu..."):
                target_dest = smart_resolve_input(all_target_input)
                if target_dest:
                    try:
                        api_link = f"{BOT_SERVER_URL.strip('/')}/change_room?link={quote(target_dest)}&bot=all"
                        res = requests.get(api_link, timeout=15, verify=False)
                        if res.status_code == 200:
                            st.success(f"✅ SUCCESS: Sabhi bots shift ho gaye!")
                            st.balloons()
                        else:
                            st.error(f"❌ ERROR {res.status_code}: Server ne mana kar diya.")
                    except Exception as e:
                        st.error(f"❌ SERVER OFFLINE ya UNREACHABLE. URL check karein.")
                else:
                    st.error("❌ INVALID TARGET.")
st.markdown("<hr style='border:1px dashed #333;'>", unsafe_allow_html=True)

# INDIVIDUAL 8 BOTS LOOP CREATION
for i in range(1, TOTAL_BOTS + 1):
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        st.markdown(f"<h4 style='margin-top: 5px; color: #aaaaaa;'>🤖 Bot {i}</h4>", unsafe_allow_html=True)
    
    with col2:
        target_input = st.text_input("Target", key=f"input_{i}", label_visibility="collapsed", placeholder=f"Room Link / ID for Bot {i}...")
        
    with col3:
        if st.button("🚀 CLICK ✅", key=f"btn_{i}"):
            if not target_input:
                st.warning(f"⚠️ Bot {i} ke liye link daalo!")
            else:
                with st.spinner(f"⏳ Bot {i} - TRACING TARGET..."):
                    target_dest = smart_resolve_input(target_input)

                if target_dest:
                    try:
                        api_link = f"{BOT_SERVER_URL.strip('/')}/change_room?link={quote(target_dest)}&bot={i}"
                        res = requests.get(api_link, timeout=15, verify=False)
                        
                        if res.status_code == 200:
                            st.success(f"✅ Bot {i} SUCCESS: Bot gaya!")
                        else:
                            st.error(f"❌ Bot {i} ERROR {res.status_code}")
                    except Exception as e:
                        st.error(f"❌ SERVER OFFLINE ya UNREACHABLE.")
                else:
                    st.error("❌ INVALID TARGET.")

st.markdown("<hr style='border:1px solid #333; position:relative; z-index:10;'><p style='text-align: center; color: #777777; font-weight: bold; position:relative; z-index:10;'>// DEVELOPED BY <span class='disco-lucky'>LUCKY</span> <span class='disco-lucky'>GODFATHER</span> //</p>", unsafe_allow_html=True)
