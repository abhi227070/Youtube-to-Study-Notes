import streamlit as st
from youtube_subtitle_generator import extract_video_id, get_available_languages, get_subtitles
from llm_response import llm_generator
from fpdf import FPDF
import time

st.sidebar.title("🔑 API Key Setup")

# Instructional text with a clickable link
st.sidebar.markdown(
    """
    👉 **Don't have an API Key?**  
    Get one from [NVIDIA AI Endpoints](https://www.nvidia.com/en-in/ai-data-science/foundation-models/)  
    *(Sign in required)*
    """,
    unsafe_allow_html=True
)

# Input field for API key
nvidia_api_key = st.sidebar.text_input("Enter your NVIDIA API Key:", type="password")

if not nvidia_api_key:
    st.sidebar.warning("Please enter your NVIDIA API Key to proceed.")

# Model description (LLAMA model)
st.sidebar.markdown(
    """
    ### 🔍 **About the Model**
    We are using the **Meta LLaMA 3.1-405B** model, a **state-of-the-art large language model** developed by Meta.  
    LLaMA (Large Language Model Meta AI) is designed to understand and generate human-like text based on context.
    
    - **Purpose**: Can be used for a wide range of NLP tasks, including summarization, translation, and content generation.
    - **Size**: 405 Billion parameters.
    - **Capabilities**: Multilingual, supports multiple languages including English, Hindi, and Hinglish.
    
    For more information on LLaMA, visit [Meta's LLaMA page](https://www.llama.com/)  
    """,
    unsafe_allow_html=True
)


if not nvidia_api_key:
    st.sidebar.warning("Please enter your NVIDIA API Key to proceed.")
else:
    # Main UI
    st.title("📺 YouTube to Study Notes")

    # YouTube Video URL Input
    video_url = st.text_input("🎥 Enter YouTube Video URL:")

    if video_url:
        video_id = extract_video_id(video_url)

        if video_id:
            available_languages = get_available_languages(video_id)

            if available_languages:
                selected_lang = st.selectbox("🌍 Select Subtitle Language:", available_languages.keys())

                if st.button("📥 Generate"):
                    with st.spinner("Fetching subtitles... Please wait ⏳"):
                        time.sleep(2)  # Simulating delay
                        subtitles = get_subtitles(video_id, available_languages[selected_lang])
                        study_notes = llm_generator(subtitles=subtitles, api_key=nvidia_api_key)

                        # Store in session state to persist after rerun
                        st.session_state.subtitles = subtitles
                        st.session_state.study_notes = study_notes

                    st.success("✅ Subtitles and study notes generated successfully!")

            else:
                st.error("❌ No subtitles available for this video.")
        else:
            st.error("❌ Invalid YouTube URL! Please enter a valid link.")

    # If subtitles are fetched, display UI elements
    if "subtitles" in st.session_state:
        with st.expander("📜 View Subtitles (Click to Expand)"):
            st.text_area("Subtitles:", st.session_state.subtitles, height=300)

            # Download Subtitles as TXT
            st.download_button(
                label="⬇️ Download Subtitles (.txt)",
                data=st.session_state.subtitles,
                file_name="subtitles.txt",
                mime="text/plain"
            )

        # Study Notes Section
        st.markdown("## 📝 Study Notes")
        st.write(st.session_state.study_notes)

        # File Format Selection for Study Notes
                # File Format Selection for Study Notes
        file_format = st.radio("Choose Download Format:", ["Text (.txt)", "PDF (.pdf)"])

        if file_format == "Text (.txt)":
            file_data = st.session_state.study_notes
            file_name = "study_notes.txt"
            mime_type = "text/plain"

        elif file_format == "PDF (.pdf)":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, st.session_state.study_notes)

            # Save PDF to a bytes object
            pdf_bytes = pdf.output(dest="S").encode("latin1")  # Convert PDF to bytes
            file_data = pdf_bytes
            file_name = "study_notes.pdf"
            mime_type = "application/pdf"

        # Download Button for Study Notes
        st.download_button(
            label=f"⬇️ Download Study Notes ({file_format.split()[1]})",
            data=file_data,
            file_name=file_name,
            mime=mime_type
        )

