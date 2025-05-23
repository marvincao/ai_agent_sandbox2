# README

This is a sample project demonstrating how to use the [Agno](https://docs.agno.com) library to build multi-agent AI applications.

---

## Prerequisites

- Ensure Python is installed on your system.  
  Example paths (adjust based on your setup):

  ```sh
  # location of python
  where python
  C:\Python312\python.exe

  # check python version
  python -V
  Python 3.13.2

  # location of pip
  where pip
  C:\Python312\Scripts\pip.exe

  # check pip version
  pip --version
  pip 25.1.1
  ```

- Google Gemini API Key
  To enable integration with the Google Gemini API, follow these steps:

  1. Visit [Google AI Studio](https://aistudio.google.com/apikey).  
  2. Create a new API key.  
  3. Copy the generated API key.  
  4. Update the `.env` file with your API key.

  </br>

  Example `.env` Configuration:

  ```sh
  # Copy .env_sample to .env and update the following:
  GEMINI_API_KEY=paste_your_api_key_here
  ```

---

## Install or Upgrade `uv`

`uv` is the dependency management tool used in this project. Follow these steps to install or upgrade it:

```sh
# Install or upgrade uv
pip install --upgrade uv

# Verify uv installation and version
uv --version
uv 0.7.3 (3c413f74b 2025-05-07)
```

---

## Set Up the Project Environment

Use the following commands to set up and manage the project's environment:

### Create a Virtual Environment and Install Dependencies

```sh
# Create a virtual environment and sync dependencies
uv sync --native-tls
```

### Upgrade Dependencies

```sh
# Upgrade dependencies to their latest versions
uv lock --upgrade --native-tls
```

---

## Run the applications

```sh
# change to demo folder
cd demo

# run the agents
uv run ticker_agent.py
uv run finance_agent.py
...
```

---

## Output

Outputs are saved in the `output` directory.
