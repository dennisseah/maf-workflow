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

## Custom Context Providers Example

- This sample illustrates how to create custom context providers in MAF.
- It includes examples of context providers that fetch user preferences and
  system status.
- The user preferences provider retrieves user-specific settings, while the
  system status provider checks the current state of the system.

```sh
task custom-context-providers
```

# Concurrent Agent Calls Example

- This sample demonstrates how to execute multiple agent calls concurrently
  using MAF.
- It defines two executors: one for providing factual information and another
  for generating creative poems.
- The sample shows how to run these executors in parallel and consolidate their
  results into a single response.

```sh
task concurrent-agent-calls
```

## Fan-In/Fan-Out Pattern Example

- This sample showcases the Fan-In/Fan-Out pattern using MAF WorkflowBuilder
- It defines two executors: one for generating poems and another for fetching
  factual information.
- The sample demonstrates how to run these executors concurrently and then
  consolidate their outputs into a unified response.

```sh
task fan-in-fan-out
```
