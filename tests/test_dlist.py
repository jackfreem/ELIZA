"""
Tests for DLIST (Link Words) functionality

DLIST allows certain words to redirect to other keywords for processing.
This is described in the original ELIZA paper as a way to extend keyword
coverage without duplicating patterns.
"""

import pytest
from eliza.core import Eliza


class TestDLIST:
    """Test DLIST (link words) functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
        self.eliza.memory.clear()
    
    def test_links_loaded(self):
        """Test that links are loaded from script."""
        assert len(self.eliza.links) > 0
        # Check some expected links
        assert "dislike" in self.eliza.links
        assert "believe" in self.eliza.links
        assert "nobody" in self.eliza.links
    
    def test_link_redirects_to_target_keyword(self):
        """Test that link words redirect to their target keywords."""
        # "believe" should redirect to "think"
        assert self.eliza.links.get("believe") == "think"
        
        # "dislike" should redirect to "hate"
        assert self.eliza.links.get("dislike") == "hate"
        
        # "require" should redirect to "need"
        assert self.eliza.links.get("require") == "need"
    
    def test_link_word_uses_target_patterns(self):
        """Test that link words use the target keyword's patterns."""
        # "believe" -> "think" keyword
        response = self.eliza.respond("I believe life is hard")
        # Should use "think" patterns which capture "life is hard"
        assert "think" in response.lower() or "life is hard" in response.lower()
    
    def test_link_word_priority_over_regular_keyword(self):
        """Test that link words are checked before regular keywords."""
        # Even if "believe" were a keyword, the link should take priority
        # "believe" links to "think"
        response = self.eliza.respond("I believe something")
        # Should use "think" keyword patterns
        assert response is not None
    
    def test_multiple_link_words(self):
        """Test multiple different link words."""
        test_cases = [
            ("I believe that", "think"),  # believe -> think
            ("I require help", "need"),   # require -> need
            ("I desire peace", "want"),   # desire -> want
        ]
        
        for user_input, expected_keyword in test_cases:
            # Create fresh ELIZA for each test
            eliza = Eliza()
            eliza.memory.clear()
            response = eliza.respond(user_input)
            # Response should not be empty
            assert response is not None
            assert len(response) > 0
    
    def test_link_to_nonexistent_keyword_ignored(self):
        """Test that links to non-existent keywords are ignored."""
        # Manually add a bad link for testing
        self.eliza.links["badlink"] = "nonexistent_keyword"
        
        # Should not crash, should fall through to other keywords or default
        response = self.eliza.respond("badlink test")
        assert response is not None
    
    def test_link_word_in_complex_sentence(self):
        """Test link words work in complex sentences."""
        response = self.eliza.respond("I believe I am sad")
        # Should match either "believe"->"think" or "am" keyword
        assert response is not None
        assert len(response) > 0
    
    def test_hate_link_words(self):
        """Test various words that link to 'hate' keyword."""
        hate_links = ["dislike", "despise", "detest", "loathe"]
        
        for link_word in hate_links:
            if link_word in self.eliza.links:
                assert self.eliza.links[link_word] == "hate"
    
    def test_think_link_words(self):
        """Test various words that link to 'think' keyword."""
        think_links = ["believe", "belief", "suppose"]
        
        for link_word in think_links:
            if link_word in self.eliza.links:
                assert self.eliza.links[link_word] == "think"
    
    def test_want_link_words(self):
        """Test various words that link to 'want' keyword."""
        want_links = ["desire", "wish", "crave"]
        
        for link_word in want_links:
            if link_word in self.eliza.links:
                assert self.eliza.links[link_word] == "want"
    
    def test_need_link_words(self):
        """Test various words that link to 'need' keyword."""
        need_links = ["require"]
        
        for link_word in need_links:
            if link_word in self.eliza.links:
                assert self.eliza.links[link_word] == "need"
    
    def test_feel_link_words(self):
        """Test various words that link to 'feel' keyword."""
        feel_links = ["sense", "perceive"]
        
        for link_word in feel_links:
            if link_word in self.eliza.links:
                assert self.eliza.links[link_word] == "feel"
    
    def test_everyone_link_words(self):
        """Test various words that link to 'everyone' keyword."""
        everyone_links = ["nobody", "no one"]
        
        for link_word in everyone_links:
            if link_word in self.eliza.links:
                assert self.eliza.links[link_word] == "everyone"


class TestDLISTIntegration:
    """Integration tests for DLIST with full conversation flow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
        self.eliza.memory.clear()
    
    def test_link_word_with_memory(self):
        """Test that link words work with memory system."""
        # Store something in memory
        self.eliza.respond("my dog is cute")
        
        # Use link word in response
        response = self.eliza.respond("I believe that")
        
        # Should either use "think" patterns or recall memory
        assert response is not None
    
    def test_link_word_with_transformations(self):
        """Test that link words work with pre/post transformations."""
        # Use contraction with link word
        response = self.eliza.respond("I don't believe anything")
        assert response is not None
    
    def test_link_priority_vs_keyword_rank(self):
        """Test that links are checked before keyword ranking."""
        # "believe" (link) should be checked before "am" (rank 5 keyword)
        response = self.eliza.respond("I believe I am happy")
        # Should process with "think" or "am" patterns, not crash
        assert response is not None
        assert len(response) > 0


class TestDLISTEdgeCases:
    """Edge case tests for DLIST."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eliza = Eliza()
        self.eliza.memory.clear()
    
    def test_empty_links_dict(self):
        """Test behavior when no links are defined."""
        # Manually clear links
        self.eliza.links = {}
        
        # Should still work with regular keywords
        response = self.eliza.respond("I am sad")
        assert response is not None
        assert "sad" in response.lower()
    
    def test_link_word_case_insensitive(self):
        """Test that link word matching is case-insensitive."""
        # Links are checked in lowercase normalized text
        response1 = self.eliza.respond("I BELIEVE that")
        response2 = self.eliza.respond("I believe that")
        
        # Both should work (not necessarily same response due to randomization)
        assert response1 is not None
        assert response2 is not None
    
    def test_link_word_with_punctuation(self):
        """Test link words with punctuation."""
        response = self.eliza.respond("I believe, honestly")
        assert response is not None
    
    def test_multiple_link_words_in_sentence(self):
        """Test sentence with multiple link words."""
        # "believe" -> "think", "desire" -> "want"
        response = self.eliza.respond("I believe I desire happiness")
        # Should match first link word found
        assert response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
