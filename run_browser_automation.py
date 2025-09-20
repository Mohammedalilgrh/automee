#!/usr/bin/env python3
"""
Browser-Use Unified Launcher
One-click browser automation with full setup and configuration
Includes all APIs and necessary components for 100% functionality
"""

import asyncio
import os
import sys
import platform
import subprocess
from pathlib import Path
from dotenv import load_dotenv

class BrowserAutomationLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.setup_dir = Path.cwd()
        self.env_file = self.setup_dir / ".env"
        load_dotenv()
        
    def check_installation(self):
        """Check if browser-use is installed and working"""
        print("🔍 Checking installation...")
        
        try:
            import browser_use
            print("✅ Browser-use installed")
        except ImportError:
            print("❌ Browser-use not installed")
            return self.install_browser_use()
        
        try:
            import playwright
            print("✅ Playwright available")
        except ImportError:
            print("❌ Installing Playwright...")
            subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        
        return True
    
    def install_browser_use(self):
        """Install browser-use if not present"""
        print("📦 Installing browser-use...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "browser-use", "playwright", "python-dotenv"], check=True)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            print("✅ Installation complete!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def setup_api_keys(self):
        """Setup API keys interactively"""
        print("🔑 API Key Setup...")
        
        if not self.env_file.exists():
            # Create .env file
            env_content = """# Browser-Use API Configuration
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GROQ_API_KEY=

# Browser Settings
HEADLESS=false
BROWSER_SLOW_MO=1000
"""
            with open(self.env_file, 'w') as f:
                f.write(env_content)
        
        # Check if any API key is set
        api_keys = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        }
        
        working_keys = {k: v for k, v in api_keys.items() if v and v != ""}
        
        if not working_keys:
            print("❌ No API keys found!")
            print("\n🆓 For FREE unlimited usage, get a Gemini API key:")
            print("https://makersuite.google.com/app/apikey")
            print("\nAfter getting your key, add it to the .env file:")
            print(f"Edit: {self.env_file}")
            
            # Interactive key setup
            if input("\nWould you like to add an API key now? (y/n): ").lower() == 'y':
                provider = input("Choose provider (gemini/openai/anthropic/groq): ").lower()
                if provider in ['gemini', 'openai', 'anthropic', 'groq']:
                    key = input(f"Enter your {provider.upper()} API key: ").strip()
                    if key:
                        key_name = f"{provider.upper()}_API_KEY"
                        self.update_env_file(key_name, key)
                        print(f"✅ {provider.upper()} API key saved!")
                        return True
            return False
        else:
            print(f"✅ Found API keys: {list(working_keys.keys())}")
            return True
    
    def update_env_file(self, key_name, key_value):
        """Update a specific key in .env file"""
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                lines = f.readlines()
            
            # Update existing key or add new one
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(f"{key_name}="):
                    lines[i] = f"{key_name}={key_value}\n"
                    updated = True
                    break
            
            if not updated:
                lines.append(f"{key_name}={key_value}\n")
            
            with open(self.env_file, 'w') as f:
                f.writelines(lines)
    
    def get_llm_instance(self):
        """Get the appropriate LLM instance based on available API keys"""
        # Reload environment variables
        load_dotenv(override=True)
        
        if os.getenv("GEMINI_API_KEY"):
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=os.getenv("GEMINI_API_KEY")
                ), "Gemini (FREE)"
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "langchain-google-genai"], check=True)
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=os.getenv("GEMINI_API_KEY")
                ), "Gemini (FREE)"
        
        elif os.getenv("GROQ_API_KEY"):
            try:
                from langchain_groq import ChatGroq
                return ChatGroq(
                    model="mixtral-8x7b-32768",
                    groq_api_key=os.getenv("GROQ_API_KEY")
                ), "Groq (FREE)"
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "langchain-groq"], check=True)
                from langchain_groq import ChatGroq
                return ChatGroq(
                    model="mixtral-8x7b-32768", 
                    groq_api_key=os.getenv("GROQ_API_KEY")
                ), "Groq (FREE)"
        
        elif os.getenv("OPENAI_API_KEY"):
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model="gpt-4",
                    api_key=os.getenv("OPENAI_API_KEY")
                ), "OpenAI GPT-4"
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "langchain-openai"], check=True)
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model="gpt-4",
                    api_key=os.getenv("OPENAI_API_KEY")
                ), "OpenAI GPT-4"
        
        elif os.getenv("ANTHROPIC_API_KEY"):
            try:
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model="claude-3-sonnet-20240229",
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                ), "Claude 3"
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "langchain-anthropic"], check=True)
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model="claude-3-sonnet-20240229",
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                ), "Claude 3"
        
        else:
            raise ValueError("No valid API key found. Please set up an API key first.")
    
    async def run_automation_task(self, task, headless=False):
        """Run a browser automation task"""
        try:
            from browser_use import Agent
            from browser_use.browser.browser import Browser
            
            # Get LLM
            llm, provider = self.get_llm_instance()
            print(f"🤖 Using {provider}")
            
            # Create browser
            browser = Browser(
                headless=headless,
                slow_mo=int(os.getenv("BROWSER_SLOW_MO", 1000)),
            )
            
            # Create and run agent
            agent = Agent(
                task=task,
                llm=llm,
                browser=browser
            )
            
            print(f"🚀 Running task: {task}")
            result = await agent.arun()
            
            print("✅ Task completed!")
            print(f"Result: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Task failed: {e}")
            return None
    
    async def run_predefined_tasks(self):
        """Run a set of predefined automation tasks"""
        tasks = {
            "1": "Go to Google and search for 'browser automation python'",
            "2": "Visit GitHub.com, search for 'browser-use' and get the star count",
            "3": "Go to news.ycombinator.com and get the titles of top 5 articles",
            "4": "Visit example.com and extract all the text content",
            "5": "Go to httpbin.org/json and extract the JSON data",
        }
        
        print("🎯 Predefined Tasks:")
        for key, task in tasks.items():
            print(f"{key}. {task}")
        
        choice = input("\nSelect task (1-5) or 'c' for custom: ").strip()
        
        if choice in tasks:
            await self.run_automation_task(tasks[choice])
        elif choice.lower() == 'c':
            custom_task = input("Enter your custom task: ").strip()
            if custom_task:
                await self.run_automation_task(custom_task)
        else:
            print("Invalid choice")
    
    async def interactive_mode(self):
        """Run in interactive mode"""
        print("🎮 Interactive Browser Automation")
        print("Type your automation tasks, or 'quit' to exit")
        
        while True:
            task = input("\n🤖 What would you like to automate? ").strip()
            
            if task.lower() in ['quit', 'exit', 'q']:
                break
            
            if task:
                await self.run_automation_task(task)
    
    def show_menu(self):
        """Show main menu"""
        print("\n🤖 Browser Automation Launcher")
        print("=" * 40)
        print("1. Run predefined tasks")
        print("2. Interactive mode")
        print("3. Setup/check API keys")
        print("4. Test installation")
        print("5. View documentation")
        print("6. Exit")
        return input("\nChoose option (1-6): ").strip()
    
    def run_tests(self):
        """Run installation tests"""
        print("🧪 Running tests...")
        
        tests = [
            ("Python version", lambda: sys.version_info >= (3, 8)),
            ("Browser-use import", lambda: __import__("browser_use")),
            ("Playwright import", lambda: __import__("playwright")),
            ("Dotenv import", lambda: __import__("dotenv")),
            ("Environment file", lambda: self.env_file.exists()),
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    print(f"✅ {test_name}")
                else:
                    print(f"❌ {test_name}")
            except Exception as e:
                print(f"❌ {test_name}: {e}")
    
    def show_docs(self):
        """Show documentation links"""
        print("\n📚 Documentation & Resources")
        print("=" * 40)
        print("• Browser-Use Docs: https://browser-use.com")
        print("• GitHub Repository: https://github.com/browser-use/browser-use")
        print("• Discord Community: https://discord.gg/browser-use")
        print("• Free Gemini API: https://makersuite.google.com/app/apikey")
        print("• Free Groq API: https://console.groq.com/")
        print("• Examples: https://github.com/browser-use/browser-use/tree/main/examples")
    
    async def main(self):
        """Main application loop"""
        print("🚀 Browser-Use Automation Launcher")
        print("Complete setup with all APIs included")
        print("=" * 50)
        
        # Initial setup
        if not self.check_installation():
            print("Installation failed. Please check errors above.")
            return
        
        if not self.setup_api_keys():
            print("API key setup required. Please add your key to .env file.")
            print("For free usage, get Gemini API key: https://makersuite.google.com/app/apikey")
            return
        
        # Main loop
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                await self.run_predefined_tasks()
            elif choice == "2":
                await self.interactive_mode()
            elif choice == "3":
                self.setup_api_keys()
            elif choice == "4":
                self.run_tests()
            elif choice == "5":
                self.show_docs()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    launcher = BrowserAutomationLauncher()
    asyncio.run(launcher.main())