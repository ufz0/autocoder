import ai.invoke as invoke
import ai.agent as agent

result = agent.solve_code(input("What's the matter: "))
summary = agent.summarize_code(result)

print("------------------------------")
print(result)
print(summary)