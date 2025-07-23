# The LFM Project

A lightweight, fully-functional forum built with passion over three years of dedicated development.

## 🌟 About

The LFM Project is a modern, lightweight forum solution designed for communities who value simplicity without sacrificing functionality. After three years of careful development and refinement, this project is now open-source and ready for the community.

## ✨ Features

- **Lightweight Architecture**: Fast and efficient performance
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Customizable**: Easy to modify and brand for your community
- **Captcha Support**: Built-in spam protection
- **Clean Interface**: User-friendly design with HarmonyOS Sans font
- **Open Source**: Free to use and modify

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Get the source code**
   ```bash
   git clone [your-repository-url]
   cd lfm-project
   ```
   
   Or download and extract the ZIP file.

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

3. **Configure the application**
   
   Update the following files according to your needs:
   
   - **`app.py`** - Database connection settings
   - **`forum-nt-v2.htm`**, **`forum-m.htm`**, **`forum.htm`** - Update domain references
   - **`intro.htm`** - Customize introduction page
   - **`np-m.htm`** - Enable/configure captcha settings

4. **Launch the server**
   ```bash
   python app.py
   ```

5. **Test your installation**
   
   Open your browser and navigate to the local server address (typically `http://localhost:5000` or as configured).


## ⚙️ Configuration

### Database Setup
Edit `app.py` to configure your database connection:


### Domain Configuration
Update the HTML template files to reflect your domain:
- Replace placeholder domains in `forum-nt-v2.htm`, `forum-m.htm`, and `forum.htm`
- Customize the appearance and branding to match your community

### Captcha Configuration
Modify `np-m.htm` to enable or configure captcha settings for spam protection.

## 🎨 Customization

The LFM Project is designed to be easily customizable:

- **Templates**: Modify HTML files to change the appearance
- **Styling**: Update CSS within the templates
- **Features**: Extend functionality by modifying `app.py`

## 📝 License

This project uses the HarmonyOS Sans font, which is open-source and freely available.

[Add your chosen license here - MIT, GPL, etc.]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you encounter any issues or have questions, please [open an issue](link-to-issues) on GitHub.

## 🙏 Acknowledgments

*From the developer:*

The LFM project really took me a long time to develop, and standing at this spot... I am really feeling complicated. Don't know what to say, but all the memories that the LFM have created will be an unfadeable image in my mind.

Because, as they say: *"代码可能过时，但是那个瞬间，永远新鲜"* (Code may become outdated, but that moment will always be fresh).

---

**Made with ❤️ over 3 years of passionate development**