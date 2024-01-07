# CProjectG6
## Tourism ChatBot
This repository is designed to create a chat bot for Out&About. Out&About is fictional company created to help travelers find the best attractions in Lisbon, according to their interests. The app was created using streamlit. For more information on streamlit click here: [Streamlit Docs](https://docs.streamlit.io/).

## Table of Contents
- [Before Starting](#before-starting)
- [Setup](#project-setup)
- [App](#app)
- [Authors](#authors)


## Before Starting

🔑 OpenAI API Key.
If you don't already have an OpenAI Key, it's essential to create one at <https://platform.openai.com/api-keys>. This key is crucial for accessing OpenAI's services.
<br>

> Remember, it's vital to save this key securely and avoid sharing it because its use may incur costs.</font>

⚠️ It's a best practice to store your API key in a file named `.env`. This file should not be tracked by Git (add `.env` to `.gitignore` file), ensuring it remains private and inaccessible to others. Only you, within your local repository, should have access to this sensitive information.

## Project Setup
### Step 1: `.env` and `OpenAI API Key`

📁 Create a file named `.env` within the root folder of this project. Inside this file, define a variable name and assign your OpenAI API Key to this variable, following this structure:
<br>

```text
OPENAI_API_KEY=sk-xiu...
```
> 📝**Note**: Ensure that the variable in the `.env` file is named `OPENAI_API_KEY`, as demonstrated in the code above. This specific name aligns with the `Settings` class in the `util.py` file, which is a specialization of the `BaseSettings` from the `pydantic-settings` package.

After this, you need to activate it and install the packages listed in requirements.txt. Here are the steps:

### Step 2: Create the Python environment by using this command

```bash
python -m venv env
```

> 📝**Note**: `env` is the standard name for a Python environment.

### Step 3: Activate the Python environment

🖥️ To activate the Python environment, the process differs between Windows and MacOS/Linux.

#### Environment activation in MacOS/Linux

For MacOS/Linux, use the following command to activate the environment:
<br>

```bash
source env/bin/activate
```
#### Environment activation in Windows

For Windows, the activation process differs.
<br>

```bash
cd env\Scripts
activate

# or

env\Scripts\activate
```

In Windows, permission issues might arise when activating the Python environment. If you encounter this problem, in PowerShell or a VS Code terminal, you can resolve it by running the following command:
<br>

```bash
Set-ExecutionPolicy RemoteSigned
```

> When the virtual environment is activated, you will see the environment name in the command prompt, indicating that you are now working within the virtual environment.

### Step 3: recreate the Python environment

⚠️ **Attention**: </font>before running the command `pip install -r requirements.txt`, ensure that you have activated your local Python environment (`env`).
<br>

```bash
pip install -r requirements.txt
```

🗒️ The requirements.txt file is essential within a Python environment. Running pip freeze captures a comprehensive list of installed packages and their respective versions. It's crucial to update the requirements.txt whenever you install a new package. You can do this by executing the following command:
<br>

```bash
pip freeze > requirements.txt
```

This command ensures that the `requirements.txt` file remains up to date with the latest package installations and versions in your environment.

## App

🌐 To view the app on your browser open the terminal and run:
```bash
streamlit run "Out&AboutApp.py"
```
> ⏳Please be aware that running the app and asking a question to the chatbot might take a few minutes. Don't close your tab or the terminal.

## Authors
👤The people that contributed to this repository were:
- [Ana Farinha](https://github.com/AnaBFarinha) <br>
- [Ana Reis](https://github.com/ceiareis) <br>
- [Beatriz Barreto](https://github.com/beat-b) <br>
- [Mariana Neto](https://github.com/MGN19) <br>
