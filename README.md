# 🌟 The LFM Project

> *A lightweight, fully-functional forum built with passion over three years of dedicated development.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Open_Source-orange.svg)](#license)
[![Version](https://img.shields.io/badge/Version-v4.0.4_Attercap-red.svg)](#)

The LFM Project is a modern, lightweight forum solution designed for communities who value simplicity without sacrificing functionality. After three years of careful development and refinement, this project represents a labor of love and is now open-source and ready for the community.

## ✨ Key Features

### 🚀 **Performance & Architecture**
- **Lightweight Design**: Optimized for speed and efficiency
- **Flask Backend**: Robust Python web framework
- **MySQL Database**: Reliable data persistence
- **Session Management**: Secure user authentication

### 🎨 **User Experience**
- **Responsive Design**: Seamless experience on desktop and mobile
- **Clean Interface**: Intuitive design with HarmonyOS Sans typography
- **Mobile-First**: Dedicated mobile templates (`/forum/m`, `/home/m`)
- **Real-time Updates**: Dynamic post and comment system

### 🔒 **Security & Protection**
- **Advanced Password Hashing**: Argon2 encryption for user passwords
- **hCaptcha Integration**: Built-in spam and bot protection
- **SQL Injection Protection**: Parameterized queries and input sanitization
- **XSS Prevention**: Content encoding and validation
- **Session Security**: Secure session management with configurable timeouts

### 📝 **Forum Functionality**
- **Post Management**: Create, view, and organize forum posts
- **Comment System**: Nested replies and discussions
- **User Profiles**: Customizable user pages with post history
- **Email Integration**: User email management and verification
- **Markdown Support**: Rich text formatting capabilities

### 🛠 **Developer Features**
- **Modular Architecture**: Clean separation of concerns
- **Debug Mode**: Comprehensive logging and error handling
- **Easy Customization**: Template-based theming system
- **Database Flexibility**: Configurable MySQL connection settings

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+** - [Download Python](https://python.org/downloads/)
- **MySQL Server** - [Download MySQL](https://dev.mysql.com/downloads/)
- **pip** - Python package installer (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lfm-project.git
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
   
   Edit `app.py` and update the following configuration:
   
   ```python
   # Database Configuration
   self.host = 'your-mysql-host'          # e.g., 'localhost'
   self.user = 'your-mysql-username'      # e.g., 'root'
   self.password = 'your-mysql-password'  # Your MySQL password
   self.db = 'your-database-name'         # e.g., 'lfm_forum'
   
   # Security Keys
   app.secret_key = 'your-secret-key-here'  # Generate a secure random key
   CAPTCHA_SECRET_KEY = 'your-hcaptcha-secret-key'  # From hCaptcha dashboard
   ```

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
   
   Open your browser and navigate to `http://localhost:5000`

## ⚙️ Configuration Guide

### Database Configuration

The database settings are located in the `SQL` class within `app.py`:

```python
class SQL():
    def __init__(self):
        self.host = 'localhost'        # Your MySQL host
        self.user = 'your_username'    # Your MySQL username
        self.port = 3306              # MySQL port (default: 3306)
        self.password = 'your_password' # Your MySQL password
        self.db = 'your_database'      # Your database name
```

### Security Configuration

1. **Session Security**
   ```python
   app.secret_key = 'your-super-secret-key'  # Use a strong, random key
   app.permanent_session_lifetime = timedelta(hours=1)  # Session timeout
   ```

2. **hCaptcha Setup**
   - Sign up at [hCaptcha.com](https://www.hcaptcha.com/)
   - Get your site key and secret key
   - Update `CAPTCHA_SECRET_KEY` in `app.py`
   - Update the site key in your HTML templates

### File Structure

```
lfm-project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── forum.htm         # Desktop forum view
│   ├── forum-m.htm       # Mobile forum view
│   ├── login_remake.htm  # Login page
│   ├── np-m.htm         # New post page
│   ├── user.htm         # User profile page
│   └── ...
├── fonts/               # Custom fonts
│   └── hsr.TTF         # HarmonyOS Sans font
├── static/             # Static assets
└── drawings/           # User uploaded images
```

## 🎨 Customization

### Theming

The LFM Project uses a template-based theming system. You can customize:

- **Colors & Styling**: Modify CSS within HTML templates
- **Layout**: Edit HTML template structure
- **Typography**: The project includes HarmonyOS Sans font
- **Mobile Experience**: Separate mobile templates for optimal UX

### Adding Features

The modular architecture makes it easy to extend functionality:

1. **Database Extensions**: Add new tables and modify the `SQL` class
2. **New Routes**: Add Flask routes in `app.py`
3. **Templates**: Create new HTML templates in the `templates/` directory
4. **Static Assets**: Add CSS, JS, and images to the `static/` directory

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Landing page |
| `/home` | GET | Login page |
| `/home/login` | POST | User authentication |
| `/home/signin` | GET/POST | User registration |
| `/forum` | GET | Main forum view |
| `/forum/m` | GET | Mobile forum view |
| `/forum/post/<id>` | GET | View specific post |
| `/post/comment/<id>` | POST | Add comment to post |
| `/user/<id>` | GET | User profile page |
| `/new-post` | GET | New post creation page |

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
       }
   }
   ```

3. **Environment Variables**:
   Consider using environment variables for sensitive configuration:
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY', 'fallback-key')
   ```

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

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
- Verify MySQL server is running
- Check database credentials in `app.py`
- Ensure database and tables exist

**Session Issues**
- Check that `secret_key` is set
- Verify session timeout settings
- Clear browser cookies if needed

**Template Not Found**
- Ensure templates are in the `templates/` directory
- Check file names match route handlers
- Verify file permissions

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

The project uses the HarmonyOS Sans font, which is open-source and freely available.

## 🙏 Acknowledgments

*From the developer:*

> The LFM project really took me a long time to develop, and standing at this spot... I am really feeling complicated. Don't know what to say, but all the memories that the LFM have created will be an unfadeable image in my mind.
> 
> Because, as they say: *"代码可能过时，但是那个瞬间，永远新鲜"* (Code may become outdated, but that moment will always be fresh).

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report bugs](https://github.com/xhxhkxh/LFM/issues)
- 💡 [Request features](https://github.com/xhxhkxh/LFM/issues)
- 💬 [Join discussions](https://github.com/xhxhkxh/LFM/discussions)

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

*Version v4.0.4 - "Attercap"*
