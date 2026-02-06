# Installation Guide - Python 3.13 on Windows

## Option 1: Use Pre-built Wheels (RECOMMENDED - Fastest)

Try installing with pre-built wheels:

```bash
pip install --upgrade pip
pip install --only-binary :all: -r requirements.txt
```

If this fails, try Option 2.

## Option 2: Install Without Build Tools (Use Older Compatible Versions)

```bash
# Install compatible versions
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install sqlalchemy==2.0.25
pip install alembic==1.13.1
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install pyjwt==2.8.0
pip install bcrypt==4.1.2
pip install pydantic==2.6.0
pip install email-validator==2.1.0
pip install python-multipart==0.0.6
pip install cryptography==42.0.0
```

## Option 3: If Still Failing - Use Python 3.11 or 3.12

Python 3.13 is very new and some packages don't have pre-built wheels yet.

**Recommended:** Install Python 3.11 or 3.12 from python.org

Then run:
```bash
pip install -r requirements.txt
```

## Quick Test After Installation

```bash
# Test if everything installed correctly
python -c "import fastapi; import uvicorn; print('✅ Installation successful!')"
```

## Run the Server

```bash
python main.py
```

Visit: http://localhost:8000/docs
