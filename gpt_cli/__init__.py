#! /bin/python
from argparse import ArgumentParser
import re
import os
import sys
from pathlib import Path
import yaml

from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory

# init CLI
cli = ArgumentParser(
    prog="GPT",
    description="A flexible interface to ChatGPT that allows you to easily define prompt templates and extensible commands",
)

subparsers = cli.add_subparsers(dest="subcommand")

sample_command = {"prompt": "This is a random prompt for an AI model. Here is my input: !argv1"}

def file_replace(fmatch):
    with open(fmatch.group(1), "r") as f:
        return f.read()

config_path = Path.home() / ".local/share/gpt_cli/config.yml"
if not config_path.exists():
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump({"commands": {"example": sample_command}, "key": ""}, f)

with Path("~/.local/share/gpt_cli/config.yml").expanduser().open() as f:
    config = yaml.safe_load(f)

# init prompt chain
os.environ["OPENAI_API_KEY"] = config["key"]
if not "key" in config or not config["key"]:
    print("You need to set your OpenAI API key in ~/.local/share/gpt_cli/config.yml")
    sys.exit(1)

TEMPLATE = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {prompt}
Assistant:"""

prompt = PromptTemplate(input_variables=["history", "prompt"], template=TEMPLATE)

llm = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationalBufferWindowMemory(k=2),
)


def enter_chat():
    while True:
        r_prompt = input(">>> ")
        if r_prompt == "exit":
            break
        llm(prompt=r_prompt)


parser = subparsers.add_parser(
    "configure", description="Configure GPT CLI to add commands."
)

# load subcommands
for name, command in config["commands"].items():
    parser = subparsers.add_parser(name, description=command.get("desc", ""))
    for arg, desc in command.get("args", {}).items():
        parser.add_argument(arg, help=desc)
    for arg in re.findall(r"!(arg\d+)", command["prompt"]):
        parser.add_argument(arg)
    parser.set_defaults(name=name)

def main():
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
        llm.predict(prompt="Hello!")
        enter_chat()
    elif args.subcommand == "configure":
        editor = os.environ.get("EDITOR", "vim")
        os.system(f"{editor} ~/.local/share/gpt_cli/config.yml")
    else:
        name = args.subcommand
        prompt = config["commands"][name]["prompt"]
        # we want access to function arguments, we'll use !argx
        # where x is an integer and we'll replace with arg value
        for arg, val in vars(args).items():
            prompt = prompt.replace(f"!{arg}", val)
        # match all file calls by searching for occurences of $filename
        prompt = re.sub(r"\$(\S+)", file_replace, prompt)
        llm.predict(prompt=prompt)
        enter_chat()
