from g4f import Provider, ChatCompletion, models
import openai
from app import SYSTEM_PROMPT
import datetime


def unix_to_str(unix_time: int, timezone: str = "UTC") -> str:
    """
    Преобразует Unix-время в человекочитаемый формат.
    
    :param unix_time: Временная метка в формате Unix (количество секунд с 01.01.1970).
    :param timezone: Часовой пояс (по умолчанию UTC, можно передавать 'local' для локального времени).
    :return: Дата и время в формате YYYY-MM-DD HH:MM:SS.
    """
    if timezone.lower() == "local":
        dt = datetime.datetime.fromtimestamp(unix_time)
    else:
        dt = datetime.datetime.fromtimestamp(unix_time, tz=datetime.timezone.utc)
    
    return dt.strftime('%Y-%m-%d %H:%M:%S')




client_openai = openai.OpenAI(
    api_key="",
    base_url="https://api.sambanova.ai/v1",
)


async def g4f_response(text) -> str:
    gpt_reply = await ChatCompletion.create(
        model='gpt-35-turbo',
        provider=Provider.TeachAnything,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
    print(gpt_reply)
    return gpt_reply.choices[0].message.content


def with_reply(func):
    async def wrapped(client, message):
        if not message.reply_to_message:
            await message.edit("<b>Reply to message is required</b>")
        else:
            return await func(client, message)

    return wrapped
