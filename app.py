import streamlit as st
import subprocess
import sys
import os
import json

def display_all_charts(include_market_maps=True):
    """Unified function to display all charts and maps in one place"""
    try:
        charts_file = 'generated_charts.json'
        maps_file = 'generated_maps.json'
        
        # Check if any chart files exist
        if not (os.path.exists(charts_file) or os.path.exists(maps_file)):
            st.info("📊 Charts will be generated during the analysis process. Check the generated reports for embedded visualizations.")
            return
        
        st.subheader("📈 Interactive Charts & Visualizations")
        
        # Display charts
        if os.path.exists(charts_file):
            try:
                with open(charts_file, 'r', encoding='utf-8') as f:
                    charts_data = json.load(f)
                
                # Display all charts in expandable sections
                for chart_key, chart_info in charts_data.items():
                    with st.expander(f"📈 {chart_info['title']}", expanded=True):
                        st.write(chart_info['description'])
                        
                        # Recreate the Plotly figure from JSON
                        import plotly.io as pio
                        fig = pio.from_json(chart_info['figure_json'])
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show the raw data
                        with st.expander("📊 Chart Data", expanded=False):
                            st.json(chart_info['data'])
            except Exception as e:
                st.warning(f"Error loading charts: {e}")
        
        # Display maps
        if include_market_maps and os.path.exists(maps_file):
            try:
                with open(maps_file, 'r', encoding='utf-8') as f:
                    maps_data = json.load(f)
                
                # Display all maps in expandable sections
                for map_key, map_info in maps_data.items():
                    with st.expander(f"🗺️ {map_info['title']}", expanded=True):
                        st.write(map_info['description'])
                        
                        # Recreate the Plotly figure from JSON
                        import plotly.io as pio
                        fig = pio.from_json(map_info['figure_json'])
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show the raw data
                        with st.expander("📊 Map Data", expanded=False):
                            st.json(map_info['data'])
            except Exception as e:
                st.warning(f"Error loading maps: {e}")
        
        st.success("🎨 All visualizations generated successfully!")
        
    except Exception as e:
        st.warning(f"Charts display encountered an issue: {e}")
        st.info("Check the generated reports for embedded visualizations.")

st.title("🤖 Strategic Market Research AI Crew")
st.write("This AI crew conducts a comprehensive market analysis based on your product and target market details. Please provide as much detail as possible for the best results.")

# Add debug option in sidebar
with st.sidebar:
    debug_mode = st.checkbox("Debug Mode", help="Enable debug mode to see raw markdown content")
    
    # Visualization options
    st.header("📊 Visualization Options")
    enable_charts = st.checkbox("Generate Interactive Charts", value=True, help="Create visual charts and graphs from the analysis")
    include_market_maps = st.checkbox("Include Market Positioning Maps", value=True, help="Generate competitive positioning visualizations")

st.sidebar.header("Configuration")

with st.sidebar:
    st.header("Product Details")
    product_name_input = st.text_input("Product/Service Name", "QuantumLeap AI SaaS Platform")
    product_description_input = st.text_area("Product/Service Description", "An AI-powered platform that automates data analysis and generates business intelligence reports for enterprise clients.")
    
    # New USP Analysis Section
    st.header("USP & Market Positioning")
    usp_input = st.text_area("Your Unique Selling Proposition (USP)", 
                             placeholder="What makes your product/service truly unique? What problem does it solve that others don't?",
                             help="Leave empty if you want us to identify market gaps, or describe your USP if you have one")
    
    usp_confidence = st.selectbox("How confident are you in your USP?", 
                                 ["Very Confident", "Somewhat Confident", "Not Sure", "Want Market Validation"],
                                 help="This helps determine the depth of USP analysis needed")

    st.header("Market Details")
    industry_input = st.text_input("Target Industry", "Technology, SaaS, Business Intelligence")
    geo_input = st.text_input("Target Geography", "North America")
    scale_input = st.selectbox("Company Scale", ["Bootstrapped", "Venture-Backed", "Publicly Traded", "Any"], index=1)
    
    st.header("Analysis Focus")
    competitor_focus = st.text_input("Specific Competitor to Deep-Dive (Optional)", "", 
                                   help="Enter a specific competitor name for detailed analysis. Leave empty for general market analysis.")
    additional_context = st.text_area("Additional Context or Requirements", "",
                                    help="Add any specific context, requirements, or focus areas for the analysis.")


with st.form(key='analysis_form'):
    submit_button = st.form_submit_button(label='🚀 Start Comprehensive Analysis')

if submit_button:
    st.header("📊 Analysis in Progress...")
    # Hide the backend logs by simply showing a spinner and a status message
    with st.spinner("Your AI crew is conducting the market research. This may take several minutes..."):
        crew_main_path = "main.py"

        # Command to run the crew. We pass inputs as environment variables.
        command = [sys.executable, crew_main_path]
        env = os.environ.copy()
        env["PRODUCT_NAME"] = product_name_input
        env["PRODUCT_DESCRIPTION"] = product_description_input
        env["USP"] = usp_input
        env["USP_CONFIDENCE"] = usp_confidence
        env["INDUSTRY"] = industry_input
        env["GEOGRAPHY"] = geo_input
        env["SCALE"] = scale_input
        env["COMPETITOR_FOCUS"] = competitor_focus
        env["ADDITIONAL_CONTEXT"] = additional_context
        env["ENABLE_CHARTS"] = str(enable_charts)
        env["INCLUDE_MARKET_MAPS"] = str(include_market_maps)

        # We run the process but don't stream its stdout to the UI
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=env,
        )

        if process.returncode != 0:
            st.error("An error occurred during the analysis. Details below:")
            st.code(process.stderr, language='bash')
        else:
            st.success("✅ Comprehensive Analysis Complete!")

    st.header("📊 Generated Visualizations")
    
    # Display all charts if they were generated
    if enable_charts:
        display_all_charts(include_market_maps)
    else:
        st.info("📊 Charts are disabled. Enable 'Generate Interactive Charts' in the sidebar to see visualizations.")

    st.header("📄 Final Reports")
    # The final report is now a single, comprehensive document
    report_file = 'final_market_analysis_report.md'
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Clean up the markdown content
        import re
        # Remove any problematic characters that might break markdown rendering
        report_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', report_content)
        
        with st.expander(f"View: {report_file}", expanded=True):
            if debug_mode:
                st.code(report_content, language='markdown')
            else:
                try:
                    # Render the markdown content
                    st.markdown(report_content, unsafe_allow_html=False)
                    
                    # Charts are now displayed in the main visualization section above
                    
                except Exception as e:
                    st.error(f"Error rendering markdown: {e}")
                    st.code(report_content, language='markdown')

        st.download_button(
            label=f"Download {report_file}",
            data=report_content,
            file_name=report_file,
            mime='text/markdown',
        )
        
        # Add refocus functionality
        st.header("🔄 Refocus Analysis")
        st.write("Use the additional context to refocus the existing analysis:")
        
        refocus_context = st.text_area(
            "Refocus Context", 
            value=additional_context,
            help="Enter new context to refocus the analysis. This will create a new report focused on this specific aspect."
        )
        
        if st.button("🎯 Refocus Analysis on New Context"):
            if refocus_context.strip():
                st.info("🔄 Refocusing analysis based on new context...")
                with st.spinner("Refocusing the analysis. This may take several minutes..."):
                    # Run the crew with refocus context
                    refocus_command = [sys.executable, crew_main_path]
                    refocus_env = os.environ.copy()
                    refocus_env["PRODUCT_NAME"] = product_name_input
                    refocus_env["PRODUCT_DESCRIPTION"] = product_description_input
                    refocus_env["USP"] = usp_input
                    refocus_env["USP_CONFIDENCE"] = usp_confidence
                    refocus_env["INDUSTRY"] = industry_input
                    refocus_env["GEOGRAPHY"] = geo_input
                    refocus_env["SCALE"] = scale_input
                    refocus_env["COMPETITOR_FOCUS"] = competitor_focus
                    refocus_env["ADDITIONAL_CONTEXT"] = refocus_context
                    refocus_env["ENABLE_CHARTS"] = str(enable_charts)
                    refocus_env["INCLUDE_MARKET_MAPS"] = str(include_market_maps)
                    refocus_env["REFOCUS_MODE"] = "true"  # Flag to indicate refocus mode

                    refocus_process = subprocess.run(
                        refocus_command,
                        capture_output=True,
                        text=True,
                        env=refocus_env,
                    )

                    if refocus_process.returncode != 0:
                        st.error("An error occurred during refocus analysis. Details below:")
                        st.code(refocus_process.stderr, language='bash')
                    else:
                        st.success("✅ Refocused Analysis Complete!")
                        
                        # Display the refocused report
                        refocus_report_file = 'refocused_market_analysis_report.md'
                        try:
                            with open(refocus_report_file, 'r', encoding='utf-8') as f:
                                refocus_report_content = f.read()
                            
                            # Clean up the markdown content
                            refocus_report_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', refocus_report_content)
                            
                            st.header("📄 Refocused Analysis Report")
                            with st.expander(f"View: {refocus_report_file}", expanded=True):
                                if debug_mode:
                                    st.code(refocus_report_content, language='markdown')
                                else:
                                    try:
                                        # Render the markdown content
                                        st.markdown(refocus_report_content, unsafe_allow_html=False)
                                        
                                        # Charts are now displayed in the main visualization section above
                                        
                                    except Exception as e:
                                        st.error(f"Error rendering markdown: {e}")
                                        st.code(refocus_report_content, language='markdown')

                            st.download_button(
                                label=f"Download Refocused Report",
                                data=refocus_report_content,
                                file_name=refocus_report_file,
                                mime='text/markdown',
                            )
                        except FileNotFoundError:
                            st.warning(f"The refocused report '{refocus_report_file}' was not generated.")
            else:
                st.warning("Please enter refocus context to continue.")
                
    except FileNotFoundError:
        st.warning(f"The final report '{report_file}' was not generated. Check the logs for errors.")
