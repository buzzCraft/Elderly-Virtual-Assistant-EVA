
import subprocess
import re

instruction = "You are a friendly assistant to old people. Answer with no more than two sentences."

# input(" Write to your assistent: ")
prompt = "I'm feeling alone. Nobody wants to talk with me."

# Define the command and its arguments as a list
cmd = [
    "wine","./main.exe",
    "-t", "12",
    "-m", "/app/model/model.q2_k.gguf",
    "--color",
    "-c", "4096",
    "--temp", "0.7",
    "--repeat_penalty", "1.1",
    "-n", "-1",
    "-p", f"<s>[INST] <<SYS>> {instruction} <</SYS>>  {prompt}! </s>"
]


# Run the command and capture its output

result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
# decoded_res = result.stdout.decode('utf-8')
# Extract the desired output using regex
cleaned_output = re.search(r'\[0m\s*(.*?)\s*$', result.stdout)
if cleaned_output:
    cleaned_output = cleaned_output.group(1)
    # print(cleaned_output)

with open("output.txt", "a", encoding="utf-8") as f:
    print(cleaned_output)
    f.write(f"Q: {prompt} \nA: {cleaned_output} \n\n")
    # unittest ----- if the answer is "None"