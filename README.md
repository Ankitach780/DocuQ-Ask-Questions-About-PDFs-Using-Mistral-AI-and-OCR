# 📝 DocuQ-Ask-Questions-About-PDFs-Using-Mistral-AI-and-OCR
📄DocuQ is a Streamlit-based web app that allows users to upload PDF documents and ask natural language questions about them. The app uses Mistral AI's OCR and chat models to extract text from documents and provide intelligent answers.
---

## ✨ Key Features

- 🔐 **Secure Mistral API integration** via `.env` file
- 📄 Upload any **PDF document**
- 🤖 Uses **Mistral’s OCR** and **chat models** for question answering
- 🧠 Stores Q&A logs per user in a **local SQLite database**
- 👤 Session-based **user management**
- 💾 Persistent **Q&A log** viewing (toggle-able)
- 💡 Built with **Streamlit** for a clean, interactive interface

---

## 🚀 Deployment & Setup
1. Clone the repo:
```
git clone https://github.com/Ankitach780/DocuQ-Ask-Questions-About-PDFs-Using-Mistral-AI-and-OCR.git
cd docuq
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a .env file in the root directory:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```
4. Run the app:
```
streamlit run app.py
```

## 🛠️ Project Structure
```
docuq/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── qa_database.db        # SQLite DB for Q&A logs (created at runtime)
├── .env                  # Environment variables (not uploaded to GitHub)
├── .gitignore            # Ignores .env, pycache, etc.
└── README.md             # This file
```

## 🙋‍♀️ Contributing
-Pull requests are welcome! To contribute:
-Fork the project
-Create a new branch (git checkout -b feature-name)
-Commit your changes (git commit -m 'Add some feature')
-Push to the branch (git push origin feature-name)
-Open a Pull Request

## ⚖️ License
This project is licensed under the MIT License
 – feel free to use, modify, and distribute!
