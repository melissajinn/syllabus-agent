Syllabus Agent Requirements

## Problem
Students need to quickly find due dates, policies, and other logistics in long syllabus PDFs.

## Overall Goals
- Parse a syllabus (PDF)
- Answer questions accurately about due dates, policies, and exams

## Core
- PDF text extraction with page
- Tool routing using LangGraph

## Other Requirements
- Prioritize accuracy
- No hallucinations
- Clear citation of page source

## Example Questions
- Asking “What is the late policy?” returns an accurate answer with citation
- Asking “When is HW1 due?” returns correct date or "not found"
- Asking unrelated question returns “not found in syllabus”



If user says “load this pdf …” → call PDF tool, store the text in state

If user says “load course website …” → call website tool, store text in state

If user asks a question and text exists → answer using stored text

If user asks a question but no text loaded → ask them to provide PDF path or URL