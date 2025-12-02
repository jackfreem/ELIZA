"""
Core ELIZA engine - Pattern matching and response generation

Now with decomposition and reassembly rules!
This allows ELIZA to extract parts of sentences and use them in responses.
"""

import re
import random
from typing import Dict, List, Optional, Tuple


class Eliza:
    """
    ELIZA implementation with decomposition and reassembly rules.
    
    This version adds:
    - Decomposition rules: Extract parts of sentences using patterns
    - Reassembly rules: Use extracted parts to build personalized responses
    
    Example:
        Input: "I am sad"
        Pattern: "i am (.*)" matches and captures "sad"
        Response: "Why are you sad?" (uses the captured part)
    """
    
    def __init__(self):
        # Keywords with decomposition/reassembly rules
        # Each keyword has a rank (priority) and decomposition rules
        # Each decomposition rule has a pattern and reassembly templates
        self.keywords: Dict[str, Dict] = {
            "hello": {
                "rank": 0,  # Lower priority
                "decomposition": [
                    {
                        "pattern": r".*hello.*",
                        "reassembly": [
                            "Hello. How are you feeling today?",
                            "Hi there. What brings you here?",
                            "Hello. I'm here to listen."
                        ]
                    }
                ]
            },
            "mother": {
                "rank": 10,
                "decomposition": [
                    {
                        "pattern": r".*mother.*",
                        "reassembly": [
                            "Tell me more about your family.",
                            "Who else in your family?",
                            "What about your family?"
                        ]
                    }
                ]
            },
            "father": {
                "rank": 10,
                "decomposition": [
                    {
                        "pattern": r".*father.*",
                        "reassembly": [
                            "Tell me more about your family.",
                            "Who else in your family?",
                            "What about your family?"
                        ]
                    }
                ]
            },
            # "I am X" pattern - extracts X and uses it in response
            "am": {
                "rank": 5,
                "decomposition": [
                    {
                        "pattern": r".*i am (.*)",
                        "reassembly": [
                            "Why are you {0}?",
                            "How long have you been {0}?",
                            "Do you enjoy being {0}?"
                        ]
                    },
                    {
                        "pattern": r".*i'm (.*)",
                        "reassembly": [
                            "Why are you {0}?",
                            "How does being {0} make you feel?",
                            "Tell me more about being {0}."
                        ]
                    }
                ]
            },
            # "I feel X" pattern - extracts the feeling
            "feel": {
                "rank": 5,
                "decomposition": [
                    {
                        "pattern": r".*i feel (.*)",
                        "reassembly": [
                            "Do you often feel {0}?",
                            "What makes you feel {0}?",
                            "Can you tell me more about feeling {0}?"
                        ]
                    },
                    {
                        "pattern": r".*i'm feeling (.*)",
                        "reassembly": [
                            "Why do you think you're feeling {0}?",
                            "How long have you been feeling {0}?",
                            "What's causing you to feel {0}?"
                        ]
                    }
                ]
            },
            # "I think X" pattern
            "think": {
                "rank": 5,
                "decomposition": [
                    {
                        "pattern": r".*i think (.*)",
                        "reassembly": [
                            "What makes you think {0}?",
                            "Do you really think {0}?",
                            "Can you elaborate on why you think {0}?"
                        ]
                    }
                ]
            },
            # "I want X" pattern
            "want": {
                "rank": 5,
                "decomposition": [
                    {
                        "pattern": r".*i want (.*)",
                        "reassembly": [
                            "Why do you want {0}?",
                            "What would it mean to you if you had {0}?",
                            "Tell me more about wanting {0}."
                        ]
                    }
                ]
            },
            # "I need X" pattern
            "need": {
                "rank": 5,
                "decomposition": [
                    {
                        "pattern": r".*i need (.*)",
                        "reassembly": [
                            "Why do you need {0}?",
                            "What would happen if you didn't have {0}?",
                            "Tell me more about needing {0}."
                        ]
                    }
                ]
            }
        }
        
        # Default responses when no keyword matches
        self.default_responses = [
            "I see.",
            "Tell me more.",
            "Go on.",
            "I understand.",
            "Can you elaborate on that?",
            "What does that suggest to you?",
            "How does that make you feel?"
        ]
    
    def _match_keyword(self, text: str) -> Optional[Tuple[str, Dict]]:
        """
        Find the highest priority keyword that appears in the text.
        
        Returns:
            Tuple of (keyword, keyword_data) or None if no match
        """
        # Sort keywords by rank (higher rank = higher priority)
        sorted_keywords = sorted(
            self.keywords.items(),
            key=lambda x: x[1]["rank"],
            reverse=True
        )
        
        for keyword, keyword_data in sorted_keywords:
            if keyword in text:
                return (keyword, keyword_data)
        
        return None
    
    def _try_decomposition(self, text: str, keyword_data: Dict) -> Optional[str]:
        """
        Try to match decomposition patterns and generate a response.
        
        This is the core of ELIZA:
        1. Try each decomposition pattern for the keyword
        2. If a pattern matches, extract the captured groups
        3. Use those groups in a reassembly template
        
        Args:
            text: The user's input (lowercase)
            keyword_data: The keyword's data dictionary
            
        Returns:
            A response string if a pattern matched, None otherwise
        """
        for decomp_rule in keyword_data["decomposition"]:
            pattern = decomp_rule["pattern"]
            reassembly_templates = decomp_rule["reassembly"]
            
            # Try to match the pattern
            match = re.search(pattern, text, re.IGNORECASE)
            
            if match:
                # Pattern matched! Extract captured groups
                # match.groups() returns all captured parts (the (.*) parts)
                captured_parts = match.groups()
                
                # Choose a random reassembly template
                template = random.choice(reassembly_templates)
                
                # Fill in the template with captured parts
                # {0} gets the first captured group, {1} gets the second, etc.
                try:
                    response = template.format(*captured_parts)
                    return response
                except (IndexError, KeyError):
                    # Template doesn't match captured groups - skip this rule
                    continue
        
        return None
    
    def respond(self, user_input: str) -> str:
        """
        Generate a response to user input using decomposition and reassembly.
        
        Process:
        1. Find the highest priority keyword that appears in the input
        2. Try each decomposition pattern for that keyword
        3. If a pattern matches, extract parts and build a response
        4. If no pattern matches, use a default response
        
        Args:
            user_input: The user's input string
            
        Returns:
            A response string
        """
        # Convert to lowercase for matching
        input_lower = user_input.lower().strip()
        
        # Find matching keyword (highest priority)
        keyword_match = self._match_keyword(input_lower)
        
        if keyword_match:
            keyword, keyword_data = keyword_match
            
            # Try to decompose and reassemble
            response = self._try_decomposition(input_lower, keyword_data)
            
            if response:
                return response
        
        # No decomposition matched - use default response
        return random.choice(self.default_responses)

