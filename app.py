import streamlit as st
from utils import *

st.title("📄 ATS Resume Analyzer")

file = st.file_uploader("Upload Resume (PDF)")
jd = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if file and jd:

        file.seek(0)
        resume_text = extract_text(file)

        if not resume_text.strip():
            st.error("⚠️ Could not read resume properly.")
            st.stop()

        with st.spinner("Extracting keywords..."):
            keywords = keyword(jd)

        score, matched, missing = analyze(resume_text, keywords)

        st.markdown("### 🎯 ATS Score")
        st.metric(label="Score", value=f"{score}/100")
        st.progress(score)

        if score > 80:
            st.success("Excellent match 🚀")
        elif score > 50:
            st.warning("Decent but can improve ⚡")
        else:
            st.error("Needs improvement ❌")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Keywords")
            for m in matched:
                st.write(f"- {m}")

        with col2:
            st.subheader("❌ Missing Keywords")
            for m in missing:
                st.write(f"- {m}")

        # 🤖 AI Suggestions (OLLAMA USED HERE)
        with st.expander("🤖 AI Suggestions"):
            if st.button("Get Suggestions"):
                with st.spinner("Thinking..."):
                    missing_text = ", ".join(missing)

                    suggestions = query(f"""
You are an ATS assistant.

Missing skills:
{missing_text}

Give 3-5 short suggestions to improve the resume.
""")

                st.write(suggestions)

        # ✨ Improve Resume (OLLAMA)
        with st.expander("✨ Improve Resume"):
            if st.button("Improve Resume"):
                with st.spinner("Improving..."):
                    improved = query(f"""
Rewrite this resume professionally.

- Use strong action verbs
- Make it ATS friendly
- Keep it concise

Resume:
{resume_text}
""")

                st.write(improved)

    else:
        st.warning("Please upload resume and job description")