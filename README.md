# Voice Assistant

## Introduction
Voice Assistant is an advanced AI-powered assistant that helps users with various queries. Built with Flask and powered by Google's Gemini model, it provides responses based on predefined data and leverages the Gemini API for more general questions.

## Features
- **Conversational AI**: Interact with the assistant using natural language.
- **Personalized Responses**: Provides information about Shilp Gohil based on predefined data.
- **Gemini Integration**: Utilizes Google Gemini API for advanced question answering.
- **Text-to-Speech**: Speaks out responses using `pyttsx3`.
- **Web Interface**: A simple web interface for interaction.

## Installation

To set up the project locally, follow these steps:

1.  **Clone this repository**:

    ```bash
    git clone https://github.com/your-username/Voice-Assistant.git
    cd Voice-Assistant
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Gemini API Key**:

    Create a `.env` file in the root directory of the project and add your Gemini API Key:

    ```
    GEMINI_API_KEY='YOUR_GEMINI_API_KEY'
    ```

    Alternatively, you can directly replace the placeholder in `main.py`:

    ```python
    GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY' # Replace with your actual Gemini API Key
    ```

## Usage

To run the application, execute `main.py`:

```bash
python main.py
```

The application will typically run on `http://127.0.0.1:5000/`. Open this URL in your web browser to interact with the voice assistant.

### Building an Executable

To create a standalone executable of the voice assistant using PyInstaller, follow these steps:

1.  **Install PyInstaller** (if you haven't already):

    ```bash
    pip install pyinstaller
    ```

2.  **Build the Executable**:

    Run the following command in your project's root directory:

    ```bash
    pyinstaller --onefile --add-data "static;static" --add-data "templates;templates" --add-data ".env;." main.py
    ```

    This command will create a single executable file in the `dist/` directory, along with the `static`, `templates`, and `.env` files bundled within it.

    *   `--onefile`: Creates a single executable file.
    *   `--add-data "static;static"`: Includes the `static` folder and its contents.
    *   `--add-data "templates;templates"`: Includes the `templates` folder and its contents.
    *   `--add-data ".env;."`: Includes the `.env` file.

    The executable will be located in the `dist` folder.

### Deploying to Vercel

This project can be easily deployed to Vercel. A `vercel.json` file is included to configure the deployment.

1.  **Install Vercel CLI** (if you haven't already):

    ```bash
    npm install -g vercel
    ```

2.  **Deploy Your Project**:

    Navigate to your project's root directory in the terminal and run:

    ```bash
    vercel
    ```

    Follow the prompts to deploy your project. Vercel will automatically detect the `vercel.json` configuration and deploy your Flask application.

## Project Structure

```
Voice Assistant/
├── .env
├── main.py
├── requirements.txt
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    └── index.html
```

## Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Demo Video

Click the link : https://drive.google.com/file/d/1DdqDwN8Z0dnC_5qQl48y7J_ErnxlSzKU/view?usp=sharing

## Acknowledgments

-   AI Model API
-   Flask
-   pyttsx3
-   PyInstaller

## Contact

@shilpgohil@gmail.com
+919328418263
