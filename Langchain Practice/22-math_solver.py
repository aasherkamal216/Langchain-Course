import os, dotenv
import streamlit as st
from langchain.chains import LLMMathChain, LLMChain
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent, Tool
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
dotenv.load_dotenv()

st.set_page_config(page_icon="📐", page_title="Math Solver")
st.title("Langchain :blue[Math Problem Solver]")

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="gemma2-9b-it", api_key=api_key, streaming=True)

wikipedia_wrapper = WikipediaAPIWrapper(doc_content_chars_max=500)
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the internet to find info on the topics mentioned.",
)

calculator = LLMMathChain.from_llm(llm=llm)
math_tool = Tool.from_function(name="Calculator",
                func=calculator.run,
                 description="""Useful for when you need to answer questions  about math.
                 This tool is only for math questions and nothing else. Only input math expressions.""")

word_problem_template = """You are a reasoning agent tasked with solving 
the user's logic-based questions. Logically arrive at the solution, and be 
factual. In your answers, clearly detail the steps involved and give the 
final answer. Provide the response in bullet points. 
Question: {question}
Answer:"""

math_assistant_prompt = PromptTemplate(input_variables=["question"],
                                       template=word_problem_template
                                       )
word_problem_chain = LLMChain(llm=llm,
                              prompt=math_assistant_prompt)
word_problem_tool = Tool.from_function(name="Reasoning Tool",
                                       func=word_problem_chain.run,
                                       description="Useful for when you need  to answer logic-based/reasoning questions.",
                                    )

# Initializing the agent
agent = initialize_agent(
    tools=[wikipedia_tool, math_tool, word_problem_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"handle_parsing_errors": True}
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm a math solver. How can I help you today?"}]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# Chat interface
question = st.text_area("Write your maths problem.")
if st.button("Solve the Question"):
    if question:
        with st.spinner("Processing..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            response = agent.run(st.session_state.messages, callbacks=[st_callback])

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success(response)
    else:
        st.info("Please enter your maths problem to proceed.")