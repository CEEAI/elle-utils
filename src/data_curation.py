import json
import time

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import APIConnectionError

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
            "Your task is to convert all numerical values, units (e.g., °C, µg/m³, µm, g/cm³), formulas and chemical expressions into the specified Markdown notation, using the `$...$` format for inline expressions. Additionally, correct any potential spelling mistakes in English and any character errors or typos in Chinese while ensuring that the intended meaning remains unchanged.",
        ),
        ("user", "The original question: {msgs}"),
    ]
)

structured_llm = llm.with_structured_output(json_schema)


with open("data/output/questions-en.json", "r") as f:
    questions = json.load(f)

updated_questions = []
for question in questions:
    try:
        prompt = prompt_template.invoke({"msgs": question.get("Question")})
        formatted_response = structured_llm.invoke(prompt).get("Question")

        question["Question"] = formatted_response
        updated_questions.append(question)

        time.sleep(1)
    except APIConnectionError as e:
        print(f"Connection error occurred: {e}")
        print(f"Skipping question: {question.get('Question')}")
        # Keep the original question without formatting
        updated_questions.append(question)
        continue

with open("data/output/questions-en-updated.json", "w", encoding="utf-8") as f:
    json.dump(updated_questions, f, indent=2, ensure_ascii=False)
