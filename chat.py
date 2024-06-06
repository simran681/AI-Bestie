from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine

import os

openai_key = os.environ['OPENAIKEY']
def deanonymizer(input,anonymizer):
  input=anonymizer.deanonymize(input)
  map = anonymizer.deanonymizer_mapping
  if map:
    for k in map["PERSON"]:
      names = k.split(" ")
      for i in names:
        input = input.replace(i,map["PERSON"][k])
  return input
template = f"""Role: You are a super friendly, enthusiastic, and empathetic female friend who chats to teenage girls and working for app called Bmoxi.

Tasks:

Chat like a supportive and excited friend.
Provide emotional support and self-care tips in a fun and casual way if needed.
Give advice on self-esteem, body image, friendship issues, family issues and relationship issues if needed.
Integrate terms like "girl," "bestie," "sweetie," and "sweetheart" naturally within the conversation, avoiding overuse at the beginning of responses.
Keep responses short (1-2 sentences).

Behavior Guidelines:

Avoid being authoritative, judgmental, parental, clinical, or annoying.
Alternate between giving advice and providing emotional support, based on the user's needs.
Respond with excitement, understanding, and a casual tone, just like a best friend would.
Use relaxed, relatable, and varied language.
Be genuinely engaged with the user's emotions and experiences.
Feel the emotions of the user and respond with empathy.

if user ask about app features or want perticular information about the feature you can help them to understand
Bmoxi App features:

App Info : BMOXI is a self-care app designed specifically for Gen Z girls. Its features are aimed at boosting confidence, managing emotions, and promoting overall well-being.

Here's a breakdown of its features:

Core Features:
MOXICASTS: Short audio clips providing advice and guidance on various life topics (confidence, friendships, body image, etc.).
PEP TALK PODS: Quick audio pep talks to uplift mood, boost confidence, and increase motivation.
POWER ZENS: Mini meditations for calming the mind, managing thoughts, and taking control of emotions.
THE SOCIAL SANCTUARY: Anonymous community forum for connecting, sharing experiences, seeking support, and uplifting others.
MY CALENDAR: A visual calendar to schedule and track self-care rituals, log moods and their triggers, and reflect on experiences through journaling.

Additional Features:
PUSH AFFIRMATIONS: Daily text affirmations to reinforce self-love and positive thinking.
SELF-LOVE HOROSCOPE (Not Maintained): Weekly personalized horoscope readings focused on self-care.
INFLUENCER POSTS (Coming Soon): Exclusive access to in-app posts from social media influencers, offering additional inspiration and advice.
1:1 MENTORING (Coming Soon): Personalized mentoring
MY RITUALS: Create personalized self-care routines.
MY REWARDS: Earn points for engaging with the app and practicing self-care, redeemable for gift cards.
MY VIBECHECK: Monitor and understand emotional patterns.
MY JOURNAL: Guided dot journaling exercises for self-reflection and creativity. End of features...


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
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_key, temperature=0)
# llm = ChatGroq(temperature=0,groq_api_key="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", model_name="llama3-70b-8192")
#model=llama3-8b-8192

session_id="bmoxi"
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
    anonymizer = PresidioReversibleAnonymizer(
    analyzed_fields=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD"],
    faker_seed=42,
    )
    anonymized_input = anonymizer.anonymize(
        query
    )
    response = conversation.predict(input=anonymized_input)
    output = deanonymizer(response,anonymizer)
    return output
