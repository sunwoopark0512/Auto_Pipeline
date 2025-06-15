# Auto Pipeline

This repository contains scripts to collect trending keywords from Google Trends and Twitter, generate marketing hooks using OpenAI, and upload results to Notion.

## Environment Variables

The keyword filtering thresholds can be customized via environment variables. Defaults are shown below:

```bash
GOOGLE_TRENDS_MIN_SCORE=60
GOOGLE_TRENDS_MIN_GROWTH=1.3
TWITTER_MIN_MENTIONS=30
TWITTER_MIN_TOP_RETWEET=50
MIN_CPC=1000
```

Create a `.env` file or export these variables to adjust the filtering behavior.
