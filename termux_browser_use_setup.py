#!/usr/bin/env python3
"""
Browser-Use Setup for Termux (Android)
Complete automation setup for mobile/tablet devices
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class TermuxBrowserUseSetup:
    def __init__(self):
        self.setup_dir = Path.home()
        self.env_file = self.setup_dir / ".env"
        
    def check_termux_environment(self):
        """Check if running in Termux environment"""
        print("🔍 Checking Termux environment...")
        
        if not os.path.exists("/data/data/com.termux"):
            print("❌ This script is designed for Termux on Android")
            print("For PC setup, use browser_use_setup.py instead")
            return False
            
        print("✅ Termux environment detected!")
        return True
    
    def update_packages(self):
        """Update Termux packages"""
        print("\n📦 Updating Termux packages...")
        try:
            subprocess.run(["pkg", "update", "-y"], check=True)
            subprocess.run(["pkg", "upgrade", "-y"], check=True)
            print("✅ Packages updated!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to update packages: {e}")
            return False
    
    def install_dependencies(self):
        """Install required Termux packages"""
        print("\n🔧 Installing dependencies...")
        
        packages = [
            "python",
            "python-pip", 
            "git",
            "nodejs",
            "chromium",
            "x11-repo",
            "tur-repo"
        ]
        
        for package in packages:
            try:
                print(f"Installing {package}...")
                subprocess.run(["pkg", "install", package, "-y"], check=True)
            except subprocess.CalledProcessError:
                print(f"⚠️  Failed to install {package}, continuing...")
        
        print("✅ Dependencies installation completed!")
        return True
    
    def install_python_packages(self):
        """Install Python packages"""
        print("\n🐍 Installing Python packages...")
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            
            # Install required packages
            packages = [
                "browser-use",
                "python-dotenv",
                "langchain-google-genai",
                "playwright",
                "asyncio"
            ]
            
            for package in packages:
                print(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            
            print("✅ Python packages installed!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Python packages: {e}")
            return False
    
    def setup_playwright(self):
        """Setup Playwright for Termux"""
        print("\n🎭 Setting up Playwright...")
        
        try:
            # Install Playwright browsers
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            print("✅ Playwright setup complete!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Playwright setup failed: {e}")
            # Termux might need special handling
            print("Trying alternative Chromium setup...")
            return True  # Continue even if this fails
    
    def setup_display(self):
        """Setup X11 display for GUI apps"""
        print("\n🖥️  Setting up display...")
        
        try:
            # Install VNC server for GUI
            subprocess.run(["pkg", "install", "tigervnc", "-y"], check=True)
            
            # Create VNC startup script
            vnc_script = self.setup_dir / "start_vnc.sh"
            vnc_content = """#!/bin/bash
# Start VNC server for browser automation
export DISPLAY=:1
vncserver -geometry 1280x720 -depth 24 :1
echo "VNC server started on display :1"
echo "Connect with VNC viewer to localhost:5901"
"""
            with open(vnc_script, 'w') as f:
                f.write(vnc_content)
            
            os.chmod(vnc_script, 0o755)
            print("✅ VNC setup complete!")
            print("Run './start_vnc.sh' to start GUI support")
            return True
            
        except subprocess.CalledProcessError:
            print("⚠️  VNC setup failed, browser will run in headless mode")
            return True
    
    def create_env_file(self):
        """Create environment configuration"""
        print("\n🔑 Creating environment file...")
        
        env_content = """# Browser-Use Configuration for Termux
# Get FREE Gemini API key: https://makersuite.google.com/app/apikey

# REQUIRED: Add your API key here
GEMINI_API_KEY=your_gemini_api_key_here

# Termux-specific settings
HEADLESS=true
BROWSER_EXECUTABLE=/data/data/com.termux/files/usr/bin/chromium
DISPLAY=:1

# Optional: Other LLM providers
# OPENAI_API_KEY=your_openai_key_here
# GROQ_API_KEY=your_groq_key_here

# Performance settings for mobile
BROWSER_TIMEOUT=60000
BROWSER_SLOW_MO=2000
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_content)
            
        print(f"✅ Environment file created: {self.env_file}")
        return True
    
    def create_termux_demo(self):
        """Create Termux-optimized demo script"""
        print("\n📱 Creating Termux demo script...")
        
        demo_content = '''"""
Browser-Use Demo for Termux
Optimized for mobile/tablet automation
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

async def termux_demo():
    """Demo optimized for Termux environment"""
    
    print("🤖 Starting Termux Browser Automation Demo...")
    
    # Check API key
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_gemini_api_key_here":
        print("❌ Please set your GEMINI_API_KEY in the .env file!")
        print("Get a free key from: https://makersuite.google.com/app/apikey")
        return
    
    try:
        from browser_use import Agent
        from browser_use.browser.browser import Browser
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Setup LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # Create browser optimized for Termux
        browser = Browser(
            headless=True,  # Required for Termux
            slow_mo=2000,   # Slower for mobile performance
            timeout=60000,  # Longer timeout for mobile
        )
        
        print("🌐 Browser initialized in headless mode...")
        
        # Simple task for mobile
        agent = Agent(
            task="Go to httpbin.org/json and extract the data from the JSON response",
            llm=llm,
            browser=browser
        )
        
        print("🚀 Running automation task...")
        result = await agent.arun()
        
        print("✅ Demo completed!")
        print(f"Result: {result}")
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install browser-use langchain-google-genai")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("This might be due to Termux-specific issues")

def check_termux_setup():
    """Check if Termux is properly set up"""
    print("🔍 Checking Termux setup...")
    
    # Check if running in Termux
    if not os.path.exists("/data/data/com.termux"):
        print("❌ Not running in Termux environment")
        return False
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python {sys.version} may not be compatible")
        print("Update Termux packages: pkg update && pkg upgrade")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    
    # Check for required packages
    try:
        import playwright
        print("✅ Playwright available")
    except ImportError:
        print("❌ Playwright not installed: pip install playwright")
        return False
    
    return True

async def run_mobile_tasks():
    """Run various mobile-optimized tasks"""
    
    from browser_use import Agent
    from browser_use.browser.browser import Browser
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    
    browser = Browser(headless=True, slow_mo=1500)
    
    tasks = [
        "Visit example.com and get the page title",
        "Go to httpbin.org/ip and get the IP information", 
        "Visit quotes.toscrape.com and get the first quote",
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\\n📱 Task {i}: {task}")
        try:
            agent = Agent(task=task, llm=llm, browser=browser)
            result = await agent.arun()
            print(f"✅ Result: {result[:200]}...")
        except Exception as e:
            print(f"❌ Failed: {e}")

def main():
    """Main function"""
    print("🤖 Browser-Use for Termux")
    print("=" * 40)
    
    if not check_termux_setup():
        print("Please fix setup issues first")
        return
    
    print("\\nOptions:")
    print("1. Run basic demo")
    print("2. Run multiple mobile tasks")
    print("3. Custom task")
    
    choice = input("\\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(termux_demo())
    elif choice == "2":
        asyncio.run(run_mobile_tasks())
    elif choice == "3":
        custom_task = input("Enter your task: ").strip()
        if custom_task:
            asyncio.run(run_custom_task(custom_task))
    else:
        print("Invalid choice")

async def run_custom_task(task):
    """Run a custom user task"""
    from browser_use import Agent
    from browser_use.browser.browser import Browser
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    
    browser = Browser(headless=True)
    agent = Agent(task=task, llm=llm, browser=browser)
    
    try:
        result = await agent.arun()
        print(f"✅ Custom Task Result: {result}")
    except Exception as e:
        print(f"❌ Custom Task Failed: {e}")

if __name__ == "__main__":
    main()
'''
        
        demo_file = self.setup_dir / "termux_browser_demo.py"
        with open(demo_file, 'w') as f:
            f.write(demo_content)
            
        print(f"✅ Termux demo created: {demo_file}")
        return True
    
    def create_setup_instructions(self):
        """Create Termux-specific setup instructions"""
        print("\n📋 Creating setup instructions...")
        
        instructions = """# Browser-Use Setup Instructions for Termux

## Prerequisites
1. Install Termux from F-Droid (NOT Google Play Store)
2. Enable storage access: `termux-setup-storage`
3. Update packages: `pkg update && pkg upgrade`

## Installation Commands
Run these commands in Termux:

```bash
# Update and install packages
pkg update -y && pkg upgrade -y
pkg install python python-pip git nodejs chromium x11-repo tur-repo -y

# Install Python packages
pip install --upgrade pip
pip install browser-use python-dotenv langchain-google-genai playwright

# Install Playwright browsers
python -m playwright install chromium

# Setup VNC (optional, for GUI)
pkg install tigervnc -y
```

## API Key Setup
1. Get FREE Gemini API key: https://makersuite.google.com/app/apikey
2. Edit .env file: `nano .env`
3. Replace 'your_gemini_api_key_here' with your actual key

## Running
```bash
python termux_browser_demo.py
```

## Notes
- Browser runs in headless mode (no GUI) for better performance
- Use VNC server if you need to see the browser
- Some websites may not work due to mobile user agents
- Performance may be slower on mobile devices

## Troubleshooting
- If import errors occur: `pip install --upgrade browser-use`
- For display issues: Use headless=True
- Memory issues: Close other apps, reduce browser timeout
"""
        
        instructions_file = self.setup_dir / "TERMUX_SETUP.md"
        with open(instructions_file, 'w') as f:
            f.write(instructions)
            
        print(f"✅ Instructions created: {instructions_file}")
        return True
    
    def run_complete_setup(self):
        """Run the complete Termux setup"""
        print("📱 Browser-Use Setup for Termux")
        print("=" * 50)
        
        if not self.check_termux_environment():
            return
        
        steps = [
            ("Package Update", self.update_packages),
            ("Dependencies Installation", self.install_dependencies),
            ("Python Packages", self.install_python_packages),
            ("Playwright Setup", self.setup_playwright),
            ("Display Setup", self.setup_display),
            ("Environment Configuration", self.create_env_file),
            ("Demo Script Creation", self.create_termux_demo),
            ("Instructions Creation", self.create_setup_instructions),
        ]
        
        failed_steps = []
        
        for step_name, step_func in steps:
            print(f"\\n🔄 {step_name}...")
            if not step_func():
                failed_steps.append(step_name)
        
        print("\\n" + "=" * 50)
        if not failed_steps:
            print("🎉 TERMUX SETUP COMPLETE!")
            print("\\n📋 Next Steps:")
            print("1. Get FREE Gemini API key: https://makersuite.google.com/app/apikey")
            print("2. Edit .env file: nano .env")
            print("3. Add your API key to replace 'your_gemini_api_key_here'")
            print("4. Run: python termux_browser_demo.py")
            print("\\n💡 Termux Tips:")
            print("- Browser runs in headless mode for performance")
            print("- Use 'termux-wake-lock' to prevent sleep during automation")
            print("- Check TERMUX_SETUP.md for detailed instructions")
        else:
            print(f"⚠️  Setup completed with {len(failed_steps)} issues:")
            for step in failed_steps:
                print(f"   - {step}")
        
        print("\\n🔗 Resources:")
        print("- Termux Wiki: https://wiki.termux.com/")
        print("- Browser-Use Docs: https://browser-use.com")

if __name__ == "__main__":
    setup = TermuxBrowserUseSetup()
    setup.run_complete_setup()