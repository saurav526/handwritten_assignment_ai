import os

import streamlit as st
from PIL import Image

from pipeline.preprocessing import preprocess_image
from pipeline.ocr import extract_text
from pipeline.generator import generate_assignment

from utils.docx_generator import create_docx


# --------------------------------------------------
# Streamlit configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Handwritten Assignment AI",
    page_icon="📝",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title(
    "📝 Handwritten Assignment AI"
)

st.write(
    "Upload handwritten assignment pages, "
    "extract the content using OCR, "
    "generate a clean assignment with AI, "
    "and download it as DOCX."
)


# --------------------------------------------------
# Upload
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload handwritten assignment pages",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp"
    ],
    accept_multiple_files=True
)


# --------------------------------------------------
# Uploaded files
# --------------------------------------------------

if uploaded_files:

    st.subheader(
        "Uploaded Pages"
    )

    columns = st.columns(3)

    for index, uploaded_file in enumerate(
        uploaded_files
    ):

        image = Image.open(
            uploaded_file
        ).convert("RGB")

        with columns[
            index % 3
        ]:

            st.image(
                image,
                caption=f"Page {index + 1}",
                use_container_width=True
            )


    # --------------------------------------------------
    # Analyze button
    # --------------------------------------------------

    if st.button(
        "🔍 Analyze Assignment",
        type="primary"
    ):

        os.makedirs(
            "data/uploads",
            exist_ok=True
        )

        all_text = []

        progress = st.progress(
            0
        )

        status = st.empty()


        # Process every page
        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            status.write(
                f"Processing page {index + 1}..."
            )

            image = Image.open(
                uploaded_file
            ).convert("RGB")


            # Preprocessing
            processed_image = (
                preprocess_image(
                    image
                )
            )


            # Save processed image
            image_path = (
                f"data/uploads/"
                f"page_{index + 1}.png"
            )

            processed_image.save(
                image_path
            )


            # OCR
            try:

                text = extract_text(
                    image_path
                )

            except Exception as error:

                text = (
                    f"[OCR failed on page "
                    f"{index + 1}: {error}]"
                )


            all_text.append(
                f"--- PAGE {index + 1} ---\n"
                f"{text}"
            )


            progress.progress(
                (index + 1)
                / len(uploaded_files)
            )


        # Combine all pages
        extracted_text = "\n\n".join(
            all_text
        )


        st.session_state[
            "extracted_text"
        ] = extracted_text


        status.success(
            "All pages processed."
        )


# --------------------------------------------------
# OCR result
# --------------------------------------------------

if "extracted_text" in st.session_state:

    st.divider()

    st.subheader(
        "📖 Extracted Handwritten Text"
    )

    edited_text = st.text_area(

        "Review and correct OCR mistakes "
        "before generating the assignment.",

        value=st.session_state[
            "extracted_text"
        ],

        height=400
    )


    st.session_state[
        "extracted_text"
    ] = edited_text


    # --------------------------------------------------
    # Generate assignment
    # --------------------------------------------------

    if st.button(
        "✍️ Generate Complete Assignment",
        type="primary"
    ):

        with st.spinner(
            "AI is analyzing the assignment..."
        ):

            try:

                result = generate_assignment(
                    st.session_state[
                        "extracted_text"
                    ]
                )

                st.session_state[
                    "result"
                ] = result

                st.success(
                    "Assignment generated successfully."
                )

            except Exception as error:

                st.error(
                    f"Generation failed: {error}"
                )


# --------------------------------------------------
# Generated assignment
# --------------------------------------------------

if "result" in st.session_state:

    st.divider()

    st.subheader(
        "✨ Generated Assignment"
    )


    final_assignment = st.text_area(

        "You can edit the generated assignment.",

        value=st.session_state[
            "result"
        ],

        height=600
    )


    st.session_state[
        "result"
    ] = final_assignment


    # --------------------------------------------------
    # Generate DOCX
    # --------------------------------------------------

    os.makedirs(
        "output",
        exist_ok=True
    )


    docx_path = (
        "output/"
        "generated_assignment.docx"
    )


    create_docx(

        title="Generated Assignment",

        content=final_assignment,

        output_path=docx_path
    )


    # --------------------------------------------------
    # Download
    # --------------------------------------------------

    with open(
        docx_path,
        "rb"
    ) as file:

        st.download_button(

            label="📥 Download Assignment DOCX",

            data=file,

            file_name="generated_assignment.docx",

            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            )
        )