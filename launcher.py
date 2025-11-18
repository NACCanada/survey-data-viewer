"""
Windows Launcher for Survey Data Viewer
Handles startup, directory creation, browser launch, and graceful shutdown
"""

import os
import sys
import time
import threading
import webbrowser
from pathlib import Path

def get_base_path():
    """Get the base path for the application (works for both dev and bundled exe)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys._MEIPASS)
    else:
        # Running as script
        return Path(__file__).parent

def get_app_data_path():
    """Get the path where user data should be stored"""
    if getattr(sys, 'frozen', False):
        # When bundled, use the directory where the exe is located
        return Path(sys.executable).parent
    else:
        # When running as script, use current directory
        return Path(__file__).parent

def setup_directories():
    """Create necessary directories if they don't exist"""
    app_data = get_app_data_path()

    dirs = ['data', 'uploads']
    for dir_name in dirs:
        dir_path = app_data / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Directory ready: {dir_path}")

    return app_data

def open_browser(port=8080, delay=2):
    """Open the browser after a short delay"""
    time.sleep(delay)
    url = f'http://localhost:{port}'
    print(f"\n🌐 Opening browser: {url}")
    webbrowser.open(url)

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("     📊 Survey Data Viewer v3.0")
    print("=" * 60)
    print()

def print_instructions(port=8080):
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("✓ Server is running!")
    print("=" * 60)
    print(f"\n🌐 Access the application at: http://localhost:{port}")
    print("\n📌 Instructions:")
    print("   • Browser should open automatically")
    print("   • If not, copy the URL above into your browser")
    print("   • Press Ctrl+C to stop the server")
    print("\n💾 Your data is stored in:")
    print(f"   {get_app_data_path()}")
    print("\n" + "=" * 60 + "\n")

def main():
    """Main launcher function"""
    print_banner()

    # Setup directories
    print("📁 Setting up directories...")
    app_data = setup_directories()

    # Set environment variables for the Flask app
    os.environ['APP_DATA_PATH'] = str(app_data)

    # Import Flask app
    print("\n🚀 Starting Survey Data Viewer...")
    try:
        from app import app

        # Get port from environment or use default
        port = int(os.environ.get('PORT', 8080))

        # Start browser in background thread
        browser_thread = threading.Thread(target=open_browser, args=(port,))
        browser_thread.daemon = True
        browser_thread.start()

        # Print instructions
        print_instructions(port)

        # Start Flask app
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,
            use_reloader=False  # Disable reloader for exe
        )

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        print("   Thanks for using Survey Data Viewer!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\nPlease check:")
        print(f"  • Port {port} is not already in use")
        print("  • You have write permissions in this directory")
        print(f"  • Directory: {app_data}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
