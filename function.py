from g4f import Provider, ChatCompletion, models
from collections import defaultdict


user_messages = defaultdict(list)


def gpt_response(message, text) -> str:
    user_id = message.from_user.id
    user_messages[user_id].append({"role": "user", "content": text})
    if len(user_messages[user_id]) > 1:
        user_messages[user_id].append({"role": "assistant", "content": user_messages[user_id][-1]["content"]})
    gpt_reply = ChatCompletion.create(
        model=models.gpt_4,
        provider=Provider.Chatgpt4Online,
        messages=user_messages[user_id]
    )

    user_messages[user_id].append({"role": "assistant", "content": gpt_reply})
    print(gpt_reply)
    return gpt_reply
