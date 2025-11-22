"""
OS Agent - Voice and Text-Controlled System Assistant

This is the main entry point for the OS Agent that can:
- Listen to voice commands
- Accept text commands
- Execute OS-level operations
- Respond with voice or text

Usage:
    python main.py --mode voice    # Voice mode (default)
    python main.py --mode text     # Text mode
"""

import sys
import argparse
from pathlib import Path

# Import our modules
from speech_engine import Listener, Speaker
from brain import Brain
from executor import ActionExecutor


class OSAgent:
    """Main OS Agent class that ties everything together."""
    
    def __init__(self, mode='voice'):
        """
        Initialize the OS Agent.
        
        Args:
            mode (str): 'voice' or 'text'
        """
        self.mode = mode
        self.running = False
        
        # Initialize components
        print("Initializing OS Agent...")
        
        try:
            # Always need the brain and executor
            self.brain = Brain()
            self.executor = ActionExecutor()
            
            # Speech components only for voice mode
            if mode == 'voice':
                self.speaker = Speaker()
                self.listener = Listener()
                self.speaker.speak("OS Agent initialized. I'm ready to help!")
            else:
                print("OS Agent initialized in TEXT mode. Type 'exit' to quit.")
                
        except Exception as e:
            print(f"Failed to initialize: {e}")
            sys.exit(1)

    def output(self, message):
        """Output a message (voice or text depending on mode)."""
        if self.mode == 'voice':
            self.speaker.speak(message)
        else:
            print(f"Agent: {message}")

    def get_input(self):
        """Get input from user (voice or text)."""
        if self.mode == 'voice':
            result = self.listener.listen()
            
            # Handle errors
            if result == "ERROR:TIMEOUT":
                return None  # Silent timeout
            elif result == "ERROR:UNCLEAR":
                self.output("Sorry, I didn't catch that. Could you repeat?")
                return None
            elif result.startswith("ERROR"):
                self.output("I'm having trouble hearing you.")
                return None
            
            return result
        else:
            try:
                user_input = input("You: ").strip()
                return user_input if user_input else None
            except EOFError:
                return "exit"

    def process_command(self, command_dict):
        """
        Process a structured command from the brain.
        
        Args:
            command_dict (dict): Command with 'action' and 'params'
            
        Returns:
            str: Result message
        """
        action = command_dict.get('action', '')
        params = command_dict.get('params', {})
        
        # Handle special actions
        if action == 'respond':
            return params.get('message', 'I understand.')
        
        elif action == 'clarify':
            return params.get('message', 'Could you clarify that?')
        
        # Execute OS actions
        else:
            result = self.executor.execute(action, params)
            return result

    def run(self):
        """Main event loop."""
        self.running = True
        
        print("\n" + "="*60)
        print("OS AGENT ACTIVE")
        print("="*60)
        if self.mode == 'voice':
            print("Speak your commands. Say 'exit' or 'quit' to stop.")
        else:
            print("Type your commands. Type 'exit' or 'quit' to stop.")
        print("="*60 + "\n")
        
        while self.running:
            try:
                # Get user input
                user_input = self.get_input()
                
                if user_input is None:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'stop', 'goodbye']:
                    self.output("Goodbye! Shutting down OS Agent.")
                    self.running = False
                    break
                
                # Process with brain
                command = self.brain.think(user_input)
                
                # Execute command
                result = self.process_command(command)
                
                # Output result
                self.output(result)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                self.running = False
                break
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                print(f"ERROR: {error_msg}")
                self.output("Sorry, something went wrong.")

        print("\nOS Agent terminated.")


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(description='OS Agent - Voice/Text System Controller')
    parser.add_argument('--mode', type=str, default='voice', 
                       choices=['voice', 'text'],
                       help='Input mode: voice or text (default: voice)')
    
    args = parser.parse_args()
    
    # Create and run agent
    agent = OSAgent(mode=args.mode)
    agent.run()


if __name__ == "__main__":
    main()
