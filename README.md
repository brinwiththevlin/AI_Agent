# AI Agent 🤖

[![Build Status](https://github.com/brinwiththevlin/AI_Agent/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/brinwiththevlin/AI_Agent/actions/workflows/deploy-docs.yml)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://brinwiththevlin.github.io/AI_Agent/)
[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue)](https://pypi.org/project/AI-Agent/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated AI agent designed to interact with your local file system, providing intelligent information retrieval and executing complex tasks through natural language commands.

---

## 🌟 Features

- **Natural Language Understanding**: Interact with your files using everyday language.
- **File System Interaction**: Ask for file details, summaries, or contents without leaving the terminal.
- **Calculator Tool**: Perform calculations directly within the agent's environment.
- **Extensible Functionality**: Built with a modular structure that allows for easy addition of new tools and capabilities.

---

## 🛠️ Installation

To get this project up and running on your local machine, follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/brinwiththevlin/AI_Agent.git](https://github.com/brinwiththevlin/AI_Agent.git)
    cd AI_Agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the project in editable mode:**
    This command installs the project and its core dependencies as defined in `pyproject.toml`.
    ```bash
    pip install -e .
    ```

4.  **(Optional) Install dependencies for documentation:**
    If you plan to build the documentation locally, install the optional "docs" dependencies.
    ```bash
    pip install -e ".[docs]"
    ```
    *(Note: This requires defining `[project.optional-dependencies]` in your `pyproject.toml` file.)*

5.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your API keys or other necessary configurations.
    ```
    OPENAI_API_KEY="your_api_key_here"
    ```

---

## 🚀 Usage

To start the agent, run the `main.py` script from the root directory:

```bash
python main.py
```

Once started, you can interact with the agent by typing your commands.

**Examples:**

-   `"What is the file size of lorum_ipsum.txt?"`
-   `"Calculate 12 * 5 + 7"`
-   `"Summarize the file named 'agent.py'"`

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
