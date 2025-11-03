# GitHub Setup Instructions for EcoGenieBot

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `ecogeniebot`
5. Description: `Intent-based AI chatbot for environmental awareness and sustainability`
6. Make it Public (or Private if you prefer)
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands in your terminal:

```bash
# Navigate to your project directory
cd "C:\Users\lucky\project\AICTE"

# Add GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/ecogeniebot.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed on the main page

## Project Structure (Now Organized)

```
ecogeniebot/
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── app.py                  # Main Flask application
├── streamlit.py           # Streamlit web interface
├── intents.json           # Training data
├── notebooks/             # Jupyter notebooks
│   ├── chatbot_week_1.ipynb
│   ├── chatbot_week_2.ipynb
│   ├── chatbot_week_3.ipynb
│   └── EcoGenie_chatbot.ipynb
├── PROJECT/               # Original project files
└── docs/                  # Documentation (empty for now)
```

## Next Steps

1. Update your GitHub profile README to showcase this project
2. Add topics/tags to your repository (AI, chatbot, NLP, environment)
3. Consider adding a license file
4. Create issues for future improvements
5. Add screenshots of your chatbot in action

## Troubleshooting

If you get authentication errors:
- Use GitHub CLI: `gh auth login`
- Or use Personal Access Token instead of password
- Or use SSH keys for authentication

Your EcoGenieBot is now ready for GitHub! 🚀🌱