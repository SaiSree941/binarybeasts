# Shikshak Mahodhay Project

This project consists of a **Flask server (backend)** and a **Streamlit app (frontend)**.

---

## **Backend Setup**
Follow these steps to set up the backend server.

### **Step 1: Create and Activate Virtual Environment**
```bash
conda create -n shikshak_env python=3.10
conda activate shikshak_env
```

### **Step 2: Install Dependencies**
```bash
pip install mistral_inference flask gtts
pip install -r requirements.txt
```

### **Step 3: Verify Installations**
```bash
pip show mistral_inference
pip show flask
```

### **Step 4: Run Backend Server**
```bash
python main.py
```

---

## **Frontend Setup**
Follow these steps to set up and run the frontend application.

### **Step 1: Install Dependencies**
```bash
pip install streamlit requests
```

### **Step 2: Run the Application**
```bash
streamlit run app.py
```

### **Step 3: Import Required Modules (inside app.py)**
```python
import streamlit as st
import requests
```

---

## **Notes**
- Ensure your backend server is running before starting the frontend.
- Modify `app.py` as needed for API integration.

---
