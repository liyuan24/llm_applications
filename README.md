This is a repo for my experimentations on the LLM applications

## Prerequisites

Set Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your_api_key"
```

Set OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key"
```

## Interleaved Thinking

This is from Claude Developer Documentation: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking

The interleaved thinking allows Claude to think between the tool use block and tool result block.

## Tool use

Basically follow the Claude tool use [tutorial](https://github.com/anthropics/courses/tree/master/tool_use). Highly recommend it!

## Troubleshooting

### The environment variable cannot be found in Cursor or VSCode when using Jupyter Notebook

In my case, I set the environment variable in the `.bashrc` file, but it was not found in Jupyter Notebook. The following steps worked for me:

1. Close Cursor
2. In the terminal, run `source ~/.bashrc`
3. Restart Cursor







