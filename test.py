import cv2
import numpy as np
import streamlit as st

def calculate_dimensions(image_bytes, target_category, user_height_inches=70):
    # Convert uploaded web file bytes into an OpenCV image format
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    if img is None:
        return None, "Error: Invalid image file format."
        
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 130)
    
    # 🎯 Category-Specific Scanning Matrix
    if target_category == "Shirts & Tops":
        scan_row = int(height * 0.32) # Scan upper torso
        row_pixels = edges[scan_row, :]
        edge_positions = np.where(row_pixels > 0)[0]
        if len(edge_positions) >= 2:
            pixel_width = edge_positions[-1] - edge_positions[0]
            body_height_pixels = height * 0.78 
            inches_per_pixel = user_height_inches / body_height_pixels
            real_size = pixel_width * inches_per_pixel * 1.25 # Tailoring curve adjustment
            
            # Sizing Algorithm
            if real_size < 16.5: size_label = "Small (S)"
            elif real_size < 17.5: size_label = "Medium (M)"
            elif real_size < 18.5: size_label = "Large (L)"
            else: size_label = "Extra Large (XL)"
            return real_size, f"Shirt Size: {size_label}"
            
    elif target_category == "Pants & Jeans":
        scan_row = int(height * 0.60) # Scan lower hips/waist zone
        row_pixels = edges[scan_row, :]
        edge_positions = np.where(row_pixels > 0)[0]
        if len(edge_positions) >= 2:
            pixel_width = edge_positions[-1] - edge_positions[0]
            body_height_pixels = height * 0.78
            inches_per_pixel = user_height_inches / body_height_pixels
            waist_inches = pixel_width * inches_per_pixel * 2.1 # Circumference translation factor
            
            # Waist Measurement sizing rounds to nearest integer
            waist_size = int(round(waist_inches))
            if waist_size % 2 != 0: waist_size += 1 # Align to retail standard even numbers
            return waist_inches, f"Pants Waist Size: {waist_size} inches"

    elif target_category == "Shoes & Sandals":
        # Shoes require an object framing logic (scanning the lowest 10% bounding region)
        foot_zone = edges[int(height * 0.85):, :]
        edge_positions = np.where(foot_zone > 0)[1]
        if len(edge_positions) >= 2:
            pixel_length = edge_positions[-1] - edge_positions[0]
            # Reference ratio: a foot is roughly 15% of total body height 
            foot_length_inches = (pixel_length / width) * (user_height_inches * 0.15)
            
            # Brannock scale translation algorithm (US Mens standard conversion)
            us_shoe_size = (foot_length_inches * 3) - 22
            final_size = max(6, min(13, round(us_shoe_size * 2) / 2)) # Boundary caps 6 to 13, half-sizes included
            return foot_length_inches, f"US Shoe Size: {final_size}"

    elif target_category == "Glasses & Eyewear":
        scan_row = int(height * 0.18) # Target temple-to-temple eye level row
        row_pixels = edges[scan_row, :]
        edge_positions = np.where(row_pixels > 0)[0]
        if len(edge_positions) >= 2:
            pixel_width = edge_positions[-1] - edge_positions[0]
            # Face width conversion math in millimeters
            mm_per_pixel = (user_height_inches * 25.4) / height
            face_width_mm = pixel_width * mm_per_pixel * 0.85
            
            if face_width_mm < 129: frame_fit = "Narrow Frame (<130mm)"
            elif face_width_mm <= 139: frame_fit = "Medium Frame (130mm - 139mm)"
            else: frame_fit = "Wide Frame (>140mm)"
            return face_width_mm, f"Optimal Fit: {frame_fit}"

    return None, "Boundary tracking failed. Stand straight facing the lens clearly."

# --- INTERACTIVE DASHBOARD DESIGN ---
st.set_page_config(page_title="SizeGuesser Pro SaaS", page_icon="🛍️", layout="centered")
st.title("🛍️ SizeGuesser Pro: Universal Fit Engine")
st.write("An enterprise multi-category tool to scan bodies and calculate retail sizes to eliminate product returns.")

# Sidebar Configuration Controls
st.sidebar.header("⚙️ Calibration Controls")
category = st.sidebar.selectbox("Select Wearable Product Type:", ["Shirts & Tops", "Pants & Jeans", "Shoes & Sandals", "Glasses & Eyewear"])
user_height = st.sidebar.slider("Your Physical Height (inches):", 45, 85, 70)
fit_pref = st.sidebar.radio("Sizing Fit Preference:", ["Standard Fit", "Slim / Tight Fit", "Oversized / Loose Fit"])

uploaded_file = st.file_uploader("Upload crisp, front-facing reference photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Analyzing item boundaries...', use_container_width=True)
    
    with st.spinner("Executing mathematical sizing matrices..."):
        img_bytes = uploaded_file.read()
        raw_val, output_text = calculate_dimensions(img_bytes, category, user_height)
        
        if raw_val:
            st.success("🎯 Analysis Matrices Successfully Completed!")
            
            # Display responsive metric metric
            metric_label = "Calculated Metric Value"
            metric_unit = "mm" if category == "Glasses & Eyewear" else "inches"
            st.metric(label=f"{category} Raw Estimator", value=f"{raw_val:.1f} {metric_unit}")
            
            # Output final sizing string
            st.info(f"💡 **SaaS Size Recommendation:** {output_text} ({fit_pref})")
        else:
            st.error(output_text)
