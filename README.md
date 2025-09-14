<div align="center">

![Cover Page](images/image.png)

# 🤖 **Trend Setters - E-Commerce Conversational Chatbot**

*Product submitted to Cognizant Kolkata through Digital Nurture TechnoVerse East Hackathon*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Features](#features) • [Installation](#installation) • [Documentation](#documentation) • [Usage](#usage) • [Contributing](#contributing)

</div>

# 📌 Overview
This project is an AI-powered conversational chatbot designed for e-commerce platforms. The chatbot provides product recommendations based on user queries, leveraging Natural Language Processing (NLP) and Vector Search technology.

---

# 🚀 Features
- **Conversational AI**: Uses LLaMA 3 70B model via Groq API.
- **Vector Search**: Searches products dynamically using Qdrant.
- **Multi-Attribute Query Handling**: Filters products based on brand, color, category, and other attributes.
- **Flask-based Backend**: Integrates with a front-end UI.
- **Dynamic Query Processing**: Returns results even with partial inputs.
- **Fallback Mechanism**: Displays random products when no input is provided.

---

# 🛠️ Tech Stack
- **Backend**: Flask, Python
- **AI Model**: LLaMA 3 70B (via Groq API) powered by META
- **Vector Database**: Qdrant Vector Database
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: TBD

---

# 🔧 Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/priyam-hub/E-Commerce_Conversational_Chatbot.git
   cd E-Commerce_Conversational_Chatbot
   ```
2. **Create a virtual environment & activate it**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Create a `.env` file and add the following:
     ```env
     GROQ_API_KEY    =your_api_key_here
     QDRANT_URL      =your_qdrant_url_here
     QDRANT_API_KEY  =your_qdrant_api_key_here
     ```
5. **Run the Flask server**
   ```sh
   python app.py
   ```
6. **Access the chatbot UI**
   Open `http://127.0.0.1:5000` in your browser.

---

# 🔍 Usage
1. Enter a product-related query in the chatbot.
2. The chatbot will process the query using NLP.
3. If attributes like brand or color are specified, it filters the results.
4. If no attributes are found, it returns a set of random products.

---

# 📂 Project Structure
```
E-Commerce_Conversational_Chatbot/
│── flask_chatbot/
│   ├── app.py  # Main Flask application
│   ├── templates/
│   │   ├── index.html  # Chat UI
│   │   ├── chatbot.html  # Chatbot logic
│   ├── static/
│   │   ├── css/
│   │   │   ├── styles.css  # Styling for chatbot UI
│   │   ├── js/
│   │   │   ├── home.js  # Frontend interactions
│   ├── images/
│   ├── requirements.txt  # Dependencies
│── README.md
│── .env  # Environment variables
```

# 📜 License
This project is licensed under the MIT License.

---

### 🎯 Future Enhancements
- Improve NLP model accuracy
- Add chatbot support for multiple languages
- Integrate voice search

---

<div align="center">

**Made with ❤️ by Team Technocrats**

[↑ Back to Top]()

</div>

