# YouTube Video Chatbot

A simple AI-powered chatbot that lets you ask questions about a YouTube video and get answers based on its transcript. Instead of watching the entire video again, you can enter your questions and quickly find the information you need.

## Features

- Extracts transcripts from YouTube videos.
- Splits transcripts into smaller chunks for processing.
- Generates embeddings and stores them in a FAISS vector database.
- Retrieves relevant transcript sections using similarity search.
- Uses an OpenRouter language model to generate answers based on the retrieved context.
- Provides an interactive interface built with Streamlit.

## Tech Stack

- **Python** — Core programming language
- **Streamlit** — Web interface
- **LangChain** — Text processing and retrieval pipeline
- **FAISS** — Vector storage and similarity search
- **OpenRouter** — Access to embedding and chat models
- **YouTube Transcript API** — Transcript extraction

## How It Works

1. Enter a YouTube video ID.
2. Click **Save** to fetch the transcript.
3. The transcript is split into chunks and converted into embeddings.
4. The embeddings are stored in FAISS for efficient similarity search.
5. Enter a question about the video.
6. The chatbot retrieves relevant transcript sections and generates an answer using the language model.

The chatbot is designed to answer questions using the available transcript context. If the context does not contain enough information, it is instructed to say that it does not know.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

Replace the placeholders with your actual GitHub repository URL and project folder name.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

You can obtain an API key from [OpenRouter](https://openrouter.ai/).

Keep your API key private. Do not upload your `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Replace `app.py` with your Python filename if it is different. Streamlit will provide a local URL where you can access the chatbot.

## Project Structure

```text
youtube-chatbot/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `.env` file is used locally and should be excluded from version control through `.gitignore`.

## Requirements

- Python 3.10 or a compatible Python version for your installed dependencies
- An OpenRouter API key
- A YouTube video with an accessible transcript
- An internet connection

## Limitations

- The chatbot depends on transcript availability.
- Videos without accessible transcripts cannot be processed by the current implementation.
- Answers depend on the transcript content and the quality of retrieval.
- Model and embedding availability may depend on OpenRouter's current service offerings.

## Future Improvements

- Add support for multiple languages.
- Display relevant transcript excerpts with timestamps.
- Improve error handling and loading indicators.
- Allow users to process multiple videos.
- Add chat history and a more conversational interface.

## Author

Developed as a project to explore LangChain, vector databases, retrieval-augmented generation (RAG), and large language models.

If you find this project useful, feel free to star the repository or suggest improvements.
