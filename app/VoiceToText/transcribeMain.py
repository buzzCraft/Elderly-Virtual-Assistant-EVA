from transcribeMagic import transcribe_magic

# Run the magic
result = (
    transcribe_magic()
)  # result will be passed to Llm for processing, takes a few seconds after recording
print(result)
