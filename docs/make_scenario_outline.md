# Make.com Scenario Outline

This document describes how to automate the v-Infinity content pipeline using Make.com. The scenario connects external triggers to the pipeline API and keeps track of the status in Supabase, Notion, and Slack.

```mermaid
flowchart TD
    A[Webhook Trigger (Form, Zapier, Airtable)] --> B[HTTP Request to Pipeline API `/format`]
    B --> C[Create Content Row in Supabase]
    C --> D[Call `/variants`, `/snippet`, `/graphic`]
    D --> E[Store all variants to Supabase]
    E --> F[Call `/hook_uploader` → Upload]
    F --> G[Call `/auto_insight` → Notion Summary]
    G --> H[Slack Notification + Status Update]
```

## Module Breakdown

| Step | Module Name                 | Purpose                                              | Make.com Module                                                   |
|------|----------------------------|------------------------------------------------------|------------------------------------------------------------------|
| A    | Trigger                    | Accept external input                                | Webhook module or Google Form connection                         |
| B    | Formatter                  | Automatically format content                         | HTTP module: **POST** `/format`                                  |
| C    | Supabase Save              | Create initial content row                           | Supabase: Insert Row                                             |
| D    | A/B + Snippet + Graphic    | Generate variants, snippet and thumbnail             | Three HTTP modules: **POST** `/variants`, `/snippet`, `/graphic` |
| E    | Store Results              | Save generated items (variants, graphics)             | Supabase: Update Row                                             |
| F    | Upload                     | Publish content via uploader                         | HTTP module: **POST** `/hook_uploader`                           |
| G    | Insight Record             | Create summary in Notion                             | HTTP module: **POST** `/auto_insight`                            |
| H    | Slack Notification         | Send success or failure notice                       | Slack module or **POST** `/webhook`                              |

## Example Scenario A: Google Form Trigger

1. Create a **Webhook** module in Make.com and link it to your Google Form submission or Zapier event.
2. Add an **HTTP** module configured to `POST /format` using your `PIPELINE_API_URL`.
3. Insert a row in Supabase with the initial form data.
4. Chain three **HTTP** modules to call `/variants`, `/snippet` and `/graphic` sequentially. Use a short delay between calls if needed.
5. Update the Supabase row with the returned variants and any thumbnails.
6. **POST** to `/hook_uploader` to distribute the content across your channels.
7. **POST** to `/auto_insight` to store the Notion summary.
8. Send a notification to Slack and update the Supabase status once the workflow completes.

## Example Scenario B: Re-running Variants from Slack

1. Set up a Slack command (e.g., `/reab 105`) that hits your Webhook module with the content ID.
2. Use the **HTTP** module to call `/variants` for the given ID and store the new variants back in Supabase.
3. Notify the user in Slack once the process finishes.

## Required Environment Variables

| Key                  | Description                                |
|----------------------|--------------------------------------------|
| `PIPELINE_API_URL`   | Base URL for all pipeline API calls        |
| `SUPABASE_PROJECT_URL` | Supabase project URL                      |
| `SUPABASE_ANON_KEY`  | Supabase auth token                        |
| `NOTION_TOKEN`       | Token for creating Notion insights         |
| `SLACK_WEBHOOK_URL`  | Slack webhook for failure or success alerts|

Configure these variables in the **Make** scenario settings or within the HTTP module headers. When calling your API endpoints, include `Authorization: Bearer YOUR_OPENAI_API_KEY` where required.

## Quick Start Checklist

- [ ] Install the Webhook module in your Make.com account.
- [ ] Configure HTTP modules with correct headers and authorization.
- [ ] Set up Supabase, Notion, and Slack connections in Make.
- [ ] Run a single test scenario to verify that the pipeline completes without errors.

Once the scenario is working, you can expand or modify the flow to suit other triggers such as Slack commands or database updates.

