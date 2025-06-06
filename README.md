# TR Squad Finder POC
POC of application powered by Google Gemini 2.5 Flash with Google search grounding, which can return accurate squad information for Premier League teams upon a natural language request.
Specifically, the query should return the following info of each player on the requested squad:
- First name
- Surname
- Date of Birth
- Playing position.

# Example of the user query:
 - ```Please list all the current senior squad members for the Manchester United men's team. ```

# Prerequisites for local development environment
 - Python 3.12
 - Pipenv - https://pipenv.pypa.io/en/latest/installation.html

# How to run the project locally
 - Clone the repository
## API
 - Go to API folder `cd API`
 - Run `pip install pipenv` to install pipenv
 - Run `pipenv install --dev` to install all dependencies for a project (including dev)
 - Run `pipenv shell` to activate the virtual environment
 - Run `pre-commit install` to install pre-commit hooks
 - Copy the `app/.env.example` file to `app/.env` by `cp app/.env.example app/.env` and update the values as needed
 - Run `cd ./app && fastapi dev` to run the FastAPI app in development mode
```
  ──── FastAPI CLI - Development mode ───────────╮
 │                                               │
 │  Serving at: http://127.0.0.1:8000            │
 │                                               │
 │  API docs: http://127.0.0.1:8000/docs
```


## UI
- Open new tab in terminal
- Go to UI folder `cd UI`
- Copy the `.env.example` file to `.env` by `cp .env.example .env` and update the values as needed
- Run `npm run install` to install the dependencies
- Run `npm run dev` to run the development server
- Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
