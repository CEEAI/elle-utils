import json

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = init_chat_model("gpt-4o", model_provider="openai")

json_schema = {
    "title": "formatting_question",
    "description": "Formatting question",
    "type": "object",
    "properties": {
        "Question": {
            "type": "string",
            "description": "Formatted question",
        },
    },
    "required": ["Question"],
}

prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "Your task is to convert all units (e.g., °C), formulas and chemical expressions into the specified Markdown notation, using the `$...$` format for inline expressions.",
        ),
        ("user", "The original question: {msgs}"),
    ]
)

structured_llm = llm.with_structured_output(json_schema)


with open("data/output/questions-en.json", "r") as f:
    questions = json.load(f)

updated_questions = []
for question in questions:
    prompt = prompt_template.invoke({"msgs": question.get("Question")})
    formatted_response = structured_llm.invoke(prompt).get("Question")

    question["Question"] = formatted_response
    updated_questions.append(question)

with open("data/output/questions-en-updated.json", "w") as f:
    json.dump(updated_questions, f, indent=2)
