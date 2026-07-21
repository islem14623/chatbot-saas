# Chatbot SaaS

A multi-tenant AI chatbot platform. Companies can create their own AI chatbot with custom instructions, then embed it on their website using a simple script tag.

## Features
- User authentication (register/login/JWT)
- Companies can create custom AI chatbots (custom system prompt)
- Chatbot widget — embeddable on any website
- Conversation history saved in PostgreSQL
- Powered by Google Gemini AI

## Tech Stack
- Backend: FastAPI, PostgreSQL, SQLAlchemy
- Frontend: HTML, JavaScript (vanilla)
- AI: Google Gemini (gemini-2.5-flash)

## How to run
1. Set up PostgreSQL database
2. Create `.env` file with `GEMINI_API_KEY` and `JWT_SECRET_KEY`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`

## Widget embed example
\`\`\`html
<script src="http://localhost:5000/static/widget.js" data-company-id="1"></script>
\`\`\`
