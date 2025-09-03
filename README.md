# Moments

A photo sharing social networking app built with Python and Flask. The example application for the book *[Python Web Development with Flask (2nd edition)](https://helloflask.com/en/book/4)* (《[Flask Web 开发实战（第 2 版）](https://helloflask.com/book/4)》).

Demo: http://moments.helloflask.com

![Screenshot](demo.png)

## ✨ New Features

### 🤖 AI-Powered Alternative Text Generation
This version includes machine learning capabilities to automatically generate descriptive text for images:

- **Automatic Image Description**: When users upload photos without descriptions, AI generates meaningful alternative text
- **Enhanced Accessibility**: Improves experience for users with visual impairments
- **Smart Content Understanding**: Uses state-of-the-art vision-language models to analyze image content
- **Seamless Integration**: Works automatically in the background during photo uploads

## Installation

Clone the repo:

```
$ git clone https://github.com/greyli/moments
$ cd moments
```

Install dependencies with [PDM](https://pdm.fming.dev):

```
$ pdm install
```

> [!TIP]
> If you don't have PDM installed, you can create a virtual environment with `venv` and install dependencies with `pip install -r requirements.txt`.

### 🚀 Setting Up ML Features

The ML features require additional dependencies. Install them with:

```bash
pip install -r requirements.txt
```

> [!NOTE]
> The first time you run the app, it will download pre-trained ML models (~1-2GB). This may take a few minutes depending on your internet connection.

### 🗄️ Database Migration

After installation, run the database migration to add the new ML fields:

```bash
python migrate_alt_text.py
```

To initialize the app, run the `flask init-app` command:

```
$ pdm run flask init-app
```

If you just want to try it out, generate fake data with `flask lorem` command then run the app:

```
$ pdm run flask lorem
```

It will create a test account:

* email: `admin@helloflask.com`
* password: `moments`

Now you can run the app:

```
$ pdm run flask run
* Running on http://127.0.0.1:5000/
```

### 🧪 Testing ML Features

To verify that the ML features are working correctly:

```bash
python test_alt_text.py
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
