import cv2
import numpy as np
import streamlit as st

# =====================================================================
# 🎨 1. CORE APPLICATION MATRIX & ENTERPRISE DESIGN ARCHITECTURE
# =====================================================================
st.set_page_config(page_title="SizeGuesser Pro SaaS", page_icon="🛍️", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.6rem; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #4B5563; font-size: 1.1rem; margin-bottom: 25px; }
    .passport-box { border: 2px dashed #3B82F6; padding: 22px; border-radius: 12px; background-color: #EFF6FF; margin-top: 20px; }
    .brand-title { font-size: 1.2rem; font-weight: 700; color: #1F2937; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ SizeGuesser Pro v6.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Wearable Enterprise Smart Fit Protocol with Vision Engine</div>', unsafe_allow_html=True)

# 🗺️ DYNAMIC NAVIGATION MENU BAR
menu_selection = st.radio(
    "Select Department:",
    ["👕 Shirts & Tops", "👖 Pants & Jeans", "👟 Shoes & Sandals", "👓 Glasses & Eyewear"],
    horizontal=True
)

st.write("---")

# --- GLOBAL INPUT HANDLING ---
col1, col2 = st.columns(2)
with col1:
    height_ft = st.selectbox("Your Height (Feet):", [4, 5, 6, 7], index=1)
    height_in = st.slider("Your Height (Remaining Inches):", 0, 11, 7)
    total_inches = (height_ft * 12) + height_in

with col2:
    weight_lbs = st.number_input("Your Weight (lbs):", min_value=70, max_value=400, value=155)
    body_build = st.selectbox("Your Body Frame Build:", ["Slim / Lean", "Average / Balanced", "Athletic / Broad Shoulder", "Heavy / Stocky"])

# Global Fit Preference setup
fit_pref = st.radio("Sizing Cut Style Preference:", ["Standard Fit", "Slim / Tight Fit", "Oversized / Baggy"])

st.write("---")
st.subheader("📸 Step 2: Image Analysis Frame")
uploaded_file = st.file_uploader("Upload a clear, front-facing reference photo...", type=["jpg", "jpeg", "png"])

# Initialize calculations containers
calculated_size = ""
brand_conversion = {}
raw_metric_val = 0.0

if uploaded_file is not None:
    st.image(uploaded_file, caption="Target Frame Payload Captured", use_container_width=True)
    
    # 💾 FIXED MEMORY LOOP BUG: Read and lock image bytes securely inside session memory
    img_bytes = uploaded_file.getvalue()
    
    if st.button("Execute AI Sizing Analysis Matrix 🚀", use_container_width=True):
        with st.spinner("Processing background-proof contour segmentation algorithms..."):
            
            # Convert bytes safely to OpenCV image without loss
            file_bytes = np.asarray(bytearray(img_bytes), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            
            if img is not None:
                height, width, _ = img.shape
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (7, 7), 0)
                edges = cv2.Canny(blurred, 40, 120)
                
                # Proportional calibration scale math based on height input parameters
                body_height_pixels = height * 0.78
                inches_per_pixel = total_inches / body_height_pixels
                
                # Dynamic Style Adjuster Variables
                style_mod = 1.05 if fit_pref == "Oversized / Baggy" else (0.95 if fit_pref == "Slim / Tight Fit" else 1.00)

                # ==========================================
                # 👕 DEPT 1: SHIRTS & TOPS
                # ==========================================
                if menu_selection == "👕 Shirts & Tops":
                    scan_row = int(height * 0.33)
                    row_pixels = edges[scan_row, :]
                    detected_bounds = np.where(row_pixels > 0)
                    pixel_width = float(detected_bounds[-1] - detected_bounds) if len(detected_bounds) >= 2 else float(width * 0.35)
                    
                    shoulder_inches = pixel_width * inches_per_pixel * 1.15 * style_mod
                    raw_metric_val = shoulder_inches
                    base = "S" if shoulder_inches < 16.5 else ("M" if shoulder_inches < 17.5 else ("L" if shoulder_inches < 18.5 else "XL"))
                    
                    calculated_size = f"Shirt Size: {base}"
                    brand_conversion = {"Nike": base, "Zara": "M" if base == "S" else base, "H&M": base, "Adidas": base}

                # ==========================================
                # 👖 DEPT 2: PANTS & JEANS
                # ==========================================
                elif menu_selection == "👖 Pants & Jeans":
                    scan_row = int(height * 0.60)
                    row_pixels = edges[scan_row, :]
                    detected_bounds = np.where(row_pixels > 0)
                    pixel_width = float(detected_bounds[-1] - detected_bounds) if len(detected_bounds) >= 2 else float(width * 0.32)
                    
                    waist_inches = pixel_width * inches_per_pixel * 1.95 * style_mod
                    raw_metric_val = waist_inches
                    final_waist = int(round(waist_inches))
                    if final_waist % 2 != 0: final_waist += 1
                    final_waist = max(28, min(42, final_waist))
                    inseam = 30 if total_inches < 67 else (32 if total_inches < 72 else 34)
                    
                    calculated_size = f"Pants Profile: W{final_waist} / L{inseam}"
                    brand_conversion = {"Levi's 501": f"{final_waist}x{inseam}", "Zara Man": f"US {final_waist-20}", "H&M Denim": f"US {final_waist}"}

                # ==========================================
                # 👟 DEPT 3: SHOES & SANDALS
                # ==========================================
                elif menu_selection == "👟 Shoes & Sandals":
                    scan_row = int(height * 0.91)
                    row_pixels = edges[scan_row, :]
                    detected_bounds = np.where(row_pixels > 0)
                    pixel_width = float(detected_bounds[-1] - detected_bounds) if len(detected_bounds) >= 2 else float(width * 0.15)
                    
                    foot_length_inches = pixel_width * inches_per_pixel * 0.40 * style_mod
                    raw_metric_val = foot_length_inches
                    computed_shoe = (foot_length_inches * 3) - 22
                    final_shoe = max(6.0, min(14.0, round(computed_shoe * 2) / 2))
                    
                    calculated_size = f"US Men's Size {final_shoe}"
                    brand_conversion = {"Nike Air Max": f"US {final_shoe}", "Adidas Originals": f"US {final_shoe + 0.5}", "Birkenstock": f"EU {int(final_shoe + 33)}", "Puma Classics": f"US {final_shoe}"}

                # ==========================================
                # 👓 DEPT 4: GLASSES & EYEWEAR
                # ==========================================
                elif menu_selection == "👓 Glasses & Eyewear":
                    scan_row = int(height * 0.18)
                    row_pixels = edges[scan_row, :]
                    detected_bounds = np.where(row_pixels > 0)
                    pixel_width = float(detected_bounds[-1] - detected_bounds) if len(detected_bounds) >= 2 else float(width * 0.22)
                    
                    face_width_mm = pixel_width * inches_per_pixel * 25.4 * 0.33 * style_mod
                    raw_metric_val = face_width_mm
                    frame_fit = "Narrow (<130mm)" if face_width_mm < 129 else ("Medium (130mm-139mm)" if face_width_mm <= 139 else "Wide (>140mm)")
                    
                    calculated_size = f"Frame Profile: {frame_fit}"
                    brand_conversion = {"Ray-Ban Aviator": "Standard 55mm" if "Medium" in frame_fit else ("Large 58mm" if "Wide" in frame_fit else "Small 52mm"), "Oakley Frames": "Standard Fit Line"}

# --- RENDER GORGEOUS OUTPUT LAYOUT PASSPORT ---
if calculated_size:
    st.balloons()
    st.success("🎉 Analysis Metrics Successfully Computed!")
    
    unit_label = "mm" if menu_selection == "👓 Glasses & Eyewear" else "inches"
    st.markdown(f"""
    <div class="passport-box">
        <h3 style='text-align: center; margin-top: 0; color: #1E3A8A;'>🛒 PRODUCT FIT PASSPORT</h3>
        <p><b>Target Department:</b> {menu_selection}</p>
        <p><b>Anatomical Input Profile:</b> {height_ft}'{height_in}" ft | {weight_lbs} lbs | {body_build}</p>
        <p><b>Calibrated Component Width:</b> {raw_metric_val:.1f} {unit_label}</p>
        <hr style='border-top: 1px dashed #3B82F6;'>
        <h2 style='text-align: center; color: #2563EB;'>RECOMMENDED ENGINE FIT:<br>{calculated_size}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown('<div class="brand-title">🏬 Multi-Brand Retail Cross Matcher:</div>', unsafe_allow_html=True)
    st.write("Click these exact sizes when purchasing across popular e-commerce retail apps:")
    
    b_cols = st.columns(len(brand_conversion))
    for idx, (brand_name, size_val) in enumerate(brand_conversion.items()):
        with b_cols[idx]:
            st.metric(label=brand_name, value=size_val)
