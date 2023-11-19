import os
import glob
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv

def write_to_file(question, response, file_path="prompts_outputs.txt"):
    with open(file_path, "a") as file:
        file.write(f"Question: {question}\nResponse: {response}\n\n")

def main():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        st.error("OPENAI_API_KEY is not set. Please set it in your environment variables.")
        return

    st.set_page_config(page_title="Macroeconomic Researcher and Large Language Chat GPT -by TechTitans")
    st.header("Macroeconomic Researcher and Large Language Chat GPT -by TechTitans")

    local_directory = "CSV"
    csv_files = glob.glob(os.path.join(local_directory, "*.csv"))

    if csv_files:
        st.write(f"Found {len(csv_files)} CSV files.")
        csv_file_path = csv_files[0]

        user_question = st.text_input("Ask your questions :")
        if user_question:
            with st.spinner("Processing your question..."):
                agent = create_csv_agent(OpenAI(temperature=0), csv_file_path, verbose=True)
                response = agent.run(user_question)
                st.write(response)
                write_to_file(user_question, response)
    else:
        st.write("No CSV files found in the specified directory.")

if __name__ == "__main__":
    main()
