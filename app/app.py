import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.rag_pipeline import generate_answer

def main():
    st.set_page_config(page_title="Government Schemes RAG Bot", page_icon="https://i.pinimg.com/736x/8a/d6/6c/8ad66c42bf180f427f51c3e651facd81.jpg")
    st.title("Government Schemes - QA Assistant")

    st.write("Ask anything about government schemes in India!")

    user_query = st.text_input("Enter your question:", placeholder="e.g., What are schemes available for farmers in Maharashtra?")
    
    if st.button("Get Answer") or (user_query and st.session_state.get("auto_submit", False)):
        if user_query.strip() == "":
            st.warning("Please enter a valid question!")
        else:
            with st.spinner("Searching schemes and generating answer..."):
                try:
                    answer = generate_answer(user_query)
                    st.success("Answer generated successfully!")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("---")
    st.caption("Built by Suyash🚀")

if __name__ == "__main__":
    main()
