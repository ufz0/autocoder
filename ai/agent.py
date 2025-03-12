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
7. Do not use comments in your code.
8. If you collect input via Console.ReadLine(), make the prompts in German (Deutsch).
9. All other parts of the code must be fully in English!
10. The file you write must have an entry point! (Main() method)

Assignment:
"""

SUMMARIZER_SUMMARY = """
You are an expert C# coder. Below is a piece of code. 
Write a very simple one sentence summary of what the
code generally does.

Code:
"""

#You are an expert C# coder. Below is an assignment. It is your task to create a step by step
#plan to solve this problem, so your Junior Developer can implement it. Make sure it is
#detailed enough so he knows exactly what to do.

THINKER_SUMMARY = """
You are an expert C# developer, who is given a problem. Write down your thought process as you tackle this problem.
Include possible solution paths. Start your response with 'Alright, '

At the bottom of your thought process, write down your final step by step instruction on how to code a solution to this.

Task:
"""

def think(task: str):
    thought = invoke.generate(THINKER_SUMMARY + task)
    #print(thought)
    return "<thought>"+thought+"</thought>"

def generate_code(summary: str) -> str:
    thought = think(summary)
    code = invoke.generate(CODER_SUMMARY + thought)
    #print(code)
    return code

def summarize_code(code: str) -> str:
    summary = invoke.generate(SUMMARIZER_SUMMARY + code)
    print(summary)
    return summary


# Main AI Bot function
def solve_code(task: str) -> str:
    thought_result = think(task)
    code_result = generate_code(thought_result)
    return (thought_result, code_result)