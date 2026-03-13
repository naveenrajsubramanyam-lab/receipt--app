import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import io

st.title("Receipt OCR + Translator + Excel Export")

uploaded_file = st.file_uploader("Upload receipt (image or PDF)", type=["jpg", "png", "pdf"])

if uploaded_file:
    text = ""

    try:
        # Handle PDF receipts
        if uploaded_file.type == "application/pdf":
            pdf_bytes = uploaded_file.getvalue()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                page_text = page.get_text()
                if not page_text.strip():  # fallback to OCR
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    page_text = pytesseract.image_to_string(img)
                text += page_text + "\n"

        # Handle image receipts
        else:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)

        if text.strip():
            st.subheader("Original Text")
            st.text(text)

            try:
                translator = GoogleTranslator(source='auto', target='en')
                translated = translator.translate(text)
                st.subheader("Translated Text")
                st.success(translated)
            except Exception as e:
                st.error(f"Translation failed: {e}")
                translated = ""

            # Save to Excel
            df = pd.DataFrame({"Original": [text], "Translated": [translated]})
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Receipts")

            st.download_button(
                label="Download Excel",
                data=buffer.getvalue(),
                file_name="receipts.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No text could be extracted. Try a clearer image or scanned PDF.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
