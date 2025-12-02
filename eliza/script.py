"""
Script loading and management for ELIZA

This module handles loading conversation scripts (like DOCTOR) from JSON files.
Scripts define keywords, decomposition rules, reassembly rules, and transformations.
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class ScriptLoader:
    """
    Loads and manages ELIZA conversation scripts from JSON files.
    
    Scripts define:
    - keywords: List of keywords with ranks and decomposition/reassembly rules
    - pre_transforms: Pre-processing transformations (contractions, etc.)
    - post_transforms: Post-processing transformations (pronoun switching)
    - synonyms: Synonym mappings
    - quit_words: Words that signal the user wants to quit
    """
    
    def __init__(self, script_path: Optional[str] = None):
        """
        Initialize script loader.
        
        Args:
            script_path: Path to script JSON file. If None, uses default DOCTOR script.
        """
        self.script_path = script_path
        self.script_data: Optional[Dict] = None
    
    def load(self, script_path: Optional[str] = None) -> Dict:
        """
        Load a script from a JSON file.
        
        Args:
            script_path: Path to script file. If None, uses self.script_path or default.
            
        Returns:
            Dictionary containing script data
            
        Raises:
            FileNotFoundError: If script file doesn't exist
            json.JSONDecodeError: If script file is invalid JSON
        """
        if script_path is None:
            script_path = self.script_path
        
        if script_path is None:
            # Use default DOCTOR script
            script_path = self._get_default_script_path()
        
        # Resolve path relative to this file's directory
        script_file = Path(__file__).parent.parent / script_path
        
        if not script_file.exists():
            raise FileNotFoundError(f"Script file not found: {script_file}")
        
        with open(script_file, 'r', encoding='utf-8') as f:
            self.script_data = json.load(f)
        
        return self.script_data
    
    def _get_default_script_path(self) -> str:
        """Get path to default DOCTOR script."""
        return "scripts/doctor.json"
    
    def get_keywords(self) -> Dict:
        """
        Extract keywords dictionary from loaded script.
        
        Returns:
            Dictionary mapping keyword -> keyword_data (rank, decomposition rules)
        """
        if self.script_data is None:
            raise ValueError("Script not loaded. Call load() first.")
        
        keywords = {}
        
        # Script format: keywords is a list of keyword objects
        for keyword_obj in self.script_data.get("keywords", []):
            word = keyword_obj["word"]
            rank = keyword_obj.get("rank", 0)
            decomposition = keyword_obj.get("decomposition", [])
            
            keywords[word] = {
                "rank": rank,
                "decomposition": decomposition
            }
        
        return keywords
    
    def get_pre_transforms(self) -> List[List[str]]:
        """
        Extract pre-transformations from script.
        
        Returns:
            List of [pattern, replacement] pairs for pre-transformations
        """
        if self.script_data is None:
            raise ValueError("Script not loaded. Call load() first.")
        
        return self.script_data.get("pre", [])
    
    def get_post_transforms(self) -> List[List[str]]:
        """
        Extract post-transformations from script.
        
        Returns:
            List of [pattern, replacement] pairs for post-transformations
        """
        if self.script_data is None:
            raise ValueError("Script not loaded. Call load() first.")
        
        return self.script_data.get("post", [])
    
    def get_synonyms(self) -> Dict[str, List[str]]:
        """
        Extract synonyms from script.
        
        Returns:
            Dictionary mapping canonical word -> list of variations
        """
        if self.script_data is None:
            raise ValueError("Script not loaded. Call load() first.")
        
        return self.script_data.get("synon", {})
    
    def get_quit_words(self) -> List[str]:
        """
        Extract quit words from script.
        
        Returns:
            List of words that signal the user wants to quit
        """
        if self.script_data is None:
            raise ValueError("Script not loaded. Call load() first.")
        
        return self.script_data.get("quit", ["bye", "goodbye", "quit", "exit"])
    
    def get_default_responses(self) -> List[str]:
        """
        Extract default responses from script.
        
        Returns:
            List of default responses when no pattern matches
        """
        if self.script_data is None:
            raise ValueError("Script not loaded. Call load() first.")
        
        return self.script_data.get("default", [
            "I see.",
            "Tell me more.",
            "Go on.",
            "I understand.",
            "Can you elaborate on that?",
            "What does that suggest to you?",
            "How does that make you feel?"
        ])

