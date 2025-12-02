"""
Tests for script loading functionality
"""

import pytest
import json
from pathlib import Path
from eliza.script import ScriptLoader


class TestScriptLoader:
    """Test script loading functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.script_path = "scripts/doctor.json"
    
    def test_load_script(self):
        """Test that script can be loaded."""
        loader = ScriptLoader(self.script_path)
        script_data = loader.load()
        
        assert script_data is not None
        assert isinstance(script_data, dict)
        assert "keywords" in script_data
    
    def test_get_keywords(self):
        """Test that keywords can be extracted."""
        loader = ScriptLoader(self.script_path)
        loader.load()
        keywords = loader.get_keywords()
        
        assert isinstance(keywords, dict)
        assert len(keywords) > 0
        # Should have common keywords
        assert "hello" in keywords or "feel" in keywords
    
    def test_get_pre_transforms(self):
        """Test that pre-transforms can be extracted."""
        loader = ScriptLoader(self.script_path)
        loader.load()
        pre_transforms = loader.get_pre_transforms()
        
        assert isinstance(pre_transforms, list)
        assert len(pre_transforms) > 0
        # Should have contraction expansions
        assert any("i'm" in str(t).lower() or "don't" in str(t).lower() 
                  for t in pre_transforms)
    
    def test_get_post_transforms(self):
        """Test that post-transforms can be extracted."""
        loader = ScriptLoader(self.script_path)
        loader.load()
        post_transforms = loader.get_post_transforms()
        
        assert isinstance(post_transforms, list)
        assert len(post_transforms) > 0
    
    def test_get_synonyms(self):
        """Test that synonyms can be extracted."""
        loader = ScriptLoader(self.script_path)
        loader.load()
        synonyms = loader.get_synonyms()
        
        assert isinstance(synonyms, dict)
        assert len(synonyms) > 0
    
    def test_get_quit_words(self):
        """Test that quit words can be extracted."""
        loader = ScriptLoader(self.script_path)
        loader.load()
        quit_words = loader.get_quit_words()
        
        assert isinstance(quit_words, list)
        assert len(quit_words) > 0
        assert "bye" in quit_words or "quit" in quit_words
    
    def test_get_default_responses(self):
        """Test that default responses can be extracted."""
        loader = ScriptLoader(self.script_path)
        loader.load()
        defaults = loader.get_default_responses()
        
        assert isinstance(defaults, list)
        assert len(defaults) > 0
    
    def test_script_file_exists(self):
        """Test that script file exists."""
        script_file = Path(__file__).parent.parent / self.script_path
        assert script_file.exists(), f"Script file not found: {script_file}"
    
    def test_script_is_valid_json(self):
        """Test that script file is valid JSON."""
        script_file = Path(__file__).parent.parent / self.script_path
        with open(script_file, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
        assert "keywords" in data


class TestScriptIntegration:
    """Test script integration with ELIZA."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from eliza.core import Eliza
        self.eliza = Eliza()
    
    def test_script_loaded(self):
        """Test that script is loaded on initialization."""
        # ELIZA should load script by default
        assert len(self.eliza.keywords) > 0
    
    def test_script_keywords_work(self):
        """Test that keywords from script work."""
        # Test a keyword that should be in the script
        response = self.eliza.respond("hello")
        assert response is not None
    
    def test_script_memory_rules(self):
        """Test that memory rules from script are loaded."""
        assert hasattr(self.eliza, 'memory_rules')
        assert "decomposition" in self.eliza.memory_rules

