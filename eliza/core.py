"""
Core ELIZA engine - Pattern matching and response generation

Now with decomposition, reassembly, transformations, and script loading!
- Decomposition/reassembly: Extract parts and use them in responses
- Transformations: Normalize input and adjust responses
- Script system: Load conversation patterns from JSON files
"""

import json
import re
import random
from typing import Dict, List, Optional, Tuple

from eliza.transformations import Transformations
from eliza.script import ScriptLoader
from eliza.memory import Memory


class Eliza:
    """
    ELIZA implementation with decomposition, reassembly, and transformations.
    
    This version adds:
    - Decomposition rules: Extract parts of sentences using patterns
    - Reassembly rules: Use extracted parts to build personalized responses
    - Pre-transformations: Normalize input (contractions, synonyms)
    - Post-transformations: Adjust responses (pronoun switching)
    
    Example:
        Input: "I'm sad"
        Pre-transform: "i am sad" (expands contraction)
        Pattern: "i am (.*)" matches and captures "sad"
        Response: "Why are you sad?" (uses the captured part)
        Post-transform: "Why are you sad?" (already correct)
    """
    
    def __init__(self, script_path: Optional[str] = None):
        """
        Initialize ELIZA.
        
        Args:
            script_path: Path to script JSON file. If None, uses default DOCTOR script.
                        If script loading fails, falls back to hardcoded patterns.
        """
        # Try to load from script file
        self.keywords: Dict[str, Dict] = {}
        self.default_responses: List[str] = []
        self.initial_prompts: List[str] = []
        
        try:
            script_loader = ScriptLoader(script_path)
            script_data = script_loader.load()
            self.keywords = script_loader.get_keywords()
            self.default_responses = script_loader.get_default_responses()
            self.initial_prompts = script_loader.get_initial_prompts()
            
            # Update transformations with script data
            pre_transforms = script_loader.get_pre_transforms()
            post_transforms = script_loader.get_post_transforms()
            synonyms = script_loader.get_synonyms()
            keywords_to_preserve = list(self.keywords.keys())
            
            self.transformations = Transformations(
                preserve_keywords=keywords_to_preserve,
                pre_transforms=pre_transforms,
                post_transforms=post_transforms,
                synonyms=synonyms
            )
            
            # Load MEMORY rules from script if available
            memory_rules = script_data.get("memory", None)
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            # Fall back to hardcoded patterns if script loading fails
            print(f"Warning: Could not load script ({e}). Using default patterns.")
            self._init_default_patterns()
            keywords_to_preserve = list(self.keywords.keys())
            self.transformations = Transformations(preserve_keywords=keywords_to_preserve)
            memory_rules = None
            self.initial_prompts = [
                "How do you do. Please tell me your problem.",
                "Is something troubling you?",
                "What seems to be the problem?"
            ]
        
        # Ensure initial_prompts is set (in case script loading succeeded but didn't have initial)
        if not hasattr(self, 'initial_prompts') or not self.initial_prompts:
            self.initial_prompts = [
                "How do you do. Please tell me your problem.",
                "Is something troubling you?",
                "What seems to be the problem?"
            ]
        
        # Initialize memory system
        self.memory = Memory()
        self.memory_rules = memory_rules or {
            "decomposition": [
                {
                    "pattern": ".*",
                    "reassembly": [
                        "Let's discuss further why {0}.",
                        "Earlier you said {0}.",
                        "Can you tell me more about {0}?"
                    ]
                }
            ]
        }
    
    def _init_default_patterns(self):
        """Initialize with hardcoded default patterns (fallback)."""
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
            # Note: More specific patterns must come first!
            "am": {
                "rank": 5,
                "decomposition": [
                    {
                        # Handle negation FIRST (more specific pattern)
                        # After normalization: "i am not X"
                        "pattern": r".*i am not (.*)",
                        "reassembly": [
                            "Why are you not {0}?",
                            "What makes you not {0}?",
                            "Can you tell me more about not being {0}?"
                        ]
                    },
                    {
                        # General "I am X" pattern
                        "pattern": r".*i am (.*)",
                        "reassembly": [
                            "Why are you {0}?",
                            "How long have you been {0}?",
                            "Do you enjoy being {0}?"
                        ]
                    },
                    {
                        # "I'm X" pattern (before normalization)
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
            # Note: More specific patterns must come first!
            "feel": {
                "rank": 5,
                "decomposition": [
                    {
                        # Handle negation FIRST (more specific pattern)
                        # After normalization: "i do not feel X"
                        "pattern": r".*i do not feel (.*)",
                        "reassembly": [
                            "What makes you not feel {0}?",
                            "Why don't you feel {0}?",
                            "Can you tell me more about not feeling {0}?"
                        ]
                    },
                    {
                        # General "I feel X" pattern
                        "pattern": r".*i feel (.*)",
                        "reassembly": [
                            "Do you often feel {0}?",
                            "What makes you feel {0}?",
                            "Can you tell me more about feeling {0}?"
                        ]
                    },
                    {
                        # "I'm feeling X" pattern (before normalization)
                        "pattern": r".*i'm feeling (.*)",
                        "reassembly": [
                            "Why do you think you're feeling {0}?",
                            "How long have you been feeling {0}?",
                            "What's causing you to feel {0}?"
                        ]
                    },
                    {
                        # More flexible: allow words between "i" and "feel" (fallback)
                        # This catches cases like "i really feel X" or "i sometimes feel X"
                        "pattern": r".*i .+ feel (.*)",
                        "reassembly": [
                            "What makes you feel {0}?",
                            "Can you tell me more about feeling {0}?",
                            "How does feeling {0} affect you?"
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
        
        # Initialize transformations with keyword preservation
        # Preserve keywords so synonym normalization doesn't change them
        keywords_to_preserve = list(self.keywords.keys())
        self.transformations = Transformations(preserve_keywords=keywords_to_preserve)
    
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
            
            # Convert pattern string to regex if needed (scripts use strings, not raw strings)
            # Patterns from JSON are already strings, so we can use them directly
            # But we need to ensure they work as regex patterns
            if not pattern.startswith('r"') and not pattern.startswith("r'"):
                # It's a regular string pattern, use it directly
                pass
            
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
        1. Apply pre-transformations to normalize input (contractions, synonyms)
        2. Find the highest priority keyword that appears in the input
        3. Try each decomposition pattern for that keyword
        4. If a pattern matches, extract parts and build a response
        5. Apply post-transformations to adjust response (pronoun switching)
        6. If no pattern matches, use a default response
        
        Args:
            user_input: The user's input string
            
        Returns:
            A response string
        """
        # Apply pre-transformations to normalize input
        # This expands contractions, normalizes synonyms, etc.
        normalized_input = self.transformations.pre_transform(user_input)
        
        # Check if "my" appears in input - if so, store in memory
        # According to the original ELIZA paper, when "my" is present, store the sentence
        # We check this before keyword matching to ensure we capture it
        if "my" in normalized_input:
            # Store the post-transformed normalized input in memory
            # The original paper stores transformed sentences
            # We transform the normalized input (not the original) so pronouns are properly switched
            transformed_user_input = self.transformations.post_transform(normalized_input)
            self.memory.store(transformed_user_input.lower())
        
        # Find matching keyword (highest priority)
        keyword_match = self._match_keyword(normalized_input)
        
        if keyword_match:
            keyword, keyword_data = keyword_match
            
            # Try to decompose and reassemble
            response = self._try_decomposition(normalized_input, keyword_data)
            
            if response:
                # Apply post-transformations to adjust response
                # This switches pronouns, adjusts verb forms, etc.
                response = self.transformations.post_transform(response)
                return response
        
        # No keyword matched - try MEMORY
        # Use memory if available, but prefer default responses for:
        # - Responses starting with "yes"/"no" etc. (these are acknowledgments)
        # - Very short inputs that are common words
        if self.memory.has_memory():
            # Check if input starts with common response/acknowledgment words
            # Strip punctuation to handle "yes," "no." etc.
            common_starters = {"yes", "no", "ok", "okay", "sure", "right", "yeah", "yep", "nope", "yea"}
            if normalized_input.split():
                first_word_raw = normalized_input.split()[0].lower()
                # Remove punctuation
                first_word = re.sub(r'[^\w]', '', first_word_raw)
            else:
                first_word = ""
            
            # If input starts with acknowledgment words, use default (not memory)
            # Memory should be used for truly nonsensical/random inputs
            if first_word in common_starters:
                # Use default response for "yes"/"no" type responses
                pass
            else:
                # Use memory for nonsensical inputs (like "potato")
                # Memory is removed after use (consumed) - matches original ELIZA
                recalled = self.memory.recall(remove=True)  # Remove after use
                if recalled:
                    # Use MEMORY decomposition rules
                    for decomp_rule in self.memory_rules["decomposition"]:
                        pattern = decomp_rule["pattern"]
                        reassembly_templates = decomp_rule["reassembly"]
                        
                        # Try to match the pattern against the recalled memory
                        match = re.search(pattern, recalled, re.IGNORECASE)
                        if match:
                            # Use the recalled memory as {0}
                            template = random.choice(reassembly_templates)
                            
                            # Transform memory for templates that need noun phrases
                            # Templates like "Can you tell me more about {0}?" need gerund form
                            memory_for_template = self._transform_memory_for_template(recalled, template)
                            
                            response = template.format(memory_for_template)
                            response = self.transformations.post_transform(response)
                            return response
        
        # No decomposition matched - use default response
        return random.choice(self.default_responses)
    
    def _transform_memory_for_template(self, memory: str, template: str) -> str:
        """
        Transform recalled memory to work grammatically with different templates.
        
        Some templates need noun phrases (gerunds), others work with full sentences.
        For example:
        - "Earlier you said {0}." works with "your mother hates me"
        - "Can you tell me more about {0}?" needs "your mother hating you" (gerund)
        
        Args:
            memory: The recalled memory sentence
            template: The template it will be inserted into
            
        Returns:
            Transformed memory that works grammatically with the template
        """
        # Check if template needs a noun phrase (gerund form)
        # Templates with "about" or "why" often need different forms
        if "about" in template.lower():
            # Convert "your mother hates me" -> "your mother hating you"
            # Simple heuristic: find verb and convert to gerund
            # "hates" -> "hating", "is" -> "being", etc.
            transformed = memory
            
            # Convert common verb forms to gerunds
            verb_to_gerund = {
                r"\bhates\b": "hating",
                r"\bhate\b": "hating",
                r"\bis\b": "being",
                r"\bare\b": "being",
                r"\bwas\b": "being",
                r"\bwere\b": "being",
                r"\bfeels\b": "feeling",
                r"\bfeel\b": "feeling",
                r"\bthinks\b": "thinking",
                r"\bthink\b": "thinking",
                r"\bwants\b": "wanting",
                r"\bwant\b": "wanting",
                r"\bneeds\b": "needing",
                r"\bneed\b": "needing",
            }
            
            for verb_pattern, gerund in verb_to_gerund.items():
                transformed = re.sub(verb_pattern, gerund, transformed, flags=re.IGNORECASE)
            
            # Also change "me" to "you" for gerund forms
            transformed = re.sub(r"\bme\b", "you", transformed, flags=re.IGNORECASE)
            
            return transformed
        elif "why" in template.lower():
            # "Let's discuss further why {0}." - can use full sentence or add "you"
            # Keep as-is, it works
            return memory
        else:
            # Default: use memory as-is (works for "Earlier you said {0}.")
            return memory
    
    def get_initial(self) -> str:
        """
        Get an initial prompt to start the conversation.
        
        Returns:
            A random initial prompt from the script
        """
        if self.initial_prompts:
            return random.choice(self.initial_prompts)
        return "How do you do. Please tell me your problem."

