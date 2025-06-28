# Multiplayer Gaming Platform

This project is an online gaming platform that allows two players to start a match and track their health during the game. It also includes features for tracking player statistics, match history, and a leaderboard.

## Project Structure

The project is structured into two main parts: `app` (backend) and `frontend` (web interface).

### `app/` (Backend)

This directory contains the Flask backend application. Key components include:

- `db/`: Contains modules for interacting with different databases (MongoDB, PostgreSQL, Redis).
- `routes/`: Defines the API endpoints for game logic, player management, and data retrieval. Specifically, `player.py` handles starting matches, updating health, ending matches, and retrieving leaderboard data.
- `docker-compose.yml`: Defines the services for the application, including the Flask app, Redis, PostgreSQL, and MongoDB.
- `main.py`: The main entry point for the Flask application.

### `frontend/` (Web Interface)

This directory contains the static files for the web-based user interface:

- `index.html`: The main page for starting a new match, where players can input their names.
- `leaderboard.html`: Displays the game leaderboard.
- `match.html`: Likely the page where the actual game takes place and health is updated.
- `monitor.html`: A page for monitoring live game data.
- `script.js`: JavaScript code for handling frontend interactions and API calls.
- `style.css`: CSS for styling the web interface.

## How to Run the Project

To run this project, you will need Docker and Docker Compose installed. Navigate to the `app` directory and run:

```bash
docker-compose up --build
```

This will start the Flask backend, Redis, PostgreSQL, and MongoDB services. The frontend can be accessed by opening `frontend/index.html` in your web browser.

## Adding a Friend for Collaboration

Based on the current project structure and code, there isn't an explicit 


feature for adding friends or managing a friend list within the application itself. The `start_match` functionality in `player.py` takes two player names as input, implying that players are identified by their names for the purpose of a match.

If you want to collaborate with your friend on the *development* of this project, you would typically do so through a version control system like Git and a platform like GitHub. Here's a general guide:

1.  **Create a GitHub Repository:** If this project is not already on GitHub, create a new repository on GitHub. You can then push this project's code to that repository.

2.  **Invite Collaborator:** On GitHub, navigate to your repository's settings. Look for a section like 'Manage access' or 'Collaborators and teams'. From there, you can invite your friend using their GitHub username or email address.

3.  **Friend Accepts Invitation:** Your friend will receive an invitation to collaborate on the repository. Once they accept, they will have access to the codebase.

4.  **Clone the Repository:** Your friend can then clone the repository to their local machine using `git clone [repository_url]`.

5.  **Work on Branches:** Both of you should work on separate branches to avoid conflicts. For example, you might work on a `feature/my-feature` branch, and your friend on `feature/friends-feature`.

6.  **Pull Requests:** When a feature is complete, create a Pull Request (PR) on GitHub to merge your branch into the `main` (or `master`) branch. Your friend can review your code, and vice-versa.

7.  **Stay Updated:** Regularly pull changes from the `main` branch to keep your local repository updated: `git pull origin main`.

This process allows you and your friend to work on the same codebase, track changes, and merge your contributions effectively.



## Running the Backend and Frontend Locally

This project uses Docker Compose to manage its backend services (Flask application, Redis, PostgreSQL, and MongoDB). The frontend is a set of static HTML, CSS, and JavaScript files.

### 1. Running the Backend (Flask App, Databases)

To start all the backend services, navigate to the `app` directory within the extracted project folder and run the following command:

```bash
cd /home/ubuntu/project/online-gaming-platform/app
docker-compose up --build
```

- `cd /home/ubuntu/project/online-gaming-platform/app`: This command changes your current directory to the `app` folder where the `docker-compose.yml` file is located.
- `docker-compose up --build`: This command reads the `docker-compose.yml` file, builds the necessary Docker images (if they haven't been built before or if there are changes), and starts all the defined services. You will see logs from Flask, Redis, PostgreSQL, and MongoDB in your terminal.

Ensure you have Docker and Docker Compose installed on your system before running this command.

### 2. Accessing the Frontend

The frontend of the application is a collection of static files. You can access it directly through your web browser.

- **Open `index.html`:** Navigate to the `frontend` directory within the extracted project folder (e.g., `/home/ubuntu/project/online-gaming-platform/frontend/`). You can then open the `index.html` file directly in your web browser. For example, you can drag and drop the `index.html` file into your browser, or use your file explorer to open it with your preferred browser.

### 3. How Backend and Frontend Interact

The frontend (HTML, CSS, JavaScript) interacts with the backend (Flask application) through API calls. When you open `index.html` in your browser, the `script.js` file makes HTTP requests to the Flask backend (which is running inside a Docker container) to perform actions like:

- **Starting a Match:** When you fill in player names and click "Start Match" on `index.html`, `script.js` sends a request to the `/start_match` endpoint of the Flask backend. The backend then uses Redis to store match state and returns a `match_id`.
- **Updating Health/Game State:** During a match (likely on `match.html`, though not fully explored), the frontend would send requests to endpoints like `/update_health` to reflect game progress.
- **Retrieving Data:** Pages like `leaderboard.html` and `monitor.html` make requests to backend endpoints (e.g., `/leaderboard`, `/monitor`) to fetch real-time game data, player statistics, and match history from Redis, PostgreSQL, and MongoDB.

Essentially, the frontend provides the user interface, and the backend handles all the game logic, data storage, and retrieval. The `docker-compose up --build` command ensures that all the necessary backend services are running and accessible for the frontend to communicate with them.

