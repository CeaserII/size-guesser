import streamlit as st
import numpy as np

# =====================================================================
# 🎨 1. CORE APPLICATION MATRIX & ENTERPRISE DESIGN ARCHITECTURE
# =====================================================================
st.set_page_config(page_title="SizeGuesser Pro Enterprise Suite", page_icon="🌐", layout="wide")

# Initialize Local Database Session State variables for returning users
if "saved_profiles" not in st.session_state:
    st.session_state.saved_profiles = {}

# Inject Custom High-End Corporate Dashboard UI Stylesheet
st.markdown("""
    <style>
    .main-header { font-size: 2.8rem; font-weight: 800; color: #1E3A8A; letter-spacing: -0.5px; margin-bottom: 2px; }
    .sub-title { color: #4B5563; font-size: 1.15rem; margin-bottom: 30px; font-weight: 400; }
    
    /* Luxury Passport Metric UI Containers */
    .passport-card { 
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
        color: white; padding: 25px; border-radius: 14px; 
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3); margin: 20px 0;
    }
    .passport-title { font-size: 1.1rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.9; }
    .passport-value { font-size: 2.3rem; font-weight: 800; margin: 10px 0 5px 0; line-height: 1.1; }
    .passport-spec { font-size: 0.95rem; opacity: 0.85; font-family: monospace; }
    
    /* Shopify Fake Store Simulator Styling */
    .shopify-product-box { border: 1px solid #E5E7EB; border-radius: 12px; padding: 25px; background-color: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .shopify-btn-widget { background-color: #008060 !important; color: white !important; font-weight: 700 !important; border-radius: 6px !important; }
    .brand-section-header { font-size: 1.3rem; font-weight: 700; color: #111827; margin: 30px 0 15px 0; border-left: 4px solid #2563EB; padding-left: 12px; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 🎛️ 2. TOP LEVEL PORTAL SELECTION (GLOBAL SWITCHBOARD)
# =====================================================================
portal_view = st.sidebar.radio(
    "Select Active Cloud Environment Portal:",
    ["💻 Customer Sizing Terminal", "🔌 Merchant Shopify Integration Center"]
)

st.sidebar.write("---")

# =====================================================================
# 💻 PORTAL 1: CUSTOMER SIZING WORKSPACE TERMINAL
# =====================================================================
if portal_view == "💻 Customer Sizing Terminal":
    st.markdown('<div class="main-header">🌐 SizeGuesser Pro SaaS Terminal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Production Core v7.0 — Multi-Wearable Omnichannel Measurement Matrix</div>', unsafe_allow_html=True)

    st.sidebar.markdown("### 🏢 Active Department")
    selected_department = st.sidebar.radio(
        "Choose Active Fitting Logic Engine:",
        ["👕 Shirts & Tops", "👖 Pants & Jeans", "👟 Shoes & Sandals", "👓 Glasses & Eyewear"]
    )

    st.sidebar.write("---")
    st.sidebar.markdown("### 🧬 Biometric Input Profiles")
    
    # Local Profile Cloud Sync Loader Feature
    if st.session_state.saved_profiles:
        profile_names = ["-- Select a Saved Profile --"] + list(st.session_state.saved_profiles.keys())
        selected_saved = st.sidebar.selectbox("💾 Load Saved Cloud Profile:", profile_names)
        if selected_saved != "-- Select a Saved Profile --":
            prof_data = st.session_state.saved_profiles[selected_saved]
            st.sidebar.success(f"Loaded database values for '{selected_saved}'!")
    
    profile_username = st.sidebar.text_input("Profile User Registration Name:", placeholder="e.g., Alex Carter")
    height_ft = st.sidebar.selectbox("Height (Feet):", [4, 5, 6, 7], index=1)
    height_in = st.sidebar.slider("Height (Remaining Inches):", 0, 11, 7)
    weight_lbs = st.sidebar.number_input("Weight (Pounds):", min_value=70, max_value=400, value=160)
    body_build = st.sidebar.selectbox("Body Frame Build Style:", ["Slim / Lean Profile", "Balanced / Average", "Athletic / Broad Frame", "Heavy / Robust Build"])

    total_inches = (height_ft * 12) + height_in
    density_bmi = (weight_lbs / (total_inches ** 2)) * 703

    recommended_fit = ""
    brand_conversion_data = {}
    cal_metric_log = ""

    # --- DEPARTMENT 1: SHIRTS & TOPS ---
    if selected_department == "👕 Shirts & Tops":
        st.header("Shirts & Tops Engineering Hub")
        input_method = st.tabs(["⚡ Fast Biometric Profile", "📏 Tailor-Fit Chest Calibration"])
        
        with input_method[0]:
            shirt_cut = st.radio("Desired Fit Silhouette Cut:", ["Standard Fit Line", "Contoured Slim Fit", "Oversized Street Draping"])
            if st.button("Compute Optimal Tops Matrix 🚀", use_container_width=True):
                size_code = "S" if density_bmi < 19.5 else ("M" if density_bmi < 24.8 else ("L" if density_bmi < 29.8 else "XL"))
                if shirt_cut == "Oversized Street Draping" and size_code != "XL":
                    size_code = ["S", "M", "L", "XL"][["S", "M", "L", "XL"].index(size_code) + 1]
                recommended_fit = f"Men's Apparel Size {size_code}"
                cal_metric_log = f"Estimated Shoulder Arcs: {15.5 + (0.8 * ['S','M','L','XL'].index(size_code)):.1f} inches"
                brand_conversion_data = {"Nike": size_code, "Zara": "M" if size_code == "S" else size_code, "H&M Standard": size_code, "Adidas Performance": size_code}

        with input_method[1]:
            chest_circumference = st.slider("Manual Chest Circumference (Inches):", 30, 54, 40)
            if st.button("Compute Precise Sizing Profile 🎯", use_container_width=True):
                size_code = "S" if chest_circumference <= 37 else ("M" if chest_circumference <= 40 else ("L" if chest_circumference <= 43 else "XL"))
                recommended_fit = f"Calibrated Tailor Fit: Size {size_code}"
                cal_metric_log = f"Exact Input Perimeter: {chest_circumference}.0 inches"
                brand_conversion_data = {"Nike Apparel": size_code, "Zara Luxury": size_code, "Polo Ralph Lauren": "Classic Fit " + size_code}

    # --- DEPARTMENT 2: PANTS & JEANS ---
    elif selected_department == "👖 Pants & Jeans":
        st.header("Pants & Denim Sizing Hub")
        input_method = st.tabs(["⚡ Fast Biometric Profile", "📏 Denim Inseam Calibration"])
        
        with input_method[0]:
            if st.button("Compute Optimal Denim Matrix 🚀", use_container_width=True):
                computed_waist = int(density_bmi * 1.22) + 4
                if computed_waist % 2 != 0: computed_waist += 1
                final_waist = max(28, min(42, int(computed_waist)))
                estimated_inseam = 30 if total_inches < 67 else (32 if total_inches < 72 else 34)
                recommended_fit = f"Waist {final_waist} / Inseam {estimated_inseam}"
                cal_metric_log = f"Anatomical Hip Boundary Core: {final_waist - 1}.5 inches"
                brand_conversion_data = {"Levi's 501": f"{final_waist}x{estimated_inseam}", "Zara Denim": f"US {final_waist-20}", "H&M Essentials": f"US {final_waist}"}

        with input_method[1]:
            user_inseam_input = st.slider("Measured Inseam Leg Length (Inches):", 26, 36, 32)
            user_waist_input = st.number_input("Your Measured True Waist Line (Inches):", min_value=24, max_value=48, value=32)
            if st.button("Compute Exact Tailor Fit Profile 🎯", use_container_width=True):
                clean_waist = int(user_waist_input)
                if clean_waist % 2 != 0: clean_waist += 1
                recommended_fit = f"Verified Tailor Matrix: W{clean_waist} / L{user_inseam_input}"
                cal_metric_log = f"True Physical Dimensions: {user_waist_input}w x {user_inseam_input}l"
                brand_conversion_data = {"Levi's Premium": f"{clean_waist}x{user_inseam_input}", "Diesel Core": f"Size {clean_waist}"}

    # --- DEPARTMENT 3: SHOES & SANDALS ---
    elif selected_department == "👟 Shoes & Sandals":
        st.header("Footwear & Brannock Sizing Hub")
        input_method = st.tabs(["⚡ Fast Biometric Profile", "📏 Wall-Paper Foot Tracing Calibration"])
        
        with input_method[0]:
            foot_width = st.radio("Foot Width Structure Profile:", ["Standard D Width", "Wide Box Cut (E/EE Profile)"])
            socks_type = st.selectbox("Intended Sock Pairing Profile:", ["No Socks / Ultra Thin (Best for Sandals)", "Standard Casual Crew Socks", "Thick Winter Socks"])
            if st.button("Compute Footwear Sizing Matrix 🚀", use_container_width=True):
                calculated_shoe = 7.0 if total_inches < 64 else (8.5 if total_inches < 67 else (9.5 if total_inches < 69 else (10.5 if total_inches < 71 else (11.5 if total_inches < 73 else 12.5))))
                if foot_width == "Wide Box Cut (E/EE Profile)": calculated_shoe += 0.5
                if socks_type == "Thick Winter Socks": calculated_shoe += 0.5
                if socks_type == "No Socks / Ultra Thin (Best for Sandals)": calculated_shoe -= 0.5
                final_shoe_val = max(6.0, min(14.0, round(calculated_shoe * 2) / 2))
                recommended_fit = f"US Men's Size {final_shoe_val} ({foot_width})"
                cal_metric_log = f"Estimated Foot Length: {9.5 + (0.33 * final_shoe_val):.2f} inches"
                brand_conversion_data = {"Nike Air Max": f"US {final_shoe_val}", "Adidas Originals": f"US {final_shoe_val + 0.5}", "Birkenstock": f"EU {int(final_shoe_val + 33)}"}

        with input_method[1]:
            foot_inches_input = st.slider("Absolute Foot Length Dimension (Inches):", 8.0, 13.0, 10.5, step=0.1)
            if st.button("Execute Certified Brannock Scaling 🎯", use_container_width=True):
                computed_brannock = (foot_inches_input * 3) - 22
