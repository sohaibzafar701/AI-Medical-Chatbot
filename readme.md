# Medical Chatbot

A beginner-friendly FastAPI-based web application that provides a medical chatbot powered by ChromaDB. The chatbot uses a dataset from MedQuAD to answer medical questions after registration and login. This README guides you step-by-step, even if you're new to coding, to set up, prepare the dataset, and run the app without errors.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
  - [Downloading and Preparing the Dataset](#downloading-and-preparing-the-dataset)
  - [Cleaning and Converting the Dataset](#cleaning-and-converting-the-dataset)
  - [Indexing the Dataset with ChromaDB](#indexing-the-dataset-with-chromadb)
  - [Setting Up the Application](#setting-up-the-application)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
This project is a medical chatbot built with FastAPI, featuring user authentication, a SQLite database, and ChromaDB for storing medical Q&A data. The dataset is sourced from MedQuAD, cleaned, converted to JSON, and indexed for semantic search using SentenceTransformer embeddings. The frontend uses Tailwind CSS for a simple, stylish interface.

## Features
- User registration and login with JWT-based authentication.
- Secure password hashing with bcrypt.
- Medical chatbot with responses from the MedQuAD dataset.
- Query and response logging in a SQLite database.
- Responsive web design with Tailwind CSS.
- Auto-reloading during development with Uvicorn.

## Prerequisites
Before starting, install these on your computer:
- **Python 3.12** or later (download from [python.org](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (download from [git-scm.com](https://git-scm.com/downloads))
- **Node.js** (optional, for Tailwind CSS; download from [nodejs.org](https://nodejs.org/))

### Recommended Tools
- A code editor like VSCode (download from [code.visualstudio.com](https://code.visualstudio.com/))
- A virtual environment (built into Python)

## Installation

### 1. Clone the Repository
Clone this project to your computer using Git:
```bash
git clone https://github.com/your-username/medical-chatbot.git
cd medical-chatbot
```

### 2. Create a Virtual Environment
Make a virtual environment to keep things organized:
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install the needed Python packages:
```bash
pip install -r requirements.txt
```

## Setup

### Downloading and Preparing the Dataset
The chatbot uses the MedQuAD dataset. Follow these steps to download and prepare it.

#### 1. Download the MedQuAD Dataset
- Open a new terminal (or use the same one after activating the virtual environment).
- Navigate to the `dataset` directory:
  ```bash
  cd medical-chatbot/dataset
  ```
- Clone the MedQuAD repository:
  ```bash
  git clone https://github.com/abachaa/MedQuAD.git
  ```
- This creates a `MedQuAD` folder inside `dataset`.

#### 2. Index Data into Chromadb
- run the scripts in the given order in dataset directory:
1. 
```bash
  python data_loading.py
  ```
2. 
```bash
  python clean-dataset.py
  ```
3. 
```bash
  python csv_to_json.py
  ```
4. 
```bash
  python index_chromadb.py
  ```
5. 
```bash
  python check_data.py
  ```
- Expected output: `Number of items in medquad: 16359` and a sample document. If the count is 0, re-run `index_chromadb.py`.

#### 3. Troubleshoot Dataset Issues
- If indexing fails, ensure the path in `index_chromadb.py` matches `C:/Users/sohaib/Downloads/medical-chatbot-main/medical-chatbot-main/dataset/chromadb`.
- Check `medquad_cleaned.json` for data. If empty, re-run all above.

### Setting Up the Application

#### 1. Configure Environment Variables
- Navigate to the `app` directory:
  ```bash
  cd ../app
  ```
- Create a `.env` file:
  ```bash
  echo "SECRET_KEY=your_secure_key_here" > .env
  ```
- Replace `your_secure_key_here` with a unique key (e.g., `openssl rand -hex 32`).

## Running the Application

### 1. Start the Server
- In the `app` directory terminal, start the server:
  ```bash
  uvicorn main:app --reload
  ```
- The app runs at `http://127.0.0.1:8000`.

### 2. Access the Application
- Open your browser and go to `http://127.0.0.1:8000`.

## Usage

### 1. Register a New User
- Click "Register a New User".
- Enter a username and password, then click "Register".

### 2. Log In
- Click "Login".
- Enter your username and password, then click "Login".
- You’ll be redirected to the chatbot page.

### 3. Chat with the Bot
- Enter a question (e.g., "pain in my head") and click "Send".
- The response appears below.

### 4. Test with cURL (Optinal)
- Get a token:
  ```bash
  curl -X POST "http://127.0.0.1:8000/token" -d "username=your_username" -d "password=your_password" -d "grant_type=password"
  ```
- Query the chatbot:
  ```bash
  curl -H "Authorization: Bearer your_token_here" "http://127.0.0.1:8000/chatbot?query=pain%20in%20head"
  ```
  Replace `your_token_here` with the new token.

## Project Structure
```
medical-chatbot/
├── app/
│   ├── main.py           # FastAPI backend
│   └── .env             # Environment variables
├── dataset/
│   ├── chromadb/         # ChromaDB storage
│   ├── medquad_raw/     # Raw MedQuAD QA data
│   ├── medquad_cleaned.json # Cleaned dataset
│   ├── check_chromadb.py # Collection check script
│   ├── check_data.py    # Data verification script
│   ├── clean_medquad.py # Cleaning script
│   ├── index_chromadb.py # Indexing script
│   └── MedQuAD/         # Original MedQuAD repo
├── frontend/
│   └── index.html       # Frontend with Tailwind CSS
├── venv/                # Virtual environment
└── README.md            # This file
```

## Contributing
1. Fork the repo.
2. Create a branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push (`git push origin feature-branch`).
5. Open a pull request.

## License
MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments
- **FastAPI**, **ChromaDB**, **SentenceTransformer**, **Tailwind CSS**, and the **xAI Community**.
```
