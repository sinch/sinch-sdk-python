# sinch-sdk-python-snippets

Sinch Python SDK Code Snippets

This repository contains code snippets demonstrating usage of the
[Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).

## Requirements
- Python 3.9 or later
- [Poetry](https://python-poetry.org/) for dependency management
- [Sinch account](https://dashboard.sinch.com)
- [Sinch package](https://pypi.org/project/sinch/)


## Snippets execution settings
When executing a snippet, you will need to provide some information about your Sinch account (credentials, Sinch virtual phone number, ...)

These settings can be placed directly in the snippet source code, **or** you can use an environment file (`.env`). Using an environment file allows the settings to be shared and used automatically by every snippet.

### Setting Up Your Environment File

#### 1. Rename the example file

**Linux / Mac:**
```bash
cp .env.example .env
```

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

#### 2. Fill in your credentials

Open the newly created [.env](.env) file in your preferred text editor and fill in the required values (e.g., SINCH_PROJECT_ID=your_project_id).

Note: Do not share your .env file or credentials publicly.


### Install dependencies using Poetry:

```bash
poetry install
```


## Running snippets

All available code snippets are located in subdirectories, structured by feature and corresponding actions (e.g., `numbers/`, `sms/`).

To execute a specific snippet, navigate to the appropriate subdirectory and run:

```shell
python run python snippet.py
```