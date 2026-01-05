# Syllabus Assistant

An intelligent AI-powered chatbot that helps students quickly find information from course syllabi and websites using natural language queries.

## Overview

Syllabus Assistant uses LLM technology to answer questions about course policies, assignments, deadlines, and other syllabus information by processing PDF documents and course websites. Instead of manually searching through lengthy syllabi, students can ask natural language questions and get accurate answers instantly.

## Features

- **Multi-format Input**: Accepts both PDF syllabi and course website URLs
- **Natural Language Querying**: Ask questions in plain English about course content
- **Interactive Web Interface**: Modern React-based chat UI with real-time messaging
- **PDF Upload Support**: Drag-and-drop file upload directly from the browser
- **Context-Aware Responses**: Uses LLM to provide accurate answers based on loaded content
- **Stateful Conversations**: Maintains conversation history for follow-up questions
- **RESTful API**: FastAPI backend with clean API endpoints
- **CLI Interface**: Command-line tool for quick queries

## Technologies Used

### Backend
- **LangGraph**: State machine framework for building complex LLM workflows
- **LangChain**: LLM application framework with OpenAI integration
- **OpenAI GPT-4o-mini**: Language model for question answering
- **FastAPI**: Modern Python web framework for the REST API
- **Python 3.x**: Core programming language
- **BeautifulSoup4**: Web scraping for course websites
- **PyPDF2/pdfplumber**: PDF text extraction

### Frontend
- **React**: Modern JavaScript library for building user interfaces
- **JavaScript (ES6+)**: Frontend programming language
- **CSS3**: Styling and responsive design
- **Fetch API**: HTTP client for backend communication

## Architecture

The application uses a full-stack architecture:

**Backend**: Stateful graph-based agent with three main nodes:
- **Assistant Node**: Handles question answering using LLM
- **PDF Node**: Processes and loads PDF syllabus files
- **Web Node**: Scrapes and loads course website content

**Frontend**: Single-page React application with:
- Real-time chat interface
- File upload component
- Message history display
- Loading states and error handling

The system maintains conversation state including message history, data type (PDF/web), and loaded content.

## Installation
```bash
# Clone the repository
git clone https://github.com/melissajinn/syllabus-agent.git
cd syllabus-agent

# Install backend dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OpenAI API key to .env

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Usage

### Web Application (Recommended)

**Start the backend:**
```bash
uvicorn src.app:app --reload
# Backend runs on http://localhost:8000
```

**Start the frontend (in a new terminal):**
```bash
cd frontend
npm start
# Frontend opens at http://localhost:3000
```

**Using the web interface:**
1. Click "📎 Upload PDF" to upload a syllabus file, or
2. Type `web https://course-website.edu` to load a course website
3. Ask questions about the loaded content
4. Click "Reset" to start a new conversation

### CLI Interface
```bash
# Start the interactive CLI
python src/agent.py

# Example interaction:
> pdf /path/to/syllabus.pdf
Agent: Loaded syllabus.

> When is the final exam?
Agent: The final exam is on December 15th at 2:00 PM.

> web https://course-website.edu
Agent: Loaded website.

> What's the late policy?
Agent: Late submissions receive a 10% penalty per day...
```

### API Server
```bash
# Start the FastAPI server
uvicorn src.app:app --reload

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
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
   - PDFs are uploaded through the web interface or processed locally
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

5. **Frontend Communication**:
   - React frontend makes HTTP requests to FastAPI backend
   - Real-time updates display agent responses in chat interface

## Project Structure
```
syllabus-agent/
├── src/
│   ├── agent.py              # Main CLI application with LangGraph workflow
│   ├── app.py                # FastAPI backend server
│   ├── pdf_load.py           # PDF text extraction utilities
│   └── coursewebsite.py      # Web scraping for course sites
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   └── App.css           # Styling
│   ├── public/               # Static assets
│   └── package.json          # Frontend dependencies
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (API keys)
```

## Project Motivation

Built to streamline the process of navigating course materials at Carnegie Mellon University. With multiple classes each having lengthy syllabi and scattered information across various sources, this tool helps students quickly access important information without manually searching through documents.

## Future Improvements

- [ ] Support for multiple simultaneous syllabi (comparing courses)
- [ ] Vector database integration for larger documents
- [ ] User authentication and personalized sessions
- [ ] Integration with Canvas LMS
- [ ] Slack/Discord bot interface
- [ ] Export important dates to Google Calendar
- [ ] Support for additional file formats (DOCX, HTML, etc)
- [ ] Multi-user support with session management
- [ ] Search across multiple course materials
- [ ] Mobile-responsive design improvements

## Technical Highlights

- **Full-Stack Architecture**: React frontend with FastAPI backend
- **Stateful Agent Design**: Uses LangGraph's state management for context retention
- **Modular Architecture**: Separate nodes for different data sources enable easy extension
- **RESTful API**: Clean API design with CORS support for frontend integration
- **Modern UI**: Responsive chat interface with real-time updates
- **Error Handling**: Graceful handling of missing data with user prompts
- **File Upload**: Seamless PDF processing with temporary file handling

## Development
```bash
# Run backend in development mode with auto-reload
uvicorn src.app:app --reload

# Run frontend in development mode (in separate terminal)
cd frontend
npm start

# Run CLI for testing
python src/agent.py
```

## License

MIT License - see LICENSE file for details

## Contact

Melissa Jin - mjin2@andrew.cmu.edu

Project Link: [https://github.com/melissajinn/syllabus-agent](https://github.com/melissajinn/syllabus-agent)

---

*Note: This project is for educational purposes. Always verify important course information with official sources and instructors.*
