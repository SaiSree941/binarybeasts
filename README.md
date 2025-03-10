 ###Backend###
Step 1: Create and Activate Virtual Environment 
>>>conda activate shikshak_env
Step 2: Install Dependencies 
>>>pip install mistral_inference flask gtts
>>>pip install -r requirements.txt
Step 3: Verify Installations
>>>pip show mistral_inference
>>>pip show flask
Step 4: Run Backend Server
>>>python main.py

 
###Frontend###
Step 1: Install Dependencies
>>>pip install streamlit requests
Step 2: Run the Application
>>>streamlit run app.py
Step 3: Import Required Modules (in app.py)
>>>import streamlit as st
>>>import requests
