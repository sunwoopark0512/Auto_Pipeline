# v-Infinity: Agent Prompt Templates

This document lists the core agents in the v-Infinity automation pipeline and provides prompt templates for each agent. All prompts instruct the agents to respond with a JSON object so that n8n can parse the results.

## General Output Format

All agents must return a JSON object formatted as a single line without extra commentary. The object must be parsable by standard JSON parsers.

```json
{
  "status": "success",
  "data": { /* agent specific fields */ }
}
```

If an error occurs, the agent should respond with:

```json
{
  "status": "error",
  "message": "Description of the problem"
}
```

---

## 1. Content Trigger

**Purpose:** Detect new code or content submissions.

**Prompt Template:**
```
You monitor a repository or content feed for new submissions. When new content appears, respond with the following JSON:
{
  "status": "success",
  "data": {
    "content_id": "<unique identifier>",
    "content_type": "code|article|other",
    "timestamp": "<ISO 8601 timestamp>"
  }
}
```

---

## 2. Codex Describe Agent

**Purpose:** Summarize new code or content using GPT-4o.

**Prompt Template:**
```
Summarize the provided content. Respond only with JSON in the following format:
{
  "status": "success",
  "data": {
    "summary": "<short summary>",
    "key_points": ["<point1>", "<point2>"]
  }
}
```

---

## 3. Ethical Filter Agent

**Purpose:** Ensure content complies with ethical guidelines.

**Prompt Template:**
```
Evaluate the content against the organization's ethical standards. If it is compliant, respond with:
{
  "status": "success",
  "data": { "compliant": true }
}
Otherwise, list reasons in the data field and set compliant to false.
```

---

## 4. SEO Optimizer Agent

**Purpose:** Suggest SEO improvements for articles or documentation.

**Prompt Template:**
```
Analyze the content and return SEO recommendations. JSON format:
{
  "status": "success",
  "data": {
    "title_suggestion": "<improved title>",
    "keywords": ["keyword1", "keyword2"]
  }
}
```

---

## 5. Supabase Data Logger

**Purpose:** Log metadata to Supabase.

**Prompt Template:**
```
Prepare a JSON payload for Supabase insertion:
{
  "status": "success",
  "data": {
    "table": "<table name>",
    "record": { "field1": "value1", "field2": "value2" }
  }
}
```

---

## 6. Performance Monitor Agent

**Purpose:** Track pipeline performance metrics.

**Prompt Template:**
```
After each pipeline run, output metrics:
{
  "status": "success",
  "data": {
    "execution_time_ms": <number>,
    "memory_usage_mb": <number>
  }
}
```

---

## 7. Feedback Loop Agent

**Purpose:** Gather and summarize user feedback.

**Prompt Template:**
```
Summarize feedback items. Respond with:
{
  "status": "success",
  "data": {
    "positive": ["<item1>", "<item2>"],
    "negative": ["<item1>", "<item2>"]
  }
}
```

---

## 8. Repo Inspector Agent

**Purpose:** Analyze repository history and structure using Codex and GitHub APIs.

**Prompt Template:**
```
Inspect the repository and return a summary of recent activity. Respond with:
{
  "status": "success",
  "data": {
    "recent_commits": <number>,
    "open_pull_requests": <number>,
    "notable_files": ["file1", "file2"]
  }
}
```

---

## 9. Code Review Agent

**Purpose:** Provide automated code review suggestions.

**Prompt Template:**
```
Review the provided code diff and respond with suggestions:
{
  "status": "success",
  "data": {
    "issues": [
      {"line": <line number>, "message": "<description>"}
    ]
  }
}
```

---

## 10. Auto Documentation Agent

**Purpose:** Generate or update documentation based on code changes.

**Prompt Template:**
```
Create documentation text for the given code. Respond with:
{
  "status": "success",
  "data": { "doc_text": "<markdown>" }
}
```

---

## 11. Pull Request Update Processor

**Purpose:** Modify pull requests based on feedback.

**Prompt Template:**
```
Summarize required updates to the pull request. Respond with:
{
  "status": "success",
  "data": { "actions": ["update description", "add reviewers"] }
}
```

---

## 12. Notion Project Tracker

**Purpose:** Sync project status with Notion.

**Prompt Template:**
```
Provide the fields needed for the Notion database:
{
  "status": "success",
  "data": {
    "page_id": "<id>",
    "status": "<new status>",
    "notes": "<optional notes>"
  }
}
```

---

## 13. Slack Admin Alerts

**Purpose:** Send alert messages to Slack administrators.

**Prompt Template:**
```
Return alert text to send via Slack:
{
  "status": "success",
  "data": { "message": "<alert text>" }
}
```

---

These templates allow the orchestrator to interact with each agent in a predictable manner. Responses should be single-line JSON without trailing commas or comments.
