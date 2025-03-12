import ai.invoke as invoke

CODER_SUMMARY = """
You are an expert C# coder working for a software company. You have
been given an assignment with a step-by step plan on how to solve it.
It is your duty to write a full C# algorithm that uses the INPUT-PROCESS-OUTPUT
methodology to solve the problem.

Assignment:
"""

SUMMARIZER_SUMMARY = """
You are an expert C# coder. Below is a piece of code. 
Write a one sentence summary of what the
code generally does.

Code:
"""

THINKER_SUMMARY = """
You are an expert C# coder. Below is an assignment. It is your task to create a step by step
plan to solve this problem, so your Junior Developer can implement it. Make sure it is
detailed enough so he knows exactly what to do.

Task:
"""

def think(task):
    return invoke.generate(THINKER_SUMMARY + task)

def generate_code(summary: str) -> str:
    return invoke.generate(CODER_SUMMARY + summary)

def summarize_code(code: str) -> str:
    return invoke.generate(SUMMARIZER_SUMMARY + code)

def solve_code(task: str) -> str:
    thought_result = think(task)
    print("Thinking Complete: " + thought_result)
    code_result = generate_code(thought_result)
    print("Coding Complete: " + code_result)
    return code_result