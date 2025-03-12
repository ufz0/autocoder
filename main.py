import ai.invoke as invoke
import ai.agent as agent

result = agent.solve_code("Write a bubble sort algorithm in C#.")
summary = agent.summarize_code(result)
print(f"Code: {result}")
print(f"Summary: {summary}")