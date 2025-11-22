import os
import json
import google.generativeai as genai
from pathlib import Path


class Brain:
    """Handles LLM-based intent parsing and command generation."""
    
    def __init__(self, api_key=None):
        """
        Initialize the Brain with LLM configuration.
        
        Args:
            api_key (str): Gemini API key. If None, reads from .env file
        """
        # Get API key
        if api_key is None:
            api_key = self._load_api_key()
        
        if not api_key or api_key == "your_api_key_here":
            raise ValueError(
                "Gemini API key not found! Please:\n"
                "1. Copy .env.example to .env\n"
                "2. Add your Gemini API key to .env\n"
                "Get your key at: https://makersuite.google.com/app/apikey"
            )
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # System prompt defines the agent's capabilities
        self.system_prompt = """You are an OS control agent. Your job is to convert user commands into structured actions.

Available Actions:
1. open_app - Open an application
   Params: {"app_name": "application name"}
   
2. close_app - Close an application
   Params: {"app_name": "application name"}
   
3. create_file - Create a new file
   Params: {"path": "file path", "content": "file content (optional)"}
   
4. create_folder - Create a new folder
   Params: {"path": "folder path"}
   
5. delete_file - Delete a file (requires confirmation)
   Params: {"path": "file path", "confirmed": false}
   
6. delete_folder - Delete a folder (requires confirmation)
   Params: {"path": "folder path", "confirmed": false}
   
7. search_web - Search on Google
   Params: {"query": "search query"}
   
8. open_url - Open a URL
   Params: {"url": "web address"}
   
9. run_command - Run a shell command (requires confirmation)
   Params: {"command": "shell command", "confirmed": false}
   
10. get_system_info - Get system information
    Params: {}
    
11. take_screenshot - Take a screenshot
    Params: {"filename": "screenshot.png"}

IMPORTANT RULES:
- Respond ONLY with valid JSON
- JSON format: {"action": "action_name", "params": {...}}
- For unclear commands, use: {"action": "clarify", "params": {"message": "clarification question"}}
- For greetings/chat, use: {"action": "respond", "params": {"message": "your response"}}

Examples:
User: "Open notepad"
Response: {"action": "open_app", "params": {"app_name": "notepad"}}

User: "Search for Python tutorials"
Response: {"action": "search_web", "params": {"query": "Python tutorials"}}

User: "Create a file called test.txt"
Response: {"action": "create_file", "params": {"path": "test.txt", "content": ""}}

User: "Hello"
Response: {"action": "respond", "params": {"message": "Hello! How can I help you control your system today?"}}

Now convert the user's command:
"""

    def _load_api_key(self):
        """Load API key from .env file."""
        env_path = Path(__file__).parent / '.env'
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        return line.split('=', 1)[1].strip()
        
        # Also check environment variable
        return os.getenv('GEMINI_API_KEY')

    def think(self, user_input):
        """
        Process user input and generate structured command.
        
        Args:
            user_input (str): User's command
            
        Returns:
            dict: Structured command with 'action' and 'params' keys
        """
        try:
            # Create full prompt
            full_prompt = self.system_prompt + f'\nUser: "{user_input}"'
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            response_text = response.text.strip()
            
            # Extract JSON (handle markdown code blocks)
            if '```json' in response_text:
                json_str = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                json_str = response_text.split('```')[1].split('```')[0].strip()
            else:
                json_str = response_text
            
            # Parse JSON
            command = json.loads(json_str)
            
            return command
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response: {response_text}")
            return {
                "action": "respond",
                "params": {"message": "I'm having trouble understanding that command. Could you rephrase?"}
            }
        except Exception as e:
            print(f"Error in thinking: {e}")
            return {
                "action": "respond",
                "params": {"message": f"An error occurred: {str(e)}"}
            }


# Quick test
if __name__ == "__main__":
    print("Testing Brain...")
    
    try:
        brain = Brain()
        
        test_commands = [
            "Open notepad",
            "Search for weather today",
            "Create a file called hello.txt",
            "Hello there!",
        ]
        
        for cmd in test_commands:
            print(f"\nUser: {cmd}")
            result = brain.think(cmd)
            print(f"Brain output: {json.dumps(result, indent=2)}")
            
    except ValueError as e:
        print(f"\nError: {e}")
