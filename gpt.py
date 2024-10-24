import g4f

g4f.debug.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # check version
print(g4f.Provider.Ails.params)  # supported args

# Automatic selection of provider

# streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Что такое s7 технология в радиосвязи"}],
    stream=True,
)

for message in response:
    print(message, flush=True, end='')

# normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_35_turbo,
    provider=g4f.Provider.TeachAnything,
    messages=[{"role": "user", "content": "Что такое s7 технология в радиосвязи"}],
)  # alternative model setting

print(response)
