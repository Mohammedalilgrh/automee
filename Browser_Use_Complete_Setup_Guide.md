# 🤖 Browser-Use Complete Setup Guide
## **Unlimited FREE Browser Automation on PC**

### 📋 **Quick Overview**
Browser-Use is a powerful, **completely FREE** open-source tool that enables AI to control your browser for unlimited automation tasks. With 70.2k+ GitHub stars and MIT license, it's trusted by thousands of developers worldwide.

### 🎯 **What You'll Achieve**
- **100% FREE unlimited browser automation** (no payment required)
- AI that can navigate websites, fill forms, extract data
- Support for multiple AI providers (Gemini FREE, OpenAI, Claude, etc.)
- Cross-platform support (Windows, macOS, Linux)
- Headless and visible browser modes

---

## 🚀 **Method 1: Automated Setup (Recommended)**

### **Step 1: Run the Auto-Setup Script**
1. Download `browser_use_setup.py` (provided)
2. Open Command Prompt/Terminal as Administrator
3. Navigate to the script location
4. Run: `python browser_use_setup.py`

The script will automatically:
- ✅ Check Python compatibility (3.11+ required)
- ✅ Install UV package manager
- ✅ Install browser-use package
- ✅ Install Chromium browser
- ✅ Create .env configuration file
- ✅ Generate demo and advanced scripts

### **Step 2: Get Your FREE API Key**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account (free)
3. Click "Create API Key"
4. Copy the generated key
5. Open `.env` file and replace `your_gemini_api_key_here` with your key

### **Step 3: Test Installation**
Run: `python demo_browser_use.py`

---

## ⚙️ **Method 2: Manual Setup**

### **Prerequisites**
- **Python 3.11+** (Check: `python --version`)
- **Windows 10/11, macOS, or Linux**
- **Internet connection**

### **Step 1: Install UV Package Manager**

#### Windows:
```bash
pip install uv
```

#### macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### **Step 2: Install Browser-Use**
```bash
uv pip install browser-use
```

### **Step 3: Install Chromium Browser**
```bash
uvx playwright install chromium --with-deps --no-shell
```

### **Step 4: Create Environment File**
Create `.env` file in your project directory:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### **Step 5: Basic Usage Script**
Create `test_browser_use.py`:
```python
from browser_use import Agent
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    from browser_use.browser.browser import Browser
    from browser_use.agent.service import Agent
    from langchain_google_genai import ChatGoogleGenerativeAI
    import os
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    
    browser = Browser()
    agent = Agent(
        task="Go to Google and search for 'browser automation'",
        llm=llm,
        browser=browser
    )
    
    result = await agent.arun()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔑 **API Key Setup (FREE Options)**

### **Option 1: Google Gemini (Recommended - 100% FREE)**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key (no payment method required)
4. **Daily limits**: Very generous, essentially unlimited for most users
5. Add to `.env`: `GEMINI_API_KEY=your_key_here`

### **Option 2: Groq (FREE Alternative)**
1. Visit: https://console.groq.com/
2. Sign up for free account
3. Generate API key
4. Add to `.env`: `GROQ_API_KEY=your_key_here`

### **Option 3: OpenAI (Paid)**
1. Visit: https://platform.openai.com/api-keys
2. Create account and add payment method
3. Generate API key
4. Add to `.env`: `OPENAI_API_KEY=your_key_here`

---

## 🎮 **Usage Examples**

### **Basic Web Search**
```python
import asyncio
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

async def search_web():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    agent = Agent(
        task="Search Google for 'Python tutorials' and summarize top 3 results",
        llm=llm
    )
    
    result = await agent.arun()
    print(result)

asyncio.run(search_web())
```

### **Form Filling**
```python
async def fill_form():
    agent = Agent(
        task="Go to contact form at example.com, fill with name 'John Doe', email 'john@example.com', and submit",
        llm=llm
    )
    
    result = await agent.arun()
    print(result)
```

### **Data Extraction**
```python
async def extract_data():
    agent = Agent(
        task="Go to news.ycombinator.com and extract the titles of top 10 articles",
        llm=llm
    )
    
    result = await agent.arun()
    print(result)
```

---

## 🛠️ **Advanced Configuration**

### **Environment Variables (.env)**
```env
# Required: Choose ONE LLM provider
GEMINI_API_KEY=your_gemini_key_here
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_claude_key_here
# GROQ_API_KEY=your_groq_key_here

# Optional: Browser settings
HEADLESS=false          # true for background mode
BROWSER_SLOW_MO=1000   # Milliseconds delay between actions
BROWSER_TIMEOUT=30000  # Page load timeout

# Optional: Logging
LOG_LEVEL=INFO
```

### **Browser Configuration**
```python
from browser_use.browser.browser import Browser

# Custom browser settings
browser = Browser(
    headless=True,        # Run in background
    slow_mo=500,         # Slow down actions
    timeout=30000,       # Page timeout
    viewport_size={"width": 1920, "height": 1080}
)
```

---

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Python Version Error**
```
Error: Python 3.11+ required
```
**Solution**: Upgrade Python from https://python.org/downloads/

#### **2. UV Installation Failed**  
```
Error: 'uv' is not recognized
```
**Solution**: 
- Windows: `pip install uv`
- Add to PATH or restart terminal

#### **3. Chromium Installation Failed**
```
Error: Failed to install Chromium
```
**Solution**:
```bash
python -m playwright install chromium
# Or manually download Chromium
```

#### **4. API Key Not Working**
```
Error: Invalid API key
```
**Solution**:
- Check `.env` file format (no quotes around key)
- Verify key is active in provider dashboard
- Ensure no extra spaces/characters

#### **5. Import Errors**
```
Error: No module named 'browser_use'
```
**Solution**:
```bash
pip install --upgrade browser-use
# Or
uv pip install --upgrade browser-use
```

#### **6. Browser Not Opening**
```
Error: Browser failed to start
```
**Solution**:
- Check if Chromium is installed: `playwright install chromium`
- Run with `headless=False` to see browser
- Check firewall/antivirus settings

---

## 🎯 **Best Practices**

### **1. Performance Optimization**
- Use `headless=True` for faster execution
- Set appropriate timeouts
- Close browser instances properly

### **2. Error Handling**
```python
try:
    result = await agent.arun()
except Exception as e:
    print(f"Automation failed: {e}")
    # Handle gracefully
```

### **3. Rate Limiting**
- Add delays between requests
- Use `slow_mo` parameter for debugging
- Respect website rate limits

### **4. Security**
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly

---

## 📚 **Advanced Features**

### **1. Multi-tab Operations**
```python
agent = Agent(
    task="Open 3 tabs: Google, GitHub, and Stack Overflow. Search for 'AI automation' in each.",
    llm=llm
)
```

### **2. File Downloads**
```python
agent = Agent(
    task="Go to example.com/files and download all PDF files to the Downloads folder",
    llm=llm
)
```

### **3. Screenshot Capture**
```python
agent = Agent(
    task="Go to example.com, take a screenshot, and save it as 'page.png'",
    llm=llm
)
```

### **4. Cookie Management**
```python
from browser_use.browser.browser import Browser

browser = Browser(
    user_data_dir="./user_data"  # Persistent browser session
)
```

---

## 🔗 **Resources & Support**

### **Official Links**
- **Documentation**: https://browser-use.com
- **GitHub Repository**: https://github.com/browser-use/browser-use  
- **Discord Community**: https://discord.gg/browser-use
- **Examples**: https://github.com/browser-use/browser-use/tree/main/examples

### **API Provider Links**
- **Gemini API (FREE)**: https://makersuite.google.com/app/apikey
- **Groq API (FREE)**: https://console.groq.com/
- **OpenAI API**: https://platform.openai.com/api-keys
- **Anthropic Claude**: https://console.anthropic.com/

### **Learning Resources**
- **Playwright Documentation**: https://playwright.dev/python/
- **LangChain Documentation**: https://python.langchain.com/
- **Browser Automation Patterns**: https://github.com/microsoft/playwright

---

## ✅ **Quick Start Checklist**

- [ ] Python 3.11+ installed
- [ ] UV package manager installed
- [ ] Browser-use package installed
- [ ] Chromium browser installed
- [ ] .env file created
- [ ] API key obtained and configured
- [ ] Demo script tested successfully
- [ ] Advanced features explored

---

## 🎉 **You're Ready!**

Congratulations! You now have unlimited FREE browser automation powered by AI. Start with simple tasks and gradually explore more complex automation scenarios.

**Need help?** Join the Discord community or check the GitHub issues for support.

**Happy Automating! 🚀**