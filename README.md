# FastHTML Session Management Template

This repository provides a simple template for a web application using FastHTML for session management. It includes authentication, session handling, and a protected dashboard for logged-in users.

## Features

- User login with username and password.
- Persistent session storage using PySOS.
- Session expiration logic.
- A protected homepage displaying user-specific information.
- Modular structure for readability and maintainability.

## File Structure

```
.
├── app.py                # Main application logic
├── homepage_content.py   # HTML content generation for the homepage
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Requirements

- Python 3.7+
- Required packages (install using `pip`):
  - `fasthtml`
  - `pysos`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/fasthtml-session-template.git
   cd fasthtml-session-template
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open the application in your browser at `http://127.0.0.1:8000`.
2. Login using the default credentials:
   - **Username**: `admin`
   - **Password**: `admin`
3. View the protected dashboard upon successful login.

## Customization

- **Homepage Content**: Modify `homepage_content.py` to customize the HTML for the protected homepage.
- **Session Expiration**: Adjust the expiration time in `session_status_checker` within `app.py`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

