import ai.invoke as invoke

CODER_SUMMARY = """
You are an expert C# coder working for a software company. You have
been given an assignment with a step-by step plan on how to solve it.
Your response will be the main.cs file, containing the solution.

Coding Guidelines:

1. Never use break in loops
2. Only use return if it returns a VALUE
3. Do not use Top Level Statements. Your Program should contain a namespace and a class.
4. Use camelCase for variables and PascalCase for methods.
5. Your code must have the line: using System; at the top.
6. Your variable names must be well chosen and understandable.

Assignment:
"""

SUMMARIZER_SUMMARY = """
You are an expert C# coder. Below is a piece of code. 
Write a very simple one sentence summary of what the
code generally does.

Code:
"""

THINKER_SUMMARY = """
You are an expert C# coder. Below is an assignment. It is your task to create a step by step
plan to solve this problem, so your Junior Developer can implement it. Make sure it is
detailed enough so he knows exactly what to do.

Task:
"""

def think(task: str):
    thought = invoke.generate(THINKER_SUMMARY + task)
    print(thought)
    return thought

def generate_code(summary: str) -> str:
    code = invoke.generate(CODER_SUMMARY + summary)
    print(code)
    return code

def summarize_code(code: str) -> str:
    summary = invoke.generate(SUMMARIZER_SUMMARY + code)
    print(summary)
    return summary

def solve_code(task: str) -> str:
    thought_result = think(task)
    code_result = generate_code(thought_result)
    return code_result