import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="DSA Logic Builder", page_icon="💡")
st.title("💡 DSA 5-Step Logic Builder")
st.caption("Master LeetCode logic without spoilers!")

# 2. API Key Logic (Prioritize Streamlit Secrets, fallback to Sidebar)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    st.sidebar.info("[Get Free API Key here](https://aistudio.google.com)")

# 3. Sidebar Instructions
st.sidebar.markdown("""
### How to use:
1. Enter Problem Number/Title.
2. Get 5 logical micro-steps.
3. Solve the problem yourself!
""")

# 4. Input Area
problem_input = st.text_area("Paste LeetCode Problem Description or Title:", 
                             placeholder="Example: Leetcode 121 - Best Time to Buy and Sell Stock")

# 5. The Expert System Prompt
master_prompt = """
You are a 5-year experienced DSA Mentor. Your goal is to help students build intuition.
When a problem is provided:
1. Break it into exactly 5 logical micro-steps.
2. Step 1: Core Essence, Step 2: Brute Force Flaws, Step 3: Pattern Recognition, Step 4: Logic Blueprint, Step 5: Complexity.
3. DO NOT provide the full code solution. Use hints and pseudo-logic.
"""

if st.button("Generate 5-Step Blueprint"):
    if not api_key:
        st.error("Please provide an API Key to proceed.")
    elif not problem_input:
        st.warning("Please enter a problem title or description.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=master_prompt
            )
            
            with st.spinner("Analyzing logic..."):
                response = model.generate_content(f"Problem: {problem_input}")
                st.markdown("---")
                st.markdown("### 🎯 Your Logic Roadmap:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")
