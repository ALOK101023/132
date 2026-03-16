import streamlit as st
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# --- पेज सेटअप ---
st.set_page_config(
    page_title="मजदूर अधिकार सहायक",
    page_icon="⚖️",
    layout="wide"
)

# --- API Key सुरक्षा ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("API Key नहीं मिली! कृपया Streamlit Secrets में 'OPENAI_API_KEY' जोड़ें।")
    st.stop()

# --- डेटा प्रोसेसिंग ---
@st.cache_resource
def initialize_system():
    if not os.path.exists("workers_rights.txt"):
        st.error("workers_rights.txt फाइल नहीं मिली। कृपया इसे GitHub पर अपलोड करें।")
        return None

    with open("workers_rights.txt", "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([text])
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    prompt = PromptTemplate(
        template="""आप एक अनुभवी कानूनी सहायक हैं। मजदूरों की समस्या का समाधान हिंदी में दें।
        
        नियम:
        1. संबंधित कानून (Act) का नाम जरूर लिखें।
        2. शिकायत करने का तरीका और हेल्पलाइन नंबर बताएं।
        3. भाषा बहुत सरल और मददगार होनी चाहिए।

        Context: {context}
        प्रश्न: {question}
        """,
        input_variables=['context', 'question']
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        RunnableParallel({'context': retriever | RunnableLambda(format_docs), 'question': RunnablePassthrough()})
        | prompt | llm | StrOutputParser()
    )

# --- साइडबार ---
with st.sidebar:
    st.title("⚖️ सहायता केंद्र")
    st.markdown("### 🌐 Bilingual Support\nEnglish & हिंदी")
    st.divider()
    st.info("यह ऐप मजदूरों को उनके अधिकारों के प्रति जागरूक करने के लिए बनाया गया है।")

# --- मुख्य इंटरफेस ---
st.title("⚖️ मजदूर अधिकार सहायक")
st.caption("श्रमिक अधिकारों की जानकारी | Supports Hindi & English")

try:
    chain = initialize_system()
    if chain:
        # त्वरित सुझाव (Pills)
        st.write("### मुख्य सवाल चुनें:")
        options = ["न्यूनतम वेतन की जानकारी", "मालिक पैसे नहीं दे रहा", "ओवरटाइम के नियम", "बिना नोटिस निकाल दिया"]
        selected_pill = st.pills("Options:", options, selection_mode="single", label_visibility="collapsed")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # चैट हिस्ट्री दिखाएँ
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # इनपुट हैंडलिंग
        user_query = None
        if selected_pill:
            user_query = selected_pill
        if prompt_input := st.chat_input("अपनी समस्या यहाँ विस्तार से लिखें..."):
            user_query = prompt_input

        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
            
            with st.chat_message("assistant"):
                with st.spinner("समाधान खोजा जा रही है..."):
                    response = chain.invoke(user_query)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

except Exception as e:
    st.error(f"सिस्टम एरer: {e}")
