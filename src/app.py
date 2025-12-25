#Version 2
import streamlit as st
import cv2
import numpy as np
from preprocessing import load_image, preprocess_image
from ocr_engine import OCREngine
from text_extraction import TextExtractor

# -----------------------------------------------------------------------------
# 1. VISUAL CONFIGURATION & CSS ENGINE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Waybill Intelligence | OCR",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# THEME ENGINE: BLACK & PURPLE GLOW
st.markdown("""
    <style>
        /* IMPORT MODERN FONT */
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&family=Inter:wght@300;400;600&display=swap');

        /* GLOBAL RESET */
        .stApp {
            background-color: #000000; /* True Black */
            background-image: radial-gradient(circle at 50% 0%, #1a0033 0%, #000000 70%);
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
        }

        /* HEADERS */
        h1, h2, h3 {
            font-family: 'Rajdhani', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        h1 {
            background: linear-gradient(90deg, #d8b4fe 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #2e1065;
        }
        
        /* CUSTOM CARD CONTAINER (GLASSMORPHISM) */
        .glass-card {
            background: rgba(20, 20, 20, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid #3b0764;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 30px rgba(109, 40, 217, 0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .glass-card:hover {
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
            border-color: #7c3aed;
        }

        /* FILE UPLOADER STYLING */
        [data-testid="stFileUploader"] {
            background-color: #0a0a0a;
            border: 2px dashed #4c1d95;
            border-radius: 12px;
            padding: 20px;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #a78bfa;
        }

        /* PRIMARY BUTTON (NEON GLOW) */
        div.stButton > button {
            background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%);
            color: white;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 20px;
            letter-spacing: 1px;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            width: 100%;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(124, 58, 237, 0.5);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%);
            box-shadow: 0 0 25px rgba(139, 92, 246, 0.8);
            transform: scale(1.02);
        }

        /* RESULTS HUD (HEADS UP DISPLAY) */
        .hud-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }
        .hud-box {
            background: #0f0518;
            border-left: 3px solid #a855f7;
            padding: 15px;
            border-radius: 4px;
        }
        .hud-label {
            color: #9ca3af;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        .hud-value {
            color: #fff;
            font-size: 1.5rem;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
        }
        
        /* FOOTER */
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #4b5563;
            font-size: 0.8rem;
        }
        
        /* IMAGE BORDER */
        img {
            border-radius: 8px;
            border: 1px solid #333;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOGIC (UNCHANGED)
# -----------------------------------------------------------------------------

# Initialize Engine (Cached to prevent reloading)
@st.cache_resource
def get_extractor():
    ocr = OCREngine()
    extractor = TextExtractor(ocr)
    return extractor

# -----------------------------------------------------------------------------
# 3. SIDEBAR UI
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2921/2921222.png", width=60) # Placeholder Icon
    st.markdown("### SYSTEM CONFIG")
    st.markdown("---")
    
    # Styled Toggle
    gpu_option = st.checkbox("⚡ Enable GPU Acceleration", value=False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status Indicator
    try:
        extractor = get_extractor()
        st.markdown("""
            <div style='background: rgba(16, 185, 129, 0.1); border: 1px solid #059669; padding: 12px; border-radius: 8px;'>
                <span style='color: #34d399; font-weight: bold;'>● SYSTEM ONLINE</span><br>
                <span style='color: #a7f3d0; font-size: 0.8rem;'>OCR Engine Ready</span>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading OCR: {e}")

    st.markdown("<br><br><br><br><div style='color: #555; font-size: 0.8rem;'>v1.0.4 | Build 2023</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. MAIN LAYOUT
# -----------------------------------------------------------------------------

# Header
st.markdown("<h1>Waybill Identity Extraction</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #c4b5fd; margin-top: -10px; margin-bottom: 30px;'>Automated Optical Character Recognition System // Pattern: <code>_1_</code></p>", unsafe_allow_html=True)

# File Upload Section
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Waybill Image (JPG, PNG)", type=['jpg', 'png', 'jpeg'])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    # Load and Display Image
    image_np = load_image(uploaded_file)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    # --- LEFT COLUMN: VISUAL ---
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 👁️ Source Feed")
        st.image(image_np, channels="BGR", use_container_width=True)
        st.markdown("<div style='text-align: center; color: #666; font-size: 0.8rem; margin-top: 10px;'>Resolution: Original</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: DATA ---
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🧠 Analysis Control")
        
        st.write("") # Spacer
        
        # Process Button
        if st.button("EXECUTE EXTRACTION"):
            with st.spinner("🔄 DECODING PIXELS..."):
                # Preprocessing
                gray_img = preprocess_image(image_np)
                
                # Extraction Logic
                extracted_text, confidence, orientation = extractor.process_image(gray_img)
            
            st.markdown("---")
            
            # RESULTS
            if extracted_text != "Pattern Not Found":
                st.markdown(f"""
                    <div style='background: rgba(124, 58, 237, 0.1); border: 1px solid #7c3aed; padding: 20px; border-radius: 12px; margin-top: 10px;'>
                        <div style='color: #a78bfa; font-size: 0.9rem; margin-bottom: 5px;'>TARGET IDENTIFIER FOUND</div>
                        <div style='color: #fff; font-size: 2.2rem; font-family: "Rajdhani"; font-weight: 700; text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);'>
                            {extracted_text}
                        </div>
                    </div>
                    
                    <div class='hud-container'>
                        <div class='hud-box'>
                            <div class='hud-label'>Confidence Score</div>
                            <div class='hud-value' style='color: #34d399;'>{confidence:.2f}%</div>
                        </div>
                        <div class='hud-box'>
                            <div class='hud-label'>Scan Orientation</div>
                            <div class='hud-value' style='color: #60a5fa;'>{orientation}°</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                    <div style='background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; padding: 20px; border-radius: 12px; margin-top: 10px;'>
                        <div style='color: #fca5a5; font-size: 0.9rem; margin-bottom: 5px;'>STATUS</div>
                        <div style='color: #fecaca; font-size: 1.5rem; font-family: "Rajdhani"; font-weight: 700;'>
                            ⚠️ PATTERN NOT ISOLATED
                        </div>
                        <div style='margin-top: 10px; color: #f87171; font-size: 0.9rem;'>
                            Target <code>_1_</code> unreadable. Check lighting and glare.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            # Placeholder State
            st.markdown("""
                <div style='text-align: center; padding: 40px; color: #444; border: 1px dashed #333; border-radius: 8px; margin-top: 20px;'>
                    Awaiting User Command
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. FOOTER
# -----------------------------------------------------------------------------
st.markdown("<div class='footer'>Designed for AI/ML Assessment • Solution by Ishita Patoliya</div>", unsafe_allow_html=True)