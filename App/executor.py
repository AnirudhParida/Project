import os
import shutil
import webbrowser
import subprocess
import pyautogui
from pathlib import Path


class ActionExecutor:
    """Executes OS-level commands based on parsed intents."""

    def __init__(self):
        self.results = []

    def execute(self, action, params):
        """
        Execute an action with given parameters.
        
        Args:
            action (str): The action to perform (e.g., 'open_app', 'create_file')
            params (dict): Parameters for the action
            
        Returns:
            str: Result message
        """
        action_map = {
            'open_app': self.open_app,
            'close_app': self.close_app,
            'create_file': self.create_file,
            'create_folder': self.create_folder,
            'delete_file': self.delete_file,
            'delete_folder': self.delete_folder,
            'search_web': self.search_web,
            'open_url': self.open_url,
            'run_command': self.run_command,
            'get_system_info': self.get_system_info,
            'take_screenshot': self.take_screenshot,
        }

        if action in action_map:
            try:
                result = action_map[action](params)
                return result
            except Exception as e:
                return f"Error executing {action}: {str(e)}"
        else:
            return f"Unknown action: {action}"

    def open_app(self, params):
        """Open an application."""
        app_name = params.get('app_name', '')
        
        # Common Windows applications
        app_paths = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'explorer': 'explorer.exe',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
        }
        
        app_lower = app_name.lower()
        
        # Check if it's a known app
        if app_lower in app_paths:
            try:
                subprocess.Popen(app_paths[app_lower])
                return f"Opening {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {str(e)}"
        else:
            # Try to open it directly
            try:
                subprocess.Popen(app_name)
                return f"Opening {app_name}"
            except Exception as e:
                return f"Could not find application: {app_name}"

    def close_app(self, params):
        """Close an application."""
        app_name = params.get('app_name', '')
        try:
            # Use taskkill command on Windows
            subprocess.run(['taskkill', '/F', '/IM', f'{app_name}.exe'], 
                         capture_output=True, text=True)
            return f"Closed {app_name}"
        except Exception as e:
            return f"Failed to close {app_name}: {str(e)}"

    def create_file(self, params):
        """Create a new file."""
        file_path = params.get('path', '')
        content = params.get('content', '')
        
        try:
            # Expand user path
            full_path = Path(file_path).expanduser()
            
            # Create parent directories if they don't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create the file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Created file: {full_path}"
        except Exception as e:
            return f"Failed to create file: {str(e)}"

    def create_folder(self, params):
        """Create a new folder."""
        folder_path = params.get('path', '')
        
        try:
            full_path = Path(folder_path).expanduser()
            full_path.mkdir(parents=True, exist_ok=True)
            return f"Created folder: {full_path}"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"

    def delete_file(self, params):
        """Delete a file (with confirmation)."""
        file_path = params.get('path', '')
        confirm = params.get('confirmed', False)
        
        if not confirm:
            return f"Please confirm deletion of: {file_path}"
        
        try:
            full_path = Path(file_path).expanduser()
            if full_path.exists() and full_path.is_file():
                full_path.unlink()
                return f"Deleted file: {full_path}"
            else:
                return f"File not found: {full_path}"
        except Exception as e:
            return f"Failed to delete file: {str(e)}"

    def delete_folder(self, params):
        """Delete a folder (with confirmation)."""
        folder_path = params.get('path', '')
        confirm = params.get('confirmed', False)
        
        if not confirm:
            return f"Please confirm deletion of folder: {folder_path}"
        
        try:
            full_path = Path(folder_path).expanduser()
            if full_path.exists() and full_path.is_dir():
                shutil.rmtree(full_path)
                return f"Deleted folder: {full_path}"
            else:
                return f"Folder not found: {full_path}"
        except Exception as e:
            return f"Failed to delete folder: {str(e)}"

    def search_web(self, params):
        """Search the web using default browser."""
        query = params.get('query', '')
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"Searching for: {query}"

    def open_url(self, params):
        """Open a URL in the default browser."""
        url = params.get('url', '')
        webbrowser.open(url)
        return f"Opening: {url}"

    def run_command(self, params):
        """Run a shell command."""
        command = params.get('command', '')
        confirm = params.get('confirmed', False)
        
        if not confirm:
            return f"Please confirm running command: {command}"
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                                  text=True, timeout=10)
            output = result.stdout if result.stdout else result.stderr
            return f"Command output: {output[:500]}"  # Limit output
        except Exception as e:
            return f"Failed to run command: {str(e)}"

    def get_system_info(self, params):
        """Get system information."""
        import platform
        info = f"OS: {platform.system()} {platform.release()}\n"
        info += f"Machine: {platform.machine()}\n"
        info += f"Processor: {platform.processor()}"
        return info

    def take_screenshot(self, params):
        """Take a screenshot."""
        filename = params.get('filename', 'screenshot.png')
        
        try:
            # Expand path
            full_path = Path(filename).expanduser()
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(full_path)
            
            return f"Screenshot saved to: {full_path}"
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"
