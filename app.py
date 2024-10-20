
import streamlit as st

#passcode

PASS_CODE_dev = "111"
PASS_CODE_ver = "555"

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Guidelines & Standards", "About us"])
st.markdown(
    """
    <style>
    /* Change the sidebar background to light green */
    [data-testid="stSidebar"] {
        background-color: #ccffcc;  /* Light green */
    }
    /* Change the text color in the sidebar to dark blue */
    [data-testid="stSidebar"] .css-145kmo2 {
        color: #003366;  /* Dark blue */
    }
    /* Change the header text color in the sidebar to dark blue */
    [data-testid="stSidebar"] h1, h2, h3, h4, h5, h6 {
        color: #003366;  /* Dark blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if page == "Home":
    if 'page_redirect' in st.session_state:

        if st.session_state.page_redirect == "developer":
        
            st.title("Project Developer Portal")
            st.write("You can submit your project for evaluation here.")
            # Import and run the developer's page
            import developer
            developer.project_developer_page()

        elif  st.session_state.page_redirect == "verifier":
            st.title("Verification Entity Portal")
            st.write("You can view submitted projects here.")
            # Import and run the developer's page
            import verifier
            verifier.verifier_page()

    else:
        # Home page - before access to developer page
        st.image("sebastian-unrau-sp-p7uuT0tw-unsplash.jpg")
        st.markdown(
        """
        <style>
        .full-width-image {
            width: 100%;
            height: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
        st.title("Hi! Welcome to the NBS Project Submission Platform")
        st.subheader("The Problem: Time-Consuming Verification Processes")
        st.write("""Large enterprises are responsible for generating billions of metric tons of CO2 annually. To offset these emissions, they must invest in Nature-Based Solutions (NBS), which involve ecosystem conservation, restoration, or management. However, before these projects can generate carbon credits, they must go through a rigorous verification process. This process, led by Verra—the leading project registry in the voluntary carbon market—can take up to 545 days, during which projects are unable to generate monetized carbon credits.
The verification process is slow due to inefficient communication between Verra and project developers. A prolonged back-and-forth exchange of feedback contributes to significant delays, affecting NBS project availability and ultimately hindering efforts to address the global carbon emissions crisis.
This issue is particularly evident for companies, which are involved in multiple NBS projects. For them, delayed verification could lead to financial losses totaling hundreds of millions of dollars.""")
        st.subheader("Our Solution: AI-Enhanced Verification Interface")
        st.write("""We’ve developed a solution to cut down verification times by 40%. Our AI-powered interface streamlines the communication process between project developers and verifiers, making it faster and more efficient. 
        By leveraging Large Language Models (LLMs) trained on comprehensive carbon-market resources, verification standards, and past NBS projects, our interface helps both parties stay aligned and organized. This ensures that project documentation is complete and of high quality, allowing Verra’s verification process to begin sooner, without the back-and-forth delays.""")
        st.subheader("How does it work for our stakeholders?")
        st.write("""
        - for project developers:
        - for project verifiers:
        - for companies/third parties:
        """)
        st.write("""
        
                 
                 Whether you\'re a Project Developer or a Verifier, our interface can transform how you interact with the voluntary carbon market. 
                 \n Click on the button to access corresponding portal.""")


    
    
        left, right = st.columns(2)
    
    
        if 'page_redirect' not in st.session_state or st.session_state.page_redirect != "developer":
    
            with left:
    
    
                with st.popover("Project Developer"):
                    st.write("Project Developer Log-in")
                    entered_code = st.text_input("Please, enter the passcode to proceed:")
                    if st.button("Submit", key="developer_submit"):
                        if entered_code == PASS_CODE_dev:
                            st.session_state.page_redirect = "developer"
                            st.success("Code correct! Redirecting to Project Developer page...")
                            st.rerun()  
            
                        else:
                            st.error("Incorrect code. Please try again.")
    
    
        if 'page_redirect' not in st.session_state or st.session_state.page_redirect != "developer":
        
            with right:
                
                
                with st.popover("Verification Entity"):
                    st.write("Verification Entity Log-in")
                    entered_code = st.text_input("Enter the passcode to proceed:")
                    if st.button("Submit", key="verifier_submit"):
                        if entered_code == PASS_CODE_ver:
                            st.session_state.page_redirect = "verifier"
                            st.success("Code correct! Redirecting to Verification Entity page...")
                            st.rerun()  
            
                        else:
                            st.error("Incorrect code. Please try again.")



        tab1, tab2, tab3, tab4 = st.tabs(["Verra", "Carbon Credits", "Voluntary Carbon Market", "NBS"])

        with tab1:
            st.header("Verra")
            st.write(""" Verra is a leading global organization that operates as a project registry in the voluntary carbon market. Its primary role is to oversee and certify Nature-Based Solutions (NBS) and other carbon reduction projects, ensuring that they meet rigorous standards for generating carbon credits. These credits are then sold or traded to companies and organizations seeking to offset their carbon emissions.

Key functions of Verra include:

- Certifying Carbon Projects: Verra assesses and verifies projects that aim to reduce or sequester greenhouse gases. It ensures that the projects follow established standards, such as the Verra Carbon Standard (VCS) and the Climate, Community & Biodiversity Standard (CCB), to ensure the environmental and social benefits of the projects.

- Issuing Carbon Credits: Once verified, projects receive carbon credits, which represent one metric ton of CO2 removed or reduced from the atmosphere. These credits can be sold to corporations or individuals looking to offset their carbon emissions.

- Ensuring Transparency and Integrity: Verra provides a transparent platform that tracks the issuance and retirement of carbon credits, making sure that the carbon credits are legitimate and not double-counted.

The main problem of verification process right now is it being lengthy and inefficient. 
The initial four stages of the verification and validation process alone require at least 140 days of only iterative feedback exchange via email, Linkedin, and Verra’s website. In each stage, Verra and its Verification Bodies must manually compare every iteration of the submitted project to multiple standards.
Currently, there’s a lack of systematization and automation. 
            
            """)
            st.subheader("Verra Carbon Standart (VCS)")
            st.write("""The Verra Carbon Standard (VCS) is a global certification standard for carbon offset projects. 
            It provides a rigorous framework for verifying and validating greenhouse gas (GHG) emission reductions or removals, ensuring the credibility of carbon credits. 
            Projects that meet VCS criteria are issued carbon credits, which can be traded to help companies and individuals offset their emissions.
            Methodologies in the context of the Verra Carbon Standard (VCS) are detailed guidelines that define how to calculate the amount of greenhouse gas (GHG) emissions reduced or removed by a project. These methodologies establish the rules for quantifying, monitoring, and reporting emission reductions, ensuring consistency, accuracy, and transparency across different projects.
            An example of a VCS-approved methodology is the VM0003 "Methodology for Avoided Conversion of Forests".
            This methodology applies to projects that focus on avoiding deforestation or forest degradation in regions where forests are at risk of being converted to non-forest land uses, such as agriculture or urban development.
            """)
            
        
        with tab2:
            st.header("Carbon Credits")
            st.write("""
Carbon credits are a form of environmental currency used to offset greenhouse gas emissions. They represent the removal or avoidance of one metric ton of carbon dioxide (CO2) or its equivalent in other greenhouse gases, achieved through various projects like renewable energy, reforestation, or methane capture.
These credits can be bought and sold, enabling companies, governments, or individuals to offset their own emissions by investing in projects that reduce emissions elsewhere. For example, a company that cannot fully reduce its emissions may purchase carbon credits to compensate for the remainder, helping to achieve its sustainability or climate goals.
            """)
            
        with tab3:
            st.header("Voluntary Carbon Market")
            st.write("""
            The voluntary carbon market is a marketplace where individuals, companies, and organizations can buy and sell carbon credits voluntarily, outside of mandatory government-regulated emissions reduction programs. In this market, participants purchase carbon credits to offset their greenhouse gas emissions by investing in projects that reduce or remove CO2 emissions, such as reforestation, renewable energy, or methane capture initiatives.
Unlike the compliance carbon market, which is driven by regulatory requirements (e.g., cap-and-trade systems), the voluntary market operates on a purely voluntary basis, driven by participants' desire to meet sustainability targets or corporate social responsibility goals. It is a critical tool for accelerating global emissions reductions, especially for sectors where direct emissions reduction is challenging.
""")
        
        with tab4:
            st.header("NBS - Natural-based solutions")
            st.write("""Nature-Based Solutions (NBS) refer to strategies that use natural processes and ecosystems to address environmental challenges, such as climate change, biodiversity loss, and water management. These solutions focus on conserving, restoring, or enhancing natural ecosystems to provide sustainable, long-term benefits for both the environment and society.

Examples of NBS include:

Reforestation and afforestation: Planting trees to absorb carbon dioxide and restore habitats.
Wetland restoration: Rehabilitating wetlands to store carbon, improve water quality, and provide flood control.
Agroforestry: Integrating trees into agricultural systems to improve soil health, increase carbon sequestration, and support biodiversity.
Coastal ecosystem restoration: Rebuilding mangroves, salt marshes, and coral reefs to protect against sea-level rise and enhance marine biodiversity.
NBS projects play a significant role in the voluntary carbon market by generating carbon credits, as they help to reduce or remove greenhouse gas emissions through natural means.
            """)
                
                    



    

elif page == "Guidelines & Standards":
    st.title("Guidelines & Standards")
    st.write("The projects relies on the publicly available data provided by Verra.")

else:
    st.title("About us")
    st.write("The project aims to...")




