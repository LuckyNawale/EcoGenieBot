@echo off
echo EcoGenieBot GitHub Upload Script
echo ================================
echo.
echo Please follow these steps:
echo.
echo 1. Go to https://github.com/new
echo 2. Repository name: ecogeniebot
echo 3. Description: Intent-based AI chatbot for environmental awareness
echo 4. Make it Public
echo 5. DO NOT check any initialization options
echo 6. Click "Create repository"
echo.
set /p username="Enter your GitHub username: "
echo.
echo Adding GitHub remote...
git remote add origin https://github.com/%username%/ecogeniebot.git
echo.
echo Pushing to GitHub...
git push -u origin main
echo.
echo Done! Your EcoGenieBot is now on GitHub!
echo Repository URL: https://github.com/%username%/ecogeniebot
pause