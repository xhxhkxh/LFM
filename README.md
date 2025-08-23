# 🌟 The LFM Project

> *A lightweight, fully-functional forum built with passion over three years of dedicated development.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Core-purple.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Version](https://img.shields.io/badge/Version-v5.0.0%20Spinnere-red.svg)](#)

The LFM Project is a modern, lightweight forum solution designed for communities who value simplicity without sacrificing functionality. After three years of careful development and refinement, this project represents a labor of love and is now open-source with a completely refactored, modular architecture.

## ✨ Key Features

### 🚀 **Performance & Architecture**
- **Modular Design**: Clean separation with blueprints and modules
- **Flask Backend**: Robust Python web framework with blueprint organization
- **SQLAlchemy Core**: Modern database abstraction layer with PyMySQL driver
- **Session Management**: Secure user authentication with configurable timeouts
- **App Factory Pattern**: Clean application initialization and configuration

### 🎨 **User Experience**
- **Responsive Design**: Seamless experience on desktop and mobile
- **Clean Interface**: Intuitive design with HarmonyOS Sans typography
- **Mobile-First**: Dedicated mobile templates (`/forum/m`, `/home/m`)
- **Real-time Updates**: Dynamic post and comment system

### 🔒 **Security & Protection**
- **Advanced Password Hashing**: Argon2 encryption for user passwords
- **hCaptcha Integration**: Built-in spam and bot protection (WIP)
- **SQL Injection Protection**: SQLAlchemy parameterized queries and input sanitization
- **XSS Prevention**: Content encoding and validation with forbidden pattern detection
- **Session Security**: Secure session management with configurable timeouts
- **HTTPS Support**: Development HTTPS with self-signed certificates

### 📝 **Forum Functionality**
- **Post Management**: Create, view, and organize forum posts
- **Comment System**: Nested replies and discussions
- **User Profiles**: Customizable user pages with post history and email management
- **Email Integration**: User email management and verification
- **Content Encoding**: URL-safe content encoding for multilingual support

### 🛠 **Developer Features**
- **Modular Architecture**: Separated modules for auth, database, forum, and utilities
- **Blueprint Organization**: Clean route separation by functionality
- **Debug Mode**: Comprehensive logging and error handling
- **Easy Customization**: Template-based theming system
- **Database Flexibility**: SQLAlchemy-based database abstraction
- **Error Handling**: Centralized error handlers with custom error pages

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+** - [Download Python](https://python.org/downloads/)
- **MySQL Server** - [Download MySQL](https://dev.mysql.com/downloads/)
- **pip** - Python package installer (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xhxhkxh/LFM.git
   cd lfm-project
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Setup**
   
   Create your MySQL database and tables:
   ```sql
   CREATE DATABASE lfm_forum;
   USE lfm_forum;
   
   -- Users table
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       signin_date DATETIME DEFAULT CURRENT_TIMESTAMP,
       last_login DATETIME,
       email VARCHAR(255),
       pwd_need_update TINYINT DEFAULT 0
   );
   
   -- Posts table
   CREATE TABLE posts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title TEXT NOT NULL,
       content LONGTEXT NOT NULL,
       authorID INT,
       P_time DATETIME DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (authorID) REFERENCES users(id)
   );
   
   -- Reply/Comments table
   CREATE TABLE reply (
       id INT AUTO_INCREMENT PRIMARY KEY,
       content TEXT NOT NULL,
       authorID INT,
       ref_to INT,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (authorID) REFERENCES users(id),
       FOREIGN KEY (ref_to) REFERENCES posts(id)
   );
   ```

4. **Configure the application**
   
   Edit `modules/config.py` and update the following configuration:
   
   ```python
   # Database Configuration
   MYSQL = {
       'host': 'your-mysql-host',          # e.g., 'localhost'
       'user': 'your-mysql-username',      # e.g., 'root'
       'port': 3306,                       # MySQL port
       'password': 'your-mysql-password',  # Your MySQL password
       'db': 'your-database-name',         # e.g., 'lfm_forum'
       'charset': 'utf8'                   # Character set
   }
   
   # Security Keys
   SECRET_KEY = 'your-secret-key-here'  # Put your secure key here
   CAPTCHA_SECRET_KEY = 'your-hcaptcha-secret-key'  # From hCaptcha dashboard
   ```
   *⚠ Please notice that the Captcha function is still WIP!*

5. **Update domain references**
   
   In the HTML template files, replace placeholder domains with your actual domain:
   - `forum-nt-v2.htm`
   - `forum-m.htm` 
   - `forum.htm`
   - `intro.htm`

6. **Launch the server**
   ```bash
   python app.py
   ```

7. **Access your forum**
   
   Open your browser and navigate to `https://localhost:5000` (HTTPS enabled by default in development)

## ⚙️ Configuration Guide

### Database Configuration

The database settings are located in `modules/config.py`:

```python
MYSQL = {
    'host': 'localhost',        # Your MySQL host
    'user': 'your_username',    # Your MySQL username
    'port': 3306,              # MySQL port (default: 3306)
    'password': 'your_password', # Your MySQL password
    'db': 'your_database',      # Your database name
    'charset': 'utf8'          # Character encoding
}
```

### Security Configuration

1. **Session Security**
   ```python
   SECRET_KEY = 'your-super-secret-key'  # Use a strong, random key
   PERMANENT_SESSION_LIFETIME = timedelta(hours=1)  # Session timeout
   ```

2. **hCaptcha Setup**
   - Sign up at [hCaptcha.com](https://www.hcaptcha.com/)
   - Get your site key and secret key
   - Update `CAPTCHA_SECRET_KEY` in `modules/config.py`
   - Update the site key in your HTML templates

### Enhanced File Structure

```
lfm-project/
├── app.py                    # Application factory and entry point
├── requirements.txt          # Python dependencies
├── modules/                  # Core application modules
│   ├── __init__.py          # Module package initialization
│   ├── config.py            # Configuration settings
│   ├── auth.py              # Authentication logic
│   ├── db.py                # Database abstraction (SQLAlchemy)
│   ├── forum.py             # Forum blueprint and logic
│   ├── models.py            # Data models
│   ├── utils.py             # Utility functions
│   └── errors.py            # Error handlers
├── route/                   # Route blueprints
│   ├── __init__.py          # Blueprint registration
│   ├── auth.py              # Authentication routes
│   ├── forum.py             # Forum routes
│   ├── home.py              # Home page routes
│   ├── user.py              # User profile routes
│   └── misc.py              # Miscellaneous routes
├── classes/                 # Data classes
│   └── post.py              # Post and Reply classes
├── templates/               # HTML templates
│   ├── forum.htm            # Desktop forum view
│   ├── forum-m.htm          # Mobile forum view
│   ├── login_remake.htm     # Login page
│   ├── np-m.htm            # New post page
│   ├── user.htm            # User profile page
│   ├── post-nt.htm         # Post detail view
│   ├── error.htm           # Error page
│   └── 403.htm             # Access denied page
├── fonts/                  # Custom fonts
│   └── hsr.TTF             # HarmonyOS Sans font
├── static/                 # Static assets
└── drawings/               # User uploaded images
```

## 🎨 Customization

### Theming

The LFM Project uses a template-based theming system with modular organization:

- **Colors & Styling**: Modify CSS within HTML templates
- **Layout**: Edit HTML template structure in the `templates/` directory
- **Typography**: The project includes HarmonyOS Sans font
- **Mobile Experience**: Separate mobile templates for optimal UX

### Adding Features

The modular architecture makes it easy to extend functionality:

1. **Database Extensions**: Add new tables and modify the `modules/db.py` class
2. **New Blueprints**: Create new blueprint modules in the `route/` directory
3. **Business Logic**: Add new modules in the `modules/` directory
4. **Templates**: Create new HTML templates in the `templates/` directory
5. **Static Assets**: Add CSS, JS, and images to the `static/` directory

### Creating Custom Modules

```python
# Example: modules/custom_feature.py
from flask import Blueprint

bp = Blueprint('custom_feature', __name__)

@bp.route('/custom')
def custom_route():
    return "Custom feature"

# Register in route/__init__.py
from modules import custom_feature
blueprints.append(custom_feature.bp)
```

## 🔧 API Endpoints

### Authentication Routes
| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Landing page |
| `/home` | GET | Login page |
| `/home/m` | GET | Mobile login page |
| `/home/login` | POST | User authentication |
| `/home/signin` | GET/POST | User registration |

### Forum Routes
| Endpoint | Method | Description |
|----------|---------|-------------|
| `/forum` | GET | Main forum view |
| `/forum/m` | GET | Mobile forum view |
| `/forum/post/<id>` | GET | View specific post |
| `/forum/post` | POST | Create new post |
| `/forum/verify` | GET | Verify session credentials |
| `/new-post` | GET | New post creation page |
| `/post/comment/<id>` | POST | Add comment to post |

### User Routes
| Endpoint | Method | Description |
|----------|---------|-------------|
| `/user/<id>` | GET | User profile page |
| `/user/<id>/changeemail` | GET | Update user email |

### Utility Routes
| Endpoint | Method | Description |
|----------|---------|-------------|
| `/getImage` | GET | Random image from drawings |
| `/fonts/hsr.TTF` | GET | HarmonyOS Sans font |
| `/md-playground` | GET | Markdown playground |

## 🚀 Deployment

### Production Setup

1. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

2. **Set up reverse proxy** (Nginx example):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Environment Variables**:
   Consider using environment variables for sensitive configuration:
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
   MYSQL['password'] = os.environ.get('DB_PASSWORD', 'fallback-password')
   ```

4. **Database Security**:
   - Use connection pooling for better performance
   - Enable SSL connections for production databases
   - Use dedicated database user with minimal privileges

## 🏗️ Architecture Overview

### Application Factory Pattern
The application uses the factory pattern with clean separation of concerns:

- **`app.py`**: Entry point and application factory
- **`modules/`**: Business logic and core functionality
- **`route/`**: HTTP route definitions and request handling
- **`classes/`**: Data models and structures

### Database Layer
- **SQLAlchemy Core**: Modern database abstraction
- **Connection Pooling**: Efficient database connections
- **Error Handling**: Comprehensive database error management
- **Security**: Parameterized queries prevent SQL injection

### Security Features
- **Argon2 Password Hashing**: Industry-standard password security
- **Session Management**: Secure session handling with timeouts
- **Input Validation**: Content encoding and forbidden pattern detection
- **HTTPS Support**: SSL/TLS encryption for data in transit

## 🤝 Contributing

Contributions are warmly welcomed! This project represents three years of passionate development, and community input can help it grow even further.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 Python style guidelines
- Add comments for complex functionality
- Test your changes thoroughly
- Update documentation as needed
- Maintain modular architecture
- Use type hints where appropriate

### Code Quality
- Use the modular structure for new features
- Separate business logic from route handlers
- Follow the established patterns for database interactions
- Add appropriate error handling

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
- Verify MySQL server is running
- Check database credentials in `modules/config.py`
- Ensure database and tables exist
- Install required packages: `pip install PyMySQL cryptography`

**Missing Cryptography Package**
```bash
pip install cryptography
```
Required for MySQL's `sha256_password` or `caching_sha2_password` authentication methods.

**Session Issues**
- Check that `SECRET_KEY` is set in `modules/config.py`
- Verify session timeout settings
- Clear browser cookies if needed

**Template Not Found**
- Ensure templates are in the `templates/` directory
- Check file names match route handlers
- Verify file permissions

**Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that the virtual environment is activated
- Verify Python path includes the project directory

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

The project uses the HarmonyOS Sans font, which is open-source and freely available.

## 🙏 Acknowledgments

*From the developer:*

> The LFM project consumed years of my life, and standing here now, I'm overwhelmed by a flood of emotions I can't quite name. The memories we've built through LFM are etched permanently in my mind—vivid, precious, and unforgettable.

Special thanks to all contributors who have helped improve the codebase and architecture.

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report bugs](https://github.com/xhxhkxh/LFM/issues)
- 💡 [Request features](https://github.com/xhxhkxh/LFM/issues)
- 📚 [Documentation](https://github.com/xhxhkxh/LFM/wiki)

## 🎯 Roadmap

Future enhancements being considered:

- [ ] Complete hCaptcha integration
- [ ] Advanced moderation tools
- [ ] Real-time notifications with WebSocket support
- [ ] File upload system with security scanning
- [ ] Advanced search functionality with full-text indexing
- [ ] Plugin system for extensibility
- [ ] REST API endpoints for mobile apps
- [ ] Docker containerization
- [ ] Admin dashboard for forum management
- [ ] Multi-language support
- [ ] Database migration tools
- [ ] Automated testing suite

## 📊 Recent Improvements

**Version v5.0.0 "Spinnere" Features:**
- ✅ Modular architecture with blueprints
- ✅ SQLAlchemy Core database abstraction
- ✅ App factory pattern implementation
- ✅ Enhanced security with better input validation
- ✅ Improved error handling and logging
- ✅ Cleaner separation of concerns
- ✅ Development HTTPS support
- ✅ Enhanced configuration management

## 🎃Funny Ideas

- [ ] AI-Generated replys
- [ ] AI-Rating system

> Which do you prefer? Or.you have other incredible ideas? Tell me [Here](https://github.com/xhxhkxh/LFM/issues) !

---

**Made with ❤️ over 3 years of passionate development**

**And also our Contributors!**

<a href="https://github.com/xhxhkxh/LFM/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xhxhkxh/LFM" />
</a>

*Made with [contrib.rocks](https://contrib.rocks).*


## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report bugs](https://github.com/xhxhkxh/LFM/issues)
- 💡 [Request features](https://github.com/xhxhkxh/LFM/issues)

## 🎯 Roadmap

Future enhancements being considered:

- [ ] Advanced moderation tools
- [ ] Real-time notifications
- [ ] File upload system
- [ ] Advanced search functionality
- [ ] Plugin system
- [ ] REST API endpoints
- [ ] Docker containerization

---

**Made with ❤️ over 3 years of passionate development**

**And also our Contributors!**


<a href="https://github.com/xhxhkxh/LFM/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xhxhkxh/LFM" />
</a>

*Made with [contrib.rocks](https://contrib.rocks).*

*Version v5.0.0 - "Spinnere"*


