import streamlit as st


st.set_page_config(
    page_title="ML platform",
    page_icon="🏠",
)

st.write("# Welcome to ML platform - MLOps Zoomcamp")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ## Tech Stack
   
"""
)

left_tech_img, center_tech_img, right_tech_img = st.columns(3)
left_tech_img.markdown(
    """
    **ML monitoring**:
    """
)
left_tech_img.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Grafana_logo.svg/1200px-Grafana_logo.svg.png",  width=150)

center_tech_img.markdown(
    """
    **ML lifecycle**:
    """
)
center_tech_img.image("https://avatars.githubusercontent.com/u/39938107?v=4",  width=150)
right_tech_img.markdown(
    """
    - **Pipeline orchestration**:
    """
)
right_tech_img.image("https://www.prefect.io/images/brand-assets/new-logos-and-images/SVG/prefect-full-logo-light-BG.svg",  width=200)

left_tech_img2, center_tech_img2, right_tech_img2 = st.columns(3)

left_tech_img2.markdown(
    """
    **ML Serving**:
    """
)
left_tech_img2.image("https://cdn.freebiesupply.com/logos/thumbs/2x/flask-logo.png",  width=200)
