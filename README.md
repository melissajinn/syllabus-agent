# Syllabus Agent

An intelligent course assistant powered by LangChain and LangGraph that helps students quickly find information from course syllabi and websites using natural language queries.

## Overview

Syllabus Agent uses LLM technology to answer questions about course policies, assignments, deadlines, and other syllabus information by processing PDF documents and course websites. Instead of manually searching through lengthy syllabi, students can ask natural language questions and get accurate answers instantly.

## Features

- **Multi-format Input**: Accepts both PDF syllabi and course website URLs
- **Natural Language Querying**: Ask questions in plain English about course content
- **Context-Aware Responses**: Uses Retrieval-Augmented Generation (RAG) to provide accurate answers
- **Stateful Conversations**: Maintains conversation history for follow-up questions
- **FastAPI Backend**: RESTful API for integration with web frontends
- **CLI Interface**: Command-line tool for quick queries
- **PDF Upload Support**: Web-based PDF file upload handling

## Technologies Used

- **LangGraph**: State machine framework for building complex LLM workflows
- **LangChain**: LLM application framework with OpenAI integration
- **OpenAI GPT-4o-mini**: Language model for question answering
- **FastAPI**: Modern Python web framework for the REST API
- **Python 3.x**: Core programming language
- **BeautifulSoup4**: Web scraping for course websites
- **PyPDF2/pdfplumber**: PDF text extraction

## Architecture

The agent uses a stateful graph-based architecture with three main nodes:
- **Assistant Node**: Handles question answering using LLM
- **PDF Node**: Processes and loads PDF syllabus files
- **Web Node**: Scrapes and loads course website content

The system maintains conversation state including message history, data type (PDF/web), and loaded content.

## Installation

```bash
# Clone the repository
git clone https://github.com/melissajinn/syllabus-agent.git
cd syllabus-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OpenAI API key to .env
```

## Usage

### CLI Interface

```bash
# Start the interactive CLI
python agent.py

# Example interaction:
> pdf /path/to/syllabus.pdf
Agent: Loaded syllabus.

> When is the final exam?
Agent: The final exam is on December 15th at 2:00 PM. (Source: "Final Exam: Dec 15, 2:00-4:00 PM")

> web https://course-website.edu
Agent: Loaded website.

> What's the late policy?
Agent: Late submissions receive a 10% penalty per day...
```

### API Server

```bash
# Start the FastAPI server
uvicorn app:app --reload

# The API will be available at http://localhost:8000
```

**API Endpoints:**

- `POST /upload-pdf`: Upload a PDF syllabus file
  ```bash
  curl -X POST -F "file=@syllabus.pdf" http://localhost:8000/upload-pdf
  ```

- `POST /chat`: Send a question to the agent
  ```bash
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "When is the midterm?"}'
  ```

- `POST /reset`: Clear conversation history
  ```bash
  curl -X POST http://localhost:8000/reset
  ```

## Example Queries

```
"When is the final exam?"
"What's the late submission policy?"
"How much is the midterm worth?"
"What topics are covered in Week 5?"
"Is attendance mandatory?"
"What are the office hours?"
"How do I submit assignments?"
```

## How It Works

1. **Document Loading**: 
   - PDFs are processed through `pdf_load.py` to extract text
   - Websites are scraped via `coursewebsite.py` for relevant content

2. **State Management**: 
   - LangGraph maintains conversation state with message history
   - Loaded content is stored in state for context-aware responses

3. **Intelligent Routing**: 
   - Classifier function routes inputs to appropriate graph nodes (PDF/Web/Assistant)
   - Conditional edges enable dynamic workflow based on user input

4. **Response Generation**: 
   - GPT-4o-mini generates answers using only the loaded content
   - System prompt enforces sourced responses with evidence

## Project Structure

```
syllabus-agent/
├── agent.py              # Main CLI application with LangGraph workflow
├── app.py                # FastAPI backend server
├── pdf_load.py           # PDF text extraction utilities
├── coursewebsite.py      # Web scraping for course sites
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (API keys)
```

## Project Motivation

Built to streamline the process of navigating course materials at Carnegie Mellon University. With multiple classes each having various syllabi and scattered information across various sources, this tool helps students quickly access important information without manually searching through lengty.

## Future Improvements

- [ ] Support for simultaneous syllabi uploads (comparing courses)
- [ ] Vector database integration for larger documents
- [ ] React frontend for better user experience
- [ ] Integration with Canvas
- [ ] Slack/Discord bot interface
- [ ] Export significant dates to Google Calendar
- [ ] Support for additional file formats (DOCX, HTML, etc)
- [ ] Multi-user support
- [ ] Search across multiple course materials

## Technical Highlights

- **Stateful Agent Design**: Uses LangGraph's state management for context retention
- **Modular Architecture**: Separate nodes for different data sources enable easy future project extension
- **RESTful API**: FastAPI backend allows for frontend integration and scalability
- **Error Handling**: Graceful handling of missing data with user prompts
- **Source Attribution**: Responses include quotes from source material for verification

## Development

```bash
# Run in development mode with auto-reload
uvicorn app:app --reload

# Run CLI for testing
python agent.py
```

## License

MIT License - see LICENSE file for details

## Contact

Melissa Jin - mjin2@andrew.cmu.edu

Project Link: [https://github.com/melissajinn/syllabus-agent](https://github.com/melissajinn/syllabus-agent)

---

*Note: This project is for educational purposes. Always verify important course information with official sources and instructors.*
