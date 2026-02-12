import streamlit as st

page = st.sidebar.radio("Choose page", ['About Project',
                                        'Performance Dashboard',
                                        'Promotion Eligibility Model'])

if page == 'About Project':
    import about_project
    about_project.background()
elif page == 'Performance Dashboard':
    import performance_dashboard
    performance_dashboard.dashboard()
else:
    import eligibility_model
    eligibility_model.model()