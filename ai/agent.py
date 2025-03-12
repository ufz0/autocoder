import ai.invoke as invoke

CODER_SUMMARY = """
You are an expert C# coder working for a software company. You must write your code according to the following guidelines:

1. Do not use break statements.

Do not leave methods empty. If you leave them empty, you are FIRED.

Below is your task:

"""

SUMMARIZER_SUMMARY = """
You are an expert C# coder. Below is a summary of a piece of code. 
Write a one sentence summary of what the
code generally does.

Code:
"""

def generate_code(summary: str) -> str:
    return invoke.generate(CODER_SUMMARY + summary)

def summarize_code(code: str) -> str:
    return invoke.generate(SUMMARIZER_SUMMARY + code)