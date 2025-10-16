### Running the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MateuszGrabarczyk/mindpal-task.git
   cd mindpal
   ```

2. **Create .env file based on .env.example**

3. **Start the application:**

   ```bash
   docker compose up -d
   ```

   This command will:

   - Start PostgreSQL database
   - Build and run the FastAPI application
   - Run database migrations automatically

4. **Access the application:**

   - API: http://localhost:8000
   - Interactive API Documentation: http://localhost:8000/docs

5. **Running tests**

   It can be done directly in the container:

   ```bash
   pytest
   ```
