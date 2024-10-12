from openai import OpenAI
import os
import json


openai_api_key = os.environ.get("GPT")
prompts_path = "api/prompts.json"
with open(prompts_path, "r", encoding='utf-8') as f:
    all_prompt_list = json.load(f)

client = OpenAI(api_key=openai_api_key)
prompt = all_prompt_list["qs2"]

def combine_prompt(user_input: str="", prompt: dict=prompt) -> str:
    user_part = prompt["user_prefix"] + user_input + "\n" if user_input != "" else ""
    return prompt["starting_prompt"] + "\n".join(fact for fact in prompt["facts"]) \
              + "\n" + prompt["format"] + "\n" + user_part + "\n" + prompt["incremental"]

def gpt_response(user_input: str="", model="gpt-4o-mini") -> str:
    prompt = combine_prompt(user_input)
    messages = [
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    resp_text = response.choices[0].message.content.strip()
    # remove "Phrase: " from the response
    if resp_text.startswith("Phrase: "):
        return prompt, resp_text[8:]
    return prompt, resp_text


if __name__ == "__main__":
    prompt, response = gpt_response()
    print(prompt)
    print()
    print(response)
