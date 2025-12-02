"""
Simple CLI interface for ELIZA

This lets you interact with ELIZA and see how it responds.
"""

from eliza.core import Eliza


def main():
    """
    Main conversation loop - simple interactive CLI
    """
    print("=" * 60)
    print("ELIZA - A simple pattern matching chatbot")
    print("=" * 60)
    print("\nType 'quit' or 'exit' to end the conversation.\n")
    
    eliza = Eliza()
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for quit commands
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
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

