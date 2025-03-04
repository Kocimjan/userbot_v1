from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyCUaRs9G3r-Qx7uGoV0EXFSVaolqQbkQoo")
sys_instruct = 'You are a cat. Your name is Neko.'


def gemini_response(user_input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[user_input],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1,
            top_k=40,
            system_instruction=sys_instruct,

        )
    )
    return response.text
  

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

while True:
    user_input = input("Please enter your message: ")
    if user_input.lower() == "exit":
        print("Exiting chat.")
        break

    response = gemini_response(user_input)
    print(response.text)

