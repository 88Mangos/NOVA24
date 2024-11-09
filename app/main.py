# app/main.py
import streamlit as st
from parser import MSDSParser, UniversityLabMSDSParser
from utils import load_sample_msds, cache_result
from file_handler import MSDSFileHandler
import os
from dotenv import load_dotenv
import traceback


# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="MSDS Parser",
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("🧪 MSDS Parser")
    st.write("Upload your Material Safety Data Sheet for automated parsing and analysis.")
    
    # Initialize session state
    if 'parsed_results' not in st.session_state:
        st.session_state.parsed_results = None
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload MSDS (PDF, TXT, or MD)", 
        type=['pdf', 'txt', 'md']
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner('Processing file...'):
                # Process file
                file_handler = MSDSFileHandler()
                msds_text = file_handler.process_file(uploaded_file)
                print(msds_text)
                
                # Parse MSDS
                parser = MSDSParser(api_key=os.getenv('OPENAI_API_KEY'))
                result = parser.parse_msds(msds_text)
                st.session_state.parsed_results = result
                
                display_results(result)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.error(traceback.format_exc()) 

def display_results(result):
    """Display parsed MSDS information."""
    st.success('✅ File processed successfully!')
    
    # Create three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Chemical Information")
        st.write(f"**Name:** {result['chemical_name']}")
        st.write(f"**CAS Number:** {result['cas_number']}")
    
    with col2:
        st.subheader("⚠️ Hazards")
        for hazard in result['hazard_summary']['primary_hazards']:
            st.warning(hazard)
    
    with col3:
        st.subheader("🛡️ Safety Requirements")
        ppe = result['safety_requirements']['ppe_required']
        for item, requirement in ppe.items():
            st.info(f"**{item.replace('_', ' ').title()}:** {requirement}")
    
    # Emergency procedures in expandable section
    with st.expander("🚨 Emergency Procedures"):
        for procedure_type, steps in result['emergency_procedures']['first_aid'].items():
            st.write(f"**{procedure_type.replace('_', ' ').title()}:**")
            st.write(steps)
    
    # Storage requirements
    with st.expander("📦 Storage Requirements"):
        storage = result['safety_requirements']['storage_requirements']
        st.write(f"**Temperature:** {storage['temperature']}")
        st.write("**Conditions:**")
        for condition in storage['conditions']:
            st.write(f"- {condition}")

if __name__ == "__main__":
    main()