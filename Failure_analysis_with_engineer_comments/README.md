Hello Developers!


**Project Name:** Failure Analysis from engineers comments

# **Introduction**

Failure Mode Analysis is a crucial task in Natural Language Processing (NLP) that involves analyzing comments from various sources and various departments, various platforms or forums, to extract insights and failure information. This project uses OLLAMA LLAMA3.2 3B, a lightweight and efficient transformer-based language model, and Langichain framework, to develop an end-to-end comment analysis pipeline.

# **Project Overview**

Our project consists of two main components:

1.  **llama3.2** : We leverage ollama llama3.2 as our primary language model for failure analysis and text classification tasks.
2.  **Langichain** : We use Langichain to build a knowledge graph that represents entities, relationships, and concepts mentioned in the comments.

# **Getting Started**

To get started with this project:

1.  **Install dependencies** : Run `pip install -r requirements.txt` to install all required libraries.
2.  **Download OllyMai model** : Download the pre-trained OllyMai model for sentiment analysis and text classification tasks from [provide link or instructions].
3.  **Prepare Langichain dataset** : Prepare your dataset of comments by tokenizing and normalizing the text, then create a knowledge graph using Langichain.

# **Features**

Our project includes the following features:

-   Sentiment analysis: We use OllyMai to analyze sentiment in comments.
-   Text classification: We use OllyMai to classify comments into predefined categories (e.g., spam vs. non-spam).
-   Knowledge graph embedding: We leverage Langichain to build a knowledge graph that represents entities, relationships, and concepts mentioned in the comments.

# **Requirements**

To run this project, you'll need:

-   Python 3.8+ (https://www.python.org/)
-   Ollama (https://ollama.com/)
-   Langichain (https://python.langchain.com/v0.2/docs/introduction/)
-   Other dependencies listed in `requirements.txt`

# **Installation**

1.  **Install dependencies** : 
- 1. Install ollama from site (https://ollama.com/)
- 2. Open cmt promt then `ollama run llama3.2`
- 3. clone repo to local and make env `python -m venv <project_folder>` or use conda
- 4. Run `pip install -r requirements.txt` in your terminal/command prompt.

# **Usage**
- 1. preapre your soruce or comments file that has failure information as excel (.xlsx)
- 2. Change input file path in `failure_analysis.py`
- 3. run python file `python failure_analysis.py`
- 4. output will in proejct directory


# Note
- You can chage the prompt to get some more information.
