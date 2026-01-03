# AI Chatbot for HR & Project Data

A full-stack AI-powered chatbot built with FastAPI, MongoDB, and OpenAI, designed to answer queries about employees and projects using internal company data. The project supports both local and Dockerized deployment.

---

## Features

- **Conversational AI**: Uses OpenAI's GPT models for natural language understanding and tool-calling.
- **HR & Project Lookup**: Answers questions about employees and projects from internal databases.
- **Session Memory**: Maintains chat history for each session.
- **REST API**: Exposes endpoints for chat and session history.
- **Docker Support**: Easily deployable with Docker Compose.
- **Extensible**: Modular codebase for adding new tools or data sources.

---

## Directory Structure

```
InternProject/
├── app/
│   ├── chatbot/           # Chatbot logic, agent, prompts, tool schemas
│   ├── data/              # HR and project data (JSON)
│   ├── db/                # MongoDB connection and seed scripts
│   ├── services/          # OpenAI API integration
│   ├── utils/             # Utilities (chat memory, error handling, models)
│   └── main.py            # FastAPI app entrypoint
├── docker/
│   ├── Dockerfile         # Docker build for app
│   └── docker-compose.yml # Multi-container setup (app + MongoDB)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (see below)
└── README.md              # Project documentation
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/vaishnavi3103/AI-chatbot.git
cd AI-chatbot
```

### 2. Environment Variables

Create a `.env` file in the project root (or use the provided sample):

```
OPENAI_API_KEY=your-openai-api-key
MONGO_URI=mongodb://mongo:27017
```

- `OPENAI_API_KEY`: Your OpenAI API key (required for chatbot responses).
- `MONGO_URI`: MongoDB connection string. Use `mongodb://mongo:27017` for Docker, or `mongodb://localhost:27017` for local development.

---

## Running the Project

### Option 1: Docker Compose (Recommended)

Build and start all services (app + MongoDB):

```bash
docker compose -f docker/docker-compose.yml up --build
```

- The FastAPI app will be available at [http://localhost:8000](http://localhost:8000)
- MongoDB will be available at `localhost:27017` (inside Docker network as `mongo:27017`)

### Option 2: Local Development

1. **Install dependencies** (Python 3.10+ recommended):

    ```bash
    pip install -r requirements.txt
    ```

2. **Start MongoDB** (locally or via Docker):

    ```bash
    # Local MongoDB
    mongod --dbpath ./mongo_data

    # OR via Docker
    docker run -d -p 27017:27017 --name mongo-db mongo:7
    ```

3. **Seed the HR and Project Data** (if not done automatically):

    ```bash
    python -c "from app.db.seed_hr import seed_hr; seed_hr()"
    python -c "from app.db.seed_projects import seed_projects; seed_projects()"
    ```

4. **Run the FastAPI app**:

    ```bash
    uvicorn app.main:app --reload
    ```

---

## API Endpoints

### `POST /chat`

- **Description**: Send a message to the chatbot.
- **Request Body**:
    ```json
    {
      "message": "Tell me about employee ID 44-7812493",
      "session_id": "optional-session-id"
    }
    ```
- **Response**:
    ```json
    {
      "response": "Employee details ...",
      "session_id": "..."
    }
    ```

### `GET /history/{session_id}`

- **Description**: Retrieve chat history for a session.

---

## Troubleshooting

- **Internal Server Error (500)**: Check that your `.env` file is correct and MongoDB is running and seeded.
- **OpenAI API Key Error**: Ensure `OPENAI_API_KEY` is set in `.env` and loaded before the app starts.
- **MongoDB Connection Issues**: Use the correct `MONGO_URI` for your environment (Docker vs local).
- **Data Not Found**: Reseed the database using the provided seed scripts.

---

## Customization

- **Add new tools**: Edit `app/chatbot/tools.py` and extend the agent logic in `app/chatbot/agent.py`.
- **Change models**: Update `MODEL_NAME` in `app/services/open_ai_service.py`.

---

## License

This project is for internal/demo use. For production or commercial use, please review and update licensing as needed.

---

## Contributing

Pull requests and suggestions are welcome! Please open an issue or submit a PR on GitHub.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [OpenAI](https://openai.com/)
- [Docker](https://www.docker.com/)
