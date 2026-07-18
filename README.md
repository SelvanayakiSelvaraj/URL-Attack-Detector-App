# URL Attack Detector

**🔴 Live Demo: [https://url-attack-detector-web.onrender.com](https://url-attack-detector-web.onrender.com)**


An AI-powered security application that detects malicious URLs in real-time. This project uses a **Spring Boot** backend to handle user requests and a **Python Machine Learning** service to classify URL patterns.

## 🚀 Overall Working

The application follows a microservices-style architecture:

1.  **Frontend (UI)**: A modern, dark-themed dashboard (`index.html`) built with Vanilla CSS and JavaScript. Users enter a URL they want to scan.
2.  **Backend (Spring Boot)**: Acts as the orchestrator. It serves the UI and provides a REST API (`/analyze-url`). When it receives a scan request, it forwards the URL to the Python ML service.
3.  **ML Service (Python/Flask)**: Receives the URL and processes it through a machine learning model.
    *   **Feature Extraction**: Uses TF-IDF (Term Frequency-Inverse Document Frequency) to analyze character patterns (e.g., looking for `<script>`, `OR 1=1`, `../`).
    *   **Classification**: A **Logistic Regression** model classifies the URL as `Safe` or `Malicious`.
    *   **Attack Detection**: If malicious, another model identifies the specific attack type (SQLi, XSS, or Path Traversal).
4.  **Result**: The prediction and risk level (Low/Medium/High) are sent back to the UI and displayed to the user instantly.

## 🛠️ Project Structure

```text
url-attack-detector/
├── src/main/java/.../UrlController.java      # Spring Boot REST Controller
├── src/main/resources/static/index.html      # Frontend Dashboard
├── src/main/resources/application.properties  # App Configuration
├── ml_service/
│   ├── train_model.py                        # ML Model training script
│   ├── app.py                                # Python Flask API
│   ├── requirements.txt                      # Python dependencies
│   └── model/                                # Saved .pkl models
├── run_detector.bat                          # Automated ONE-CLICK launcher
├── pom.xml                                   # Maven dependencies
└── README.md                                 # Documentation
```

## 🛡️ Detections Supported
- **SQL Injection (SQLi)**: Unauthorized database access attempts.
- **Cross-Site Scripting (XSS)**: Malicious script injections.
- **Path Traversal**: Unauthorized file system access attempts.

## 🔧 Installation & Usage

### One-Click Launch (Windows)
1. Ensure you have **Java 17** and **Python 3.9+** installed.
2. Double-click `run_detector.bat`.
3. Open `http://localhost:8080` in your browser.

## 📄 License
This project is open-source and available for educational security research.
