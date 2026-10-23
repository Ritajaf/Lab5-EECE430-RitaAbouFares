# Inventory AI Agent - Assignment 5

Docker setup for the existing Django inventory AI agent.

## Build and run locally

1. Install and start Docker Desktop with Linux containers enabled.
2. Open a terminal in this `inventory` folder, alongside `manage.py` and `Dockerfile`.
3. Create `.env` from `.env.example` if it does not already exist. Set a valid key:

   ```text
   GEMINI_API_KEY=your_actual_gemini_api_key
   ```

4. Build the image and run the container:

   ```console
   docker build -t inventory-agent .
   docker run -d --name inventory-agent -p 8000:8000 --env-file .env inventory-agent
   ```

5. Open http://localhost:8000/ and use the inventory chat.

The container applies the existing Django migrations before starting the server.
It creates its own empty SQLite database. Your local database, virtual
environment, and `.env` are excluded from the image and Git commits. The Gemini
key is supplied only when the container runs.

To view startup logs or stop the container:

```console
docker logs inventory-agent
docker stop inventory-agent
```

## GitHub steps to complete yourself

1. Push the contents of this `inventory` folder to a new GitHub repository.
2. In that repository, open **Settings > Collaborators > Add people**, enter
   `am38@aub.edu.lb`, and send the collaborator invitation.
3. To build and run the application from GitHub, clone the new repository into
   a different folder and enter it:

   ```console
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git inventory-agent-from-github
   cd inventory-agent-from-github
   ```

4. Copy `.env.example` to `.env`, set your valid Gemini API key, then build and
   run a separate image and container from the cloned files:

   ```console
   docker build -t inventory-agent-from-github .
   docker run -d --name inventory-agent-from-github -p 8001:8000 --env-file .env inventory-agent-from-github
   ```

5. Open http://localhost:8001/ to verify the application built from GitHub.
