import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import fitz
import io
import re
from googletrans import Translator

st.title("Receipt to Excel App")

uploaded_files = st.file_uploader("Upload receipts (images or PDF)", accept_multiple_files=True)

if uploaded_files:
    translator = Translator()
    rows = []
    sno = 1
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith(".pdf"):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text = pytesseract.image_to_string(img, lang="kor")
                # Extract fields (receipt code, date, amount, food item)
        else:
            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img, lang="kor")
            # Extract fields (same as above)

    df = pd.DataFrame(rows)
    st.write(df)

    # Export Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for month_name, group in df.groupby("MonthName"):
            group.to_excel(writer, sheet_name=month_name, index=False)

    st.download_button("Download Excel", data=output.getvalue(), file_name="receipts_by_month.xlsx")
