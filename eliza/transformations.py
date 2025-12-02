"""
Text transformations for ELIZA

Pre-transformations: Normalize user input before pattern matching
Post-transformations: Adjust responses to make them more natural
"""

import re
from typing import Dict, List, Tuple


class Transformations:
    """
    Handles text transformations for ELIZA.
    
    Pre-transformations normalize input to make pattern matching easier.
    Post-transformations adjust responses to feel more natural.
    """
    
    def __init__(self, preserve_keywords: List[str] = None, 
                 pre_transforms: List[List[str]] = None,
                 post_transforms: List[List[str]] = None,
                 synonyms: Dict[str, List[str]] = None):
        """
        Initialize transformations.
        
        Args:
            preserve_keywords: List of keywords to preserve (don't normalize)
                              These are typically keywords used for pattern matching
            pre_transforms: List of [pattern, replacement] pairs for pre-transforms
                           If None, uses defaults
            post_transforms: List of [pattern, replacement] pairs for post-transforms
                            If None, uses defaults
            synonyms: Dictionary mapping canonical -> variations
                     If None, uses defaults
        """
        self.preserve_keywords = preserve_keywords or []
        
        # Pre-transformations: Applied to user input BEFORE pattern matching
        # These normalize the text to make patterns match more reliably
        if pre_transforms is not None:
            # Convert from script format [pattern, replacement] to tuple format
            self.pre_transforms: List[Tuple[str, str]] = [
                (pattern, replacement) for pattern, replacement in pre_transforms
            ]
        else:
            # Use defaults
            self.pre_transforms: List[Tuple[str, str]] = [
            # Contractions
            (r"i'm", "i am"),
            (r"you're", "you are"),
            (r"he's", "he is"),
            (r"she's", "she is"),
            (r"it's", "it is"),
            (r"we're", "we are"),
            (r"they're", "they are"),
            (r"i've", "i have"),
            (r"you've", "you have"),
            (r"we've", "we have"),
            (r"they've", "they have"),
            (r"i'll", "i will"),
            (r"you'll", "you will"),
            (r"he'll", "he will"),
            (r"she'll", "she will"),
            (r"we'll", "we will"),
            (r"they'll", "they will"),
            (r"i'd", "i would"),
            (r"you'd", "you would"),
            (r"he'd", "he would"),
            (r"she'd", "she would"),
            (r"we'd", "we would"),
            (r"they'd", "they would"),
            (r"don't", "do not"),
            (r"doesn't", "does not"),
            (r"didn't", "did not"),
            (r"won't", "will not"),
            (r"wouldn't", "would not"),
            (r"can't", "cannot"),
            (r"cannot", "can not"),
            (r"couldn't", "could not"),
            (r"shouldn't", "should not"),
            (r"mustn't", "must not"),
            (r"isn't", "is not"),
            (r"aren't", "are not"),
            (r"wasn't", "was not"),
            (r"weren't", "were not"),
            (r"haven't", "have not"),
            (r"hasn't", "has not"),
            (r"hadn't", "had not"),
            (r"let's", "let us"),
            (r"that's", "that is"),
            (r"what's", "what is"),
            (r"who's", "who is"),
            (r"where's", "where is"),
            (r"when's", "when is"),
            (r"why's", "why is"),
            (r"how's", "how is"),
            (r"there's", "there is"),
            (r"here's", "here is"),
        ]
        
        # Post-transformations: Applied to responses AFTER reassembly
        # These make responses feel more natural by switching pronouns
        # Note: We need to be careful - some phrases like "tell me" should stay as "tell me"
        if post_transforms is not None:
            # Convert from script format [pattern, replacement] to tuple format
            # Script uses simple strings, so we add word boundaries to avoid partial matches
            self.post_transforms: List[Tuple[str, str]] = [
                (r"\b" + pattern + r"\b", replacement) for pattern, replacement in post_transforms
            ]
        else:
            # Use defaults
            self.post_transforms: List[Tuple[str, str]] = [
                # First person to second person (user's perspective)
                # But avoid changing "me" in common phrases like "tell me"
                (r"\bam\b", "are"),
                (r"\bis\b", "are"),
                (r"\bwas\b", "were"),
                (r"\bi\b", "you"),
                (r"\bmy\b", "your"),
                (r"\bmyself\b", "yourself"),
                # Only change "me" if it's not part of "tell me" or similar phrases
                # This is a simplified approach - in practice, we'd need more context
                (r"\bme\b(?!\s+(?:more|about|how|what|why|when|where))", "you"),
                (r"\bmine\b", "yours"),
            ]
        
        # Synonyms: Map variations to a canonical form
        # This helps patterns match even when users use different words
        if synonyms is not None:
            self.synonyms: Dict[str, List[str]] = synonyms
        else:
            # Use defaults
            self.synonyms: Dict[str, List[str]] = {
            "be": ["am", "is", "are", "was", "were", "being", "been"],
            "feel": ["feeling", "felt"],
            "think": ["thinking", "thought", "believe", "believing"],
            "want": ["wanting", "wanted", "wish", "wishing", "wished"],
            "need": ["needing", "needed", "require", "requiring", "required"],
            "like": ["liking", "liked", "enjoy", "enjoying", "enjoyed"],
            "hate": ["hating", "hated", "dislike", "disliking", "disliked"],
            "love": ["loving", "loved"],
            "sad": ["sadness", "saddened", "unhappy", "depressed", "depression"],
            "happy": ["happiness", "glad", "gladness", "joy", "joyful", "cheerful"],
            "angry": ["anger", "mad", "furious", "annoyed", "annoyance"],
            "afraid": ["fear", "fearful", "scared", "scary", "frightened"],
            "mother": ["mom", "mommy", "mama", "mum", "mummy"],
            "father": ["dad", "daddy", "papa", "pop"],
            "family": ["families", "relatives", "relatives"],
        }
        
        # Build reverse synonym lookup: word -> canonical form
        self._synonym_map: Dict[str, str] = {}
        for canonical, variations in self.synonyms.items():
            self._synonym_map[canonical] = canonical
            for variation in variations:
                self._synonym_map[variation] = canonical
    
    def pre_transform(self, text: str) -> str:
        """
        Apply pre-transformations to normalize user input.
        
        This makes pattern matching more reliable by:
        - Expanding contractions ("I'm" -> "I am")
        - Normalizing synonyms (variations -> canonical form)
        - Cleaning up the text
        
        Args:
            text: Raw user input
            
        Returns:
            Normalized text ready for pattern matching
        """
        # Convert to lowercase
        normalized = text.lower().strip()
        
        # Apply contraction expansions
        for pattern, replacement in self.pre_transforms:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        # Apply synonym normalization (but preserve keywords)
        words = normalized.split()
        normalized_words = []
        for word in words:
            # Remove punctuation for matching
            clean_word = re.sub(r'[^\w]', '', word)
            # Don't normalize if it's a keyword we want to preserve
            if clean_word in self.preserve_keywords:
                normalized_words.append(word)
            elif clean_word in self._synonym_map:
                canonical = self._synonym_map[clean_word]
                # Preserve original punctuation
                normalized_words.append(word.replace(clean_word, canonical))
            else:
                normalized_words.append(word)
        
        normalized = ' '.join(normalized_words)
        
        # Clean up multiple spaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def post_transform(self, text: str) -> str:
        """
        Apply post-transformations to adjust responses.
        
        This makes responses feel more natural by:
        - Switching pronouns ("I" -> "you", "my" -> "your")
        - Adjusting verb forms ("am" -> "are")
        
        Args:
            text: Response text from reassembly
            
        Returns:
            Adjusted response text
        """
        transformed = text
        
        # Apply post-transformations
        for pattern, replacement in self.post_transforms:
            transformed = re.sub(pattern, replacement, transformed, flags=re.IGNORECASE)
        
        # Capitalize first letter
        if transformed:
            transformed = transformed[0].upper() + transformed[1:]
        
        return transformed

