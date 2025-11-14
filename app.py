#라이브러리 로드
import cv2
import numpy as np
import streamlit as st

from functions import scan_document

st.set_page_config(page_title="📸➡️📄 Mini Scanner", layout="wide")

def main():
    st.title("📸➡️📄 Mini Scanner")
    st.write("Automatically scan documents captured with your camera")

    # 사이드바
    st.sidebar.header("⚙️Settings Options")

    mode = st.sidebar.selectbox(
        "Select Scan Mode",
        ("onix", "color", "gray", "bw"),
        index=0,
        help = "Choose the desired scan mode for your document.")
    
    auto_crop = st.sidebar.checkbox(
        "Auto Crop Document",
        value=True,
        help="Automatically detect and crop the document from the image."
    )

    remove_notes = st.sidebar.checkbox(
        "Remove Colored Notes",
        value=False,
        help="Remove colored writings such as highlighter marks from the document."
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Upload an image of a document to scan it using the selected settings.")

    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is None:
        st.info("Upload any image file")
        st.stop()
    
    
    # 파일을 OpenCV BGR 이미지로 읽기
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()), dtype=np.uint8)
    
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image_bgr is None:
        st.error("Error: Unable to read the image file.")
        st.stop()
    
    # 원본 이미지는 RGB로 변환하여 표시
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    st.subheader("1️⃣Original Image")
    st.image(image_rgb, caption = 'original', use_column_width=True)

    
    # 스캔 실행
    with st.spinner("🧠Scanning document..."):
        result, warped_doc, mask = scan_document(
            image = image_bgr,
            mode = mode,
            auto_crop = auto_crop,
            remove_colored_notes = remove_notes,
        )

    # warped_doc RGB로 변환하여 표시
    warped_doc = cv2.cvtColor(warped_doc, cv2.COLOR_BGR2RGB)

    if result.ndim == 2:
        result_display = result
    
    else:
        result_display = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    st.subheader("2️⃣Scanned Result")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📐Warped Document:**")
        st.image(warped_doc, 
                 caption="Warped Document", 
                 use_column_width=True)
        
    with col2:
        st.markdown("**✨Scanned Fianl Result(mode:{mode}**")
        st.image(result_display, 
                 caption="Final Scan", 
                 use_column_width=True,
                 clamp=True)
        
    
    # 필기 마스크가 있으면 확인용으로 보여주기
    if remove_notes and mask is not None:
        st.subheader("3️⃣Removed Colored Notes Mask")
        st.image(mask, 
                 caption="Removed Colored Notes Mask", 
                 use_column_width=True,
                 clamp=True)
        

    st.markdown("---")
    st.subheader("📥 Download")

    if result.ndim == 2:
        success, buffer = cv2.imencode(".png", result)

    else:
        success, buffer = cv2.imencode(".png", result)

    if not success:
        st.error("Error: Unable to encode the image for download.")
        return
    

    st.download_button(
        label="💾 Download Scanned Image",
        data=buffer.tobytes(),
        file_name="scanned_document.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()