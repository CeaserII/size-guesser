import cv2
import numpy as np
import streamlit as st

def estimate_shirt_size(image_bytes):
    # Convert uploaded web file bytes into an OpenCV image format
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    if img is None:
        return None, "Error: Invalid image format."
        
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    upper_body_row = int(height * 0.3)
    row_pixels = edges[upper_body_row, :]
    edge_positions = np.where(row_pixels > 0)[0]
    
    if len(edge_positions) >= 2:
        left_edge = edge_positions[0]
        right_edge = edge_positions[-1]
        pixel_width = right_edge - left_edge
        
        estimated_inches = (pixel_width / width) * 38.0
        
        if estimated_inches < 16.5:
            size = "Small (S)"
        elif estimated_inches < 17.5:
            size = "Medium (M)"
        elif estimated_inches < 18.5:
            size = "Large (L)"
        else:
            size = "Extra Large (XL)"
            
        return estimated_inches, size
    else:
        return None, "Could not isolate body frame edges cleanly. Ensure a clear background."

# --- STREAMLIT WEB INTERFACE ---
st.set_page_config(page_title="AI Size Guesser", page_icon="👕")
st.title("👕 AI Body Size Guesser & Fit Matcher")
st.write("Upload a front-facing full body photo to find your perfect clothing size instantly!")

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded picture on the website
    st.image(uploaded_file, caption='Uploaded Photo', use_container_width=True)
    st.write("Analyzing dimensions...")
    
    # Read the file data bytes
    img_bytes = uploaded_file.read()
    width_inches, recommended_size = estimate_shirt_size(img_bytes)
    
    if width_inches:
        st.success("🎯 Analysis Complete!")
        st.metric(label="Calculated Shoulder Width", value=f"{width_inches:.1f} inches")
        st.subheader(f"Your Recommended Shirt Size: **{recommended_size}**")
    else:
        st.error(recommended_size)
