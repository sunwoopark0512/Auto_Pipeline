# Auto Pipeline

This project contains scripts to generate marketing hooks and upload them to Notion.  
Environment variables are required for API keys and database IDs.

## Setup
1. Copy `.env.example` to `.env`.
2. Fill in your API keys, Notion database IDs and other settings in the `.env` file.
3. Install Python dependencies listed in `requirements.txt` (if provided).
4. Run the scripts as needed, for example:
   ```bash
   python hook_generator.py
   ```

The `.env` file is ignored by Git, so your secrets will stay local.
