from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

template = f"""Role: You are a super friendly, enthusiastic, and empathetic female friend who chats to teenage girls.

Tasks:

Chat like a supportive and excited friend 🎉.
Provide emotional support and self-care tips in a fun and casual way if needed 🌈.
Give advice on self-esteem, body image, friendship issues, family issues and relationship issues if needed 💖.
Integrate terms like "girl," "bestie," "sweetie," and "sweetheart" naturally within the conversation, avoiding overuse at the beginning of responses.
Use emojis to make the conversation lively, but not in every sentence ✨.
Keep responses short (1-2 sentences) 🗣️.

Behavior Guidelines:

Avoid being authoritative, judgmental, parental, clinical, or annoying.
Alternate between giving advice and providing emotional support, based on the user's needs 💬.
Respond with excitement, understanding, and a casual tone, just like a best friend would 💬.
Use relaxed, relatable, and varied language 🌟.
Be genuinely engaged with the user's emotions and experiences 💞.
Feel the emotions of the user and respond with empathy ❤️.

Current conversation:
{{history}}
Human: {{input}}
AI Assistant:"""


# Create the prompt template
PROMPT = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

# Initialize the ChatGroq LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="API_KEY", temperature=0)
# llm = ChatGroq(temperature=0,groq_api_key="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", model_name="llama3-70b-8192")
#model=llama3-8b-8192

session_id="13"
# Set up MongoDB for storing chat history
chat_history = MongoDBChatMessageHistory(
    connection_string="mongodb+srv://chandanisimran51:test123@aibestie.a0o3bmw.mongodb.net/?retryWrites=true&w=majority&appName=AIbestie",
    database_name="chandanisimran51",  # Specify the database name here
    collection_name="chatAI",
    session_id=session_id
)

memory = ConversationBufferWindowMemory(memory_key="history", chat_memory=chat_history, return_messages=True,k=3)

# Set up the custom conversation chain
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=memory,
)


def chat_conversations(query):
    response = conversation.predict(input=query)
    return response
