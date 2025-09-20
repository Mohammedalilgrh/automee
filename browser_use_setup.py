#!/usr/bin/env python3
"""
Browser-Use Automation Agent Setup and Launcher
Complete setup script for unlimited free browser automation
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from typing import Optional

class BrowserUseSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.setup_dir = Path.cwd()
        self.env_file = self.setup_dir / ".env"
        
    def check_python_version(self):
        """Check if Python version meets requirements"""
        print("🔍 Checking Python version...")
        if self.python_version < (3, 11):
            print(f"❌ Python 3.11+ required. Current version: {sys.version}")
            print("Please upgrade Python to 3.11 or higher")
            return False
        print(f"✅ Python {sys.version.split()[0]} - Compatible!")
        return True
    
    def install_uv(self):
        """Install UV package manager"""
        print("\n📦 Installing UV package manager...")
        try:
            # Check if uv is already installed
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
            print("✅ UV already installed!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        try:
            if self.system == "windows":
                # Install via pip as fallback for Windows
                subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
            else:
                # Unix systems - use curl installer
                subprocess.run([
                    "curl", "-LsSf", "https://astral.sh/uv/install.sh"
                ], check=True, shell=True)
            
            print("✅ UV installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install UV: {e}")
            print("Please install UV manually from: https://github.com/astral-sh/uv")
            return False
    
    def install_browser_use(self):
        """Install browser-use package"""
        print("\n🌐 Installing browser-use...")
        try:
            subprocess.run(["uv", "pip", "install", "browser-use"], check=True)
            print("✅ Browser-use installed successfully!")
            return True
        except subprocess.CalledProcessError:
            # Fallback to regular pip
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "browser-use"], check=True)
                print("✅ Browser-use installed successfully (via pip)!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install browser-use: {e}")
                return False
    
    def install_chromium(self):
        """Install Chromium via Playwright"""
        print("\n🌍 Installing Chromium browser...")
        try:
            subprocess.run([
                "uvx", "playwright", "install", "chromium", "--with-deps", "--no-shell"
            ], check=True)
            print("✅ Chromium installed successfully!")
            return True
        except subprocess.CalledProcessError:
            # Fallback method
            try:
                subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
                print("✅ Chromium installed successfully (fallback method)!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Chromium: {e}")
                print("Please install manually: python -m playwright install chromium")
                return False
    
    def setup_env_file(self):
        """Setup environment file with API keys"""
        print("\n🔑 Setting up environment variables...")
        
        if self.env_file.exists():
            print("✅ .env file already exists!")
            return True
        
        print("Creating .env file for API keys...")
        env_content = """# Browser-Use Environment Configuration
# Get your FREE Gemini API key from: https://makersuite.google.com/app/apikey

# REQUIRED: Choose ONE of the following LLM providers
GEMINI_API_KEY=your_gemini_api_key_here

# OPTIONAL: Alternative LLM providers (uncomment and add key if preferred)
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# GROQ_API_KEY=your_groq_api_key_here

# OPTIONAL: Browser settings
# HEADLESS=false  # Set to true for headless mode
# BROWSER_SLOW_MO=1000  # Milliseconds to slow down browser actions

# OPTIONAL: Logging
# LOG_LEVEL=INFO
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created .env file at: {self.env_file}")
        print("\n🚨 IMPORTANT: You need to add your API key to the .env file!")
        print("For FREE unlimited usage, get a Gemini API key from:")
        print("https://makersuite.google.com/app/apikey")
        return True
    
    def create_demo_script(self):
        """Create a demo script to test the installation"""
        print("\n📝 Creating demo script...")
        
        demo_content = '''"""
Browser-Use Demo Script
Run this after setting up your API key in .env
"""

import asyncio
from browser_use import Agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def demo_search():
    """Demo: Search for browser-use GitHub repo and get star count"""
    
    # Check if API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Please set your GEMINI_API_KEY in the .env file!")
        print("Get a free key from: https://makersuite.google.com/app/apikey")
        return
    
    print("🚀 Starting browser automation demo...")
    
    try:
        # Import the appropriate chat model
        from browser_use.browser.browser import Browser
        from browser_use.agent.service import Agent
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # Create browser instance
        browser = Browser()
        
        # Create agent
        agent = Agent(
            task="Go to GitHub, search for 'browser-use' repository, and tell me how many stars it has",
            llm=llm,
            browser=browser
        )
        
        # Run the agent
        result = await agent.arun()
        print(f"✅ Demo completed! Result: {result}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("This might be due to missing dependencies or API key issues.")

def run_demo():
    """Run the demo"""
    asyncio.run(demo_search())

if __name__ == "__main__":
    print("🤖 Browser-Use Demo")
    print("Make sure you've set your GEMINI_API_KEY in .env first!")
    
    choice = input("Press Enter to run demo, or 'q' to quit: ")
    if choice.lower() != 'q':
        run_demo()
'''
        
        demo_file = self.setup_dir / "demo_browser_use.py"
        with open(demo_file, 'w') as f:
            f.write(demo_content)
        
        print(f"✅ Demo script created: {demo_file}")
        return True
    
    def create_advanced_script(self):
        """Create an advanced usage script"""
        print("\n🎯 Creating advanced usage script...")
        
        advanced_content = '''"""
Advanced Browser-Use Script
Demonstrates various automation capabilities
"""

import asyncio
import os
from pathlib import Path
from browser_use import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BrowserAutomation:
    def __init__(self):
        self.setup_llm()
    
    def setup_llm(self):
        """Setup the Language Model"""
        if os.getenv("GEMINI_API_KEY"):
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
            print("✅ Using Gemini API (FREE)")
        elif os.getenv("OPENAI_API_KEY"):
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model="gpt-4",
                api_key=os.getenv("OPENAI_API_KEY")
            )
            print("✅ Using OpenAI API")
        else:
            raise ValueError("No API key found! Please set GEMINI_API_KEY or OPENAI_API_KEY in .env")
    
    async def web_search_task(self, query: str):
        """Perform web search and extraction"""
        from browser_use.browser.browser import Browser
        from browser_use.agent.service import Agent
        
        browser = Browser(headless=False)  # Set to True for headless mode
        
        agent = Agent(
            task=f"Search Google for '{query}' and summarize the top 3 results",
            llm=self.llm,
            browser=browser
        )
        
        result = await agent.arun()
        return result
    
    async def form_filling_task(self, form_data: dict):
        """Demonstrate form filling capabilities"""
        from browser_use.browser.browser import Browser
        from browser_use.agent.service import Agent
        
        browser = Browser(headless=False)
        
        task_description = f"""
        Go to a demo form website and fill out the form with this information:
        {form_data}
        Then submit the form.
        """
        
        agent = Agent(
            task=task_description,
            llm=self.llm,
            browser=browser
        )
        
        result = await agent.arun()
        return result
    
    async def data_extraction_task(self, url: str, data_to_extract: str):
        """Extract specific data from a website"""
        from browser_use.browser.browser import Browser
        from browser_use.agent.service import Agent
        
        browser = Browser(headless=True)  # Headless for data extraction
        
        agent = Agent(
            task=f"Go to {url} and extract: {data_to_extract}. Return the data in a structured format.",
            llm=self.llm,
            browser=browser
        )
        
        result = await agent.arun()
        return result
    
    async def multi_tab_task(self):
        """Demonstrate multi-tab operations"""
        from browser_use.browser.browser import Browser
        from browser_use.agent.service import Agent
        
        browser = Browser(headless=False)
        
        task = """
        Open multiple tabs:
        1. Tab 1: Go to GitHub and search for 'browser-use'
        2. Tab 2: Go to Python.org and check the latest Python version
        3. Tab 3: Go to Stack Overflow and search for 'web automation'
        
        Then provide a summary of what you found in each tab.
        """
        
        agent = Agent(
            task=task,
            llm=self.llm,
            browser=browser
        )
        
        result = await agent.arun()
        return result

async def main():
    """Main function to run different automation tasks"""
    automation = BrowserAutomation()
    
    print("🤖 Advanced Browser Automation")
    print("Choose a task:")
    print("1. Web Search & Summarization")
    print("2. Form Filling Demo")
    print("3. Data Extraction")
    print("4. Multi-tab Operations")
    print("5. Custom Task")
    
    choice = input("Enter your choice (1-5): ")
    
    try:
        if choice == "1":
            query = input("Enter search query: ") or "browser automation python"
            result = await automation.web_search_task(query)
            print(f"\\n✅ Search Results:\\n{result}")
        
        elif choice == "2":
            form_data = {
                "name": "Test User",
                "email": "test@example.com",
                "message": "This is a test message from browser-use automation"
            }
            result = await automation.form_filling_task(form_data)
            print(f"\\n✅ Form Filling Result:\\n{result}")
        
        elif choice == "3":
            url = input("Enter URL to extract data from: ") or "https://news.ycombinator.com"
            data_to_extract = input("What data to extract: ") or "top 5 article titles"
            result = await automation.data_extraction_task(url, data_to_extract)
            print(f"\\n✅ Extracted Data:\\n{result}")
        
        elif choice == "4":
            result = await automation.multi_tab_task()
            print(f"\\n✅ Multi-tab Results:\\n{result}")
        
        elif choice == "5":
            custom_task = input("Enter your custom task: ")
            if custom_task:
                from browser_use.browser.browser import Browser
                from browser_use.agent.service import Agent
                
                browser = Browser(headless=False)
                agent = Agent(
                    task=custom_task,
                    llm=automation.llm,
                    browser=browser
                )
                result = await agent.arun()
                print(f"\\n✅ Custom Task Result:\\n{result}")
        
        else:
            print("Invalid choice!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your API key is set correctly in the .env file")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        advanced_file = self.setup_dir / "advanced_browser_use.py"
        with open(advanced_file, 'w') as f:
            f.write(advanced_content)
        
        print(f"✅ Advanced script created: {advanced_file}")
        return True
    
    def run_full_setup(self):
        """Run the complete setup process"""
        print("🚀 Browser-Use Complete Setup")
        print("=" * 50)
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("UV Package Manager", self.install_uv),
            ("Browser-Use Installation", self.install_browser_use),
            ("Chromium Installation", self.install_chromium),
            ("Environment Setup", self.setup_env_file),
            ("Demo Script Creation", self.create_demo_script),
            ("Advanced Script Creation", self.create_advanced_script),
        ]
        
        failed_steps = []
        
        for step_name, step_func in steps:
            if not step_func():
                failed_steps.append(step_name)
        
        print("\n" + "=" * 50)
        if not failed_steps:
            print("🎉 SETUP COMPLETE! Browser-Use is ready for unlimited automation!")
            print("\n📋 Next Steps:")
            print("1. Get your FREE Gemini API key: https://makersuite.google.com/app/apikey")
            print("2. Add it to the .env file (replace 'your_gemini_api_key_here')")
            print("3. Run: python demo_browser_use.py")
            print("4. For advanced features: python advanced_browser_use.py")
            print("\n💡 Tips:")
            print("- Gemini API is completely FREE with no usage limits")
            print("- Use headless=True for faster, background automation")
            print("- Check the .env file for more configuration options")
        else:
            print(f"⚠️  Setup completed with {len(failed_steps)} issues:")
            for step in failed_steps:
                print(f"   - {step}")
            print("\nPlease resolve these issues and try again.")
        
        print("\n🔗 Resources:")
        print("- Documentation: https://browser-use.com")
        print("- GitHub: https://github.com/browser-use/browser-use")
        print("- Discord: https://discord.gg/browser-use")

if __name__ == "__main__":
    setup = BrowserUseSetup()
    setup.run_full_setup()