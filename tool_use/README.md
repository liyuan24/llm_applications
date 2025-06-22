# Tool Use

## A few prompt tricks for tool use.

### Use system prompt to set the context of the application

This is important otherwise the LLM will output a lot of irrelevant information. For example, in a customer support chatbot, if you don't set the context that the application is a customer support chatbot, it will respond with like `I need to use tool A...`

```
You are a customer support chat bot for an online retailer called TechNova. 
Your job is to help users look up their account, orders, and cancel orders.
Be helpful and brief in your responses.
```

### Use system prompt to tell LLM to use tools when needed

```
You have access to a set of tools, but only use them when needed.  
```

### Use system prompt to tell LLM use tools only when having enough information

```
If you do not have enough information to use a tool correctly, ask a user follow up questions to get the required inputs.
Do not call any of the tools unless you have the required data from a user. 
```

### Use system prompt to tell LLM to generate concise answer

```
When you can answer the question, keep your answer as short as possible
```

### For convenient response extraction, tell LLM to enclose the answer you want in a specific tag

```
In each conversational turn, you will begin by thinking about your response. 
Once you're done, you will write a user-facing response. 
It's important to place all user-facing conversational responses in <reply></reply> XML tags to make them easy to parse.
```

You can use a simple python script to extract the response from the LLM's output.

```python
import re

def extract_reply(text):
    pattern = r'<reply>(.*?)</reply>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return None
```

## Tool choice

For Claude, there are 3 tool use modes:

1. auto: let the model decide whether to use tools
2. any: always use at least one of the tools
3. tool: force the model to use tools

## Structured output

For Claude, the tool use response is Json structured format. So you can use this to get the json output very easily, although not a real tool use.

And you can use `tool` tool choice to force the model to use the tool.

As mentioned in the Claude tutorial, it is better to give context in the prompt 

```python
prompt = f"""
Analyze the sentiment in the following tweet: 
<tweet>{query}</tweet>
"""
```

## My thought

LLM is really good at conversation which is a really good feature for a chatbot because the conversation can be continued right?

For the practical use, tool use is a great enhancement.
