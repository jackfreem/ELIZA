"""
Tests for core ELIZA functionality
"""

import pytest
from eliza.core import Eliza


class TestCore:
    """Test core ELIZA pattern matching and response generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
    
    def test_basic_keyword_matching(self):
        """Test that keywords are matched correctly."""
        response = self.eliza.respond("hello")
        assert response is not None
        assert len(response) > 0
        # Should get a greeting response
        assert "hello" in response.lower() or "hi" in response.lower()
    
    def test_decomposition_reassembly(self):
        """Test decomposition and reassembly rules."""
        response = self.eliza.respond("I am sad")
        assert response is not None
        # Should extract "sad" and use it in response
        assert "sad" in response.lower()
        assert "you" in response.lower()  # Should switch pronouns
    
    def test_contraction_handling(self):
        """Test that contractions are expanded correctly."""
        # "I'm" should be treated the same as "I am"
        response1 = self.eliza.respond("I'm sad")
        response2 = self.eliza.respond("I am sad")
        
        # Both should extract "sad"
        assert "sad" in response1.lower()
        assert "sad" in response2.lower()
    
    def test_negation_patterns(self):
        """Test negation patterns like 'I don't feel'."""
        response = self.eliza.respond("I don't feel happy")
        assert response is not None
        # Should handle negation
        assert "not" in response.lower() or "don't" in response.lower()
    
    def test_keyword_priority(self):
        """Test that higher rank keywords are matched first."""
        # "mother" has rank 10, "am" has rank 5
        # "My mother" should match "mother" not "am"
        response = self.eliza.respond("My mother is nice")
        assert "family" in response.lower() or "mother" in response.lower()
    
    def test_default_response(self):
        """Test default responses when no keyword matches."""
        response = self.eliza.respond("xyzabc123")
        assert response is not None
        assert len(response) > 0
        # Should be one of the default responses
        default_responses = [
            "i see", "tell me more", "go on", "i understand",
            "can you elaborate", "what does that suggest",
            "how does that make you feel"
        ]
        assert any(phrase in response.lower() for phrase in default_responses)
    
    def test_multiple_patterns_per_keyword(self):
        """Test that multiple patterns per keyword work."""
        # "feel" keyword has multiple patterns
        response1 = self.eliza.respond("I feel happy")
        response2 = self.eliza.respond("I'm feeling sad")
        
        assert response1 is not None
        assert response2 is not None
        assert "feel" in response1.lower() or "happy" in response1.lower()
        assert "feel" in response2.lower() or "sad" in response2.lower()


class TestMemory:
    """Test memory system functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
    
    def test_memory_storage(self):
        """Test that sentences with 'my' are stored in memory."""
        # Clear memory first
        self.eliza.memory.clear()
        
        # Say something with "my"
        self.eliza.respond("My dog is cute")
        
        # Memory should have stored something
        assert len(self.eliza.memory) > 0
        recalled = self.eliza.memory.recall()
        assert recalled is not None
        assert "dog" in recalled.lower() or "cute" in recalled.lower()
    
    def test_memory_recall_when_no_keyword(self):
        """Test that memory is used when no keyword matches."""
        # Clear memory first
        self.eliza.memory.clear()
        
        # Store something in memory
        self.eliza.respond("My cat is fluffy")
        
        # Now say something with no keywords
        response = self.eliza.respond("xyzabc")
        
        # Should reference memory
        assert "cat" in response.lower() or "fluffy" in response.lower()
        assert "earlier" in response.lower() or "discuss" in response.lower()
    
    def test_memory_fifo(self):
        """Test that memory uses FIFO (oldest first)."""
        self.eliza.memory.clear()
        
        # Store multiple memories
        self.eliza.respond("My first thing")
        self.eliza.respond("My second thing")
        
        # Should recall oldest first
        recalled = self.eliza.memory.recall()
        assert "first" in recalled.lower()
    
    def test_memory_max_size(self):
        """Test that memory respects max size limit."""
        self.eliza.memory.clear()
        
        # Store more than max_size items
        for i in range(10):
            self.eliza.respond(f"My thing {i}")
        
        # Should only have max_size items
        assert len(self.eliza.memory) <= self.eliza.memory.max_size


class TestTransformations:
    """Test transformation functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
    
    def test_pronoun_switching(self):
        """Test that pronouns are switched correctly."""
        response = self.eliza.respond("I am happy")
        # "I" should become "you", "my" should become "your"
        assert "you" in response.lower()
        # Should not have "I" in response (except in ELIZA's own words)
    
    def test_verb_form_adjustment(self):
        """Test that verb forms are adjusted."""
        # Test directly with transformations to avoid randomness
        test_text = "why am i sad"
        transformed = self.eliza.transformations.post_transform(test_text)
        # "am" should become "are" in transformation
        assert "are" in transformed.lower()
        assert "am" not in transformed.lower()
    
    def test_is_not_changed_to_are(self):
        """Test that 'is' is NOT incorrectly changed to 'are'."""
        # Store something with "is"
        self.eliza.memory.clear()
        self.eliza.respond("My dog is cute")
        
        # Recall it
        recalled = self.eliza.memory.recall()
        # Should still have "is", not "are"
        assert "is" in recalled.lower()
        assert "are" not in recalled or recalled.index("are") > recalled.index("is")


class TestIntegration:
    """Integration tests for full conversation flow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
        self.eliza.memory.clear()
    
    def test_full_conversation(self):
        """Test a full conversation flow."""
        # Greeting
        r1 = self.eliza.respond("Hello")
        assert r1 is not None
        
        # User shares feeling
        r2 = self.eliza.respond("I feel sad")
        assert "sad" in r2.lower() or "feel" in r2.lower()
        
        # User mentions family (stores in memory)
        r3 = self.eliza.respond("My mother is nice")
        assert "family" in r3.lower() or "mother" in r3.lower()
        
        # Random input (should use memory)
        r4 = self.eliza.respond("potato")
        assert "mother" in r4.lower() or "nice" in r4.lower()
    
    def test_memory_persistence(self):
        """Test that memory persists across multiple interactions."""
        self.eliza.memory.clear()
        
        # Store memory
        self.eliza.respond("My favorite color is blue")
        
        # Multiple interactions
        self.eliza.respond("Hello")
        self.eliza.respond("I am happy")
        
        # Memory should still be available
        assert len(self.eliza.memory) > 0
        recalled = self.eliza.memory.recall()
        assert "blue" in recalled.lower() or "color" in recalled.lower()

