import google as genai
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

SYSTEM_PROMPT = config.get('g4f', 'SYSTEM_PROMPT')

client = genai.Client(api_key="AIzaSyCUaRs9G3r-Qx7uGoV0EXFSVaolqQbkQoo")


def gemini_response(user_input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[user_input])
    return response.text
  
  
  
# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction=SYSTEM_PROMPT,
)

chat_session = model.start_chat(
  history=[
  ]
)


def gemini_response_chat(user_input):
    response = chat_session.send_message(user_input)
    return response.text


def with_reply(func):
    async def wrapped(client, message):
        if not message.reply_to_message:
            await message.edit("<b>Требуется ответить на сообщение.</b>")
        else:
            return await func(client, message)

    return wrapped
