@echo off
REM Grant Research Agent Docker Startup Script for Windows/Google Cloud

echo 🇨🇦 Starting Grant Research Agent for Google Cloud...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Build the Docker image
echo 🔨 Building Docker image...
docker build -t grant-research-agent .

REM Run the container
echo 🚀 Starting Grant Research Agent...
docker run -d --name grant-research-app -p 8501:8501 -e GOOGLE_CLOUD_PROJECT=%GOOGLE_CLOUD_PROJECT% grant-research-agent

REM Wait for the service to start
echo ⏳ Waiting for service to start...
timeout /t 10 >nul

REM Check if container is running
docker ps | findstr grant-research-app >nul
if %errorlevel% equ 0 (
    echo ✅ Grant Research Agent is running!
    echo 🌐 Access the app at: http://localhost:8501
    echo.
    echo 📋 Useful commands:
    echo    View logs:       docker logs -f grant-research-app
    echo    Stop container:  docker stop grant-research-app
    echo    Remove container: docker rm grant-research-app
) else (
    echo ❌ Failed to start Grant Research Agent
    echo 📋 Check logs with: docker logs grant-research-app
)

pause
