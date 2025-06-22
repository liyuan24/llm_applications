

'''
The solution to the excercise of Anthropic's tool use tutorial https://github.com/anthropics/courses/blob/master/tool_use/04_complete_workflow.ipynb
This is a simple chatbot that uses the Anthropic API to answer questions.
It uses the get_article tool to get the contents of a recent wikipedia article about the topic.
'''
import re
import wikipedia
from anthropic import Anthropic

client = Anthropic()

model = "claude-3-7-sonnet-20250219"

article_search_tool = {
    "name": "get_article",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}

def get_article(search_term):
    results = wikipedia.search(search_term)
    first_result = results[0]
    page = wikipedia.page(first_result, auto_suggest=False)
    return page.content

def extract_answers(text):
    """
    Extracts all text between <answer> and </answer> tags.
    
    Args:
        text (str): Input string containing <answer> tags.
    
    Returns:
        List[str]: A list of extracted text between the tags.
    """
    pattern = r"<answer>(.*?)</answer>"
    ans = re.findall(pattern, text, re.DOTALL)
    return " ".join(ans) if ans else ""

def run_chatbot():
    import sys

    system_prompt = """
    You will be asked a question by the user. 
    If answering the question requires data you were not trained on, you can use the get_article tool to get the contents of a recent wikipedia article about the topic. 
    If you can answer the question without needing to get more information, please do so. 
    Only call the tool when needed. 
    """

    print("Welcome to Claude's Q&A Chatbot. Type 'exit' to quit.\n")

    while True:
        question = input("Enter your question: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        prompt = f"""
        Answer the following question <question>{question}</question>
        When you can answer the question, keep your answer as short as possible and enclose it in <answer> tags
        """
        messages = [{"role": "user", "content": prompt}]
        
        response = client.messages.create(
            model=model,
            system=system_prompt,
            messages=messages,
            max_tokens=1000,
            tools=[article_search_tool]
        )

        # Handle tool use if triggered
        while response.stop_reason == "tool_use":
            tool_use = response.content[-1]
            tool_name = tool_use.name
            tool_input = tool_use.input
            messages.append({"role": "assistant", "content": response.content})

            if tool_name == "get_article":
                search_term = tool_input["search_term"]
                print(f"Claude wants to get an article for {search_term}...")
                wiki_result = get_article(search_term)
                tool_response = {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": wiki_result
                        }
                    ]
                }
                messages.append(tool_response)
                response = client.messages.create(
                    model=model,
                    system=system_prompt,
                    messages=messages,
                    max_tokens=1000,
                    tools=[article_search_tool]
                )

        final_answer = extract_answers(response.content[0].text)
        print(f"Claude: {final_answer}\n")

if __name__ == "__main__":
    run_chatbot()
