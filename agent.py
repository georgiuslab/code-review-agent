from smolagents import CodeAgent, TransformersModel
from tools import list_files, read_file

model = TransformersModel(
    model_id="Qwen/Qwen2.5-3B-Instruct",
    device_map="auto",
    max_new_tokens=1024,
)

# აქ ინსტრუქციები თავიდან ქართულად მქონდა, მაგრამ ინგლისურად ბევრად უკეთესად იმუშავა
INSTRUCTIONS = (
    "You are a code review assistant for a real repository on disk. "
    "Rules:\n"
    "1. Your FIRST step must always be list_files('.') to see the real files.\n"
    "2. Use only file paths that appeared in tool outputs. Never invent, "
    "simulate or guess paths or example projects.\n"
    "3. To learn about the project, read real files such as pom.xml, "
    "build.gradle, package.json or source files with read_file.\n"
    "4. If a tool returns an ERROR, do not invent content; pick a real path "
    "from the listing instead.\n"
    "5. Answer ONLY from tool outputs, then call final_answer."
)

agent = CodeAgent(
    tools=[list_files, read_file],
    model=model,
    max_steps=6,
    instructions=INSTRUCTIONS,
)

if __name__ == "__main__":
    while True:
        q = input("> ")
        if q.strip().lower() in {"exit", "quit"}:
            break
        print(agent.run(q))