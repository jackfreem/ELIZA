"""
Simple CLI interface for ELIZA

This lets you interact with ELIZA and see how it responds.
"""

from eliza.core import Eliza
from eliza.script import ScriptLoader


def main():
    """
    Main conversation loop - simple interactive CLI
    """
    print("=" * 60)
    print("ELIZA - A simple pattern matching chatbot")
    print("=" * 60)
    print("\nType 'quit' or 'exit' to end the conversation.\n")
    
    # Load ELIZA with default DOCTOR script
    eliza = Eliza()
    
    # Get quit words from script (if available)
    try:
        script_loader = ScriptLoader()
        script_loader.load()
        quit_words = script_loader.get_quit_words()
    except:
        quit_words = ['quit', 'exit', 'bye', 'goodbye']
    
    # Display initial prompt
    initial = eliza.get_initial()
    print(f"ELIZA: {initial}\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for quit commands
        if user_input.lower() in quit_words:
            print("\nELIZA: Goodbye. It was nice talking to you.")
            break
        
        # Skip empty input
        if not user_input:
            continue
        
        # Get and display ELIZA's response
        response = eliza.respond(user_input)
        print(f"ELIZA: {response}\n")


if __name__ == "__main__":
    main()

