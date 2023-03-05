# GPT-prompts

GPT-prompts is a simple command line tool that allows you to write extensible ChatGPT prompt templates for different use cases, and then call them from your terminal.

# Install

```
pip install ChatGPT-cli
```

# Usage:

```
usage: GPT [-h] {commands} ...

A flexible interface to ChatGPT that allows you to easily define prompt
templates and extensible commands

positional arguments:
{commands}

options:
  -h, --help            show this help message and exit
```

You can specify templates and commands you want by calling `GPT configure`, and editing that file. This is the config template for a user that just has one command which labels a file.


```
key: <OpenAI API key>
commands:
  label:
    prompt: "I want you to label this text with salient themes, ideas or concepts. Also give it a title. Text: $!file \n Labels: "
    args:
      file: The file you want to label
	desc: Label files.
```

The `!` signals this corresponds to the `file` argument, and the `$` makes `GPT-cli` replace that with the file contents. You can also use anonymous arguments, for example in a command that analyzes your code:


```
commands:
  code:
    prompt: "I want you to analyze my code and how to make it cleaner and more efficient. You are a highly competent engineer at Google. Tell me about potential improvements in the code and directly provide inline suggestions for code changes you would make. Also describe what it does, and give it a rating out of 10. This is the code: \n$!arg1"
    desc: Analyze your code.

```

You can see some more example prompt templates in `commands.yml`. If you make any cool/useful ones, open a pull request and I might add it!

