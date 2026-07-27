# 🤖 Chatbot SaaS

A multi-tenant AI chatbot platform. Companies sign up, create a custom AI chatbot with their own instructions (system prompt), then embed it on their website with a single script tag — like Intercom or Tawk.to, but self-built.

**Live demo:** https://chatbot-frontend-iwnp.onrender.com

## Features
- 🔐 User authentication (register/login, JWT via secure headers)
- 🏢 Multi-tenant companies — each with an isolated AI personality (system prompt)
- 💬 Embeddable chat widget — works on any external website
- 🧪 Live widget preview before going live
- 📝 Conversation history stored per company/user
- 🔒 Ownership checks — users can only access their own data
- 🐳 Fully Dockerized, deployed with CI/CD

## Tech Stack
| Layer      | Tech |
|------------|------|
| Backend    | FastAPI, PostgreSQL, SQLAlchemy, JWT |
| AI         | Groq (llama-3.3-70b-versatile) |
| Frontend   | HTML, vanilla JavaScript |
| Infra      | Docker, docker-compose, GitHub Actions CI/CD |
| Hosting    | Render.com |

## Architecture
```
Customer's Website
      │
      ▼
  widget.js  ──────►  /api/chat/public-chat  ──────►  Groq AI
                            │
                            ▼
                       PostgreSQL
                    (companies, users,
                     conversations, messages)
```

## How it works
1. A business registers and logs in
2. They create a "company" — giving their bot a name and instructions (e.g. *"You are a support agent for a jewelry shop"*)
3. They preview the bot live, then copy an embed snippet:
   ```html
   <script src="https://chatbot-frontend-iwnp.onrender.com/widget.js" data-company-id="1"></script>
   ```
4. They paste that snippet into their own website — the chat widget appears instantly

## Security
- JWT sent via `Authorization: Bearer <token>` header (not URL params)
- Passwords hashed, minimum 8 characters
- Login errors don't reveal whether an email is registered
- Users can only read/access conversations they own

## Running locally
```bash
git clone https://github.com/islem14623/chatbot-saas.git
cd chatbot-saas
# create backend/.env with GROQ_API_KEY, JWT_SECRET_KEY, DATABASE_URL
docker-compose up --build
```

## Author
Built by Islem — DevOps/Cloud Engineer in progress.
