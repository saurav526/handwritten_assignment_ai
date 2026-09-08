import os
import streamlit as st
from PIL import Image
from pipeline.preprocessing import preprocess_image
from pipeline.ocr import extract_text
from pipeline.generator import generate_assignment
from utils.docx_generator import create_docx

st.set_page_config(page_title="Handwritten Assignment AI", page_icon="📝", layout="wide")

st.title("📝 Handwritten Assignment AI")
st.caption("Upload handwritten pages → OCR → AI analysis → complete assignment → DOCX")

files = st.file_uploader(
    "Upload handwritten assignment pages",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True
)

if files:
    st.subheader("Uploaded Pages")
    cols = st.columns(3)

    for i, uploaded in enumerate(files):
        image = Image.open(uploaded).convert("RGB")
        with cols[i % 3]:
            st.image(image, caption=f"Page {i + 1}", use_container_width=True)

    if st.button("🔍 Analyze Assignment", type="primary"):
        os.makedirs("data/uploads", exist_ok=True)

        all_text = []
        progress = st.progress(0)

        for i, uploaded in enumerate(files):
            image = Image.open(uploaded).convert("RGB")
            processed = preprocess_image(image)

            path = f"data/uploads/page_{i + 1}.png"
            processed.save(path)

            try:
                text = extract_text(path)
            except Exception as e:
                text = f"[OCR failed on page {i + 1}: {e}]"

            all_text.append(f"--- PAGE {i + 1} ---\n{text}")
            progress.progress((i + 1) / len(files))

        extracted = "\n\n".join(all_text)
        st.session_state["extracted_text"] = extracted

    if "extracted_text" in st.session_state:
        st.subheader("📖 Extracted Text")
        edited_text = st.text_area(
            "You can correct OCR mistakes before generation.",
            st.session_state["extracted_text"],
            height=350
        )
        st.session_state["extracted_text"] = edited_text

        if st.button("✍️ Generate Complete Assignment"):
            with st.spinner("Analyzing and generating..."):
                try:
                    result = generate_assignment(st.session_state["extracted_text"])
                    st.session_state["result"] = result
                except Exception as e:
                    st.error(f"Generation failed: {e}")

    if "result" in st.session_state:
        st.subheader("✨ Generated Assignment")
        result = st.text_area(
            "Edit the final assignment if needed.",
            st.session_state["result"],
            height=500
        )
        st.session_state["result"] = result

        os.makedirs("output", exist_ok=True)
        docx_path = "output/generated_assignment.docx"

        create_docx(
            title="Generated Assignment",
            content=result,
            output_path=docx_path
        )

        with open(docx_path, "rb") as f:
            st.download_button(
                "📥 Download DOCX",
                data=f,
                file_name="generated_assignment.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
else:
    st.info("Upload one or more handwritten pages to begin.")
