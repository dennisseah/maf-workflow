# Sample

Some sample to demonstrate MAF capabilities.

## Conditional Workflow Example

- When an input is provided, the sample code figures out if the message is
  - a greeting (e.g., "hello", "hi") or
  - an inappropriate message (e.g., "badword1", "badword2").
  - a statement (anything else).
  - a question.
- Based on the classification, it performs different actions:
  - For greetings, it responds with a friendly message.
  - For inappropriate messages, it flags them.
  - For statements, it acknowledges them.
  - For questions, it provides a generic answer.

```sh
task workflow-conditional -- hello
```

replace hello with any input message to see how the workflow responds.

## Multi-turn Conversation Example

- This sample demonstrates how to manage a multi-turn conversation using MAF.
- It shows how to serialize the conversation state and resume it later.
- The conversation involves an agent that interacts with a user, maintaining
  context across multiple exchanges.
- We also show how to create a custom chat message store to handle serialization
  and deserialization of the conversation state.

```sh
task multi-turns-conversation
```
