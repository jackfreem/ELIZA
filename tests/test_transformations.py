"""
Tests for transformation functionality
"""

import pytest
from eliza.transformations import Transformations


class TestPreTransformations:
    """Test pre-transformations (input normalization)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.transformations = Transformations()
    
    def test_contraction_expansion(self):
        """Test that contractions are expanded."""
        result = self.transformations.pre_transform("I'm happy")
        assert "i am" in result or "i'm" not in result.lower()
        
        result = self.transformations.pre_transform("don't")
        assert "do not" in result
    
    def test_synonym_normalization(self):
        """Test that synonyms are normalized."""
        result = self.transformations.pre_transform("mom")
        assert "mother" in result
    
    def test_keyword_preservation(self):
        """Test that keywords are preserved during normalization."""
        # Create transformations with keywords to preserve
        t = Transformations(preserve_keywords=["feel", "am"])
        
        result = t.pre_transform("I feel happy")
        assert "feel" in result  # Should not be normalized
    
    def test_lowercase_conversion(self):
        """Test that input is converted to lowercase."""
        result = self.transformations.pre_transform("HELLO WORLD")
        assert result == result.lower()


class TestPostTransformations:
    """Test post-transformations (response adjustment)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.transformations = Transformations()
    
    def test_pronoun_switching(self):
        """Test that pronouns are switched."""
        result = self.transformations.post_transform("I am happy")
        assert "you" in result.lower()
        # "I" should be changed to "you" (except in ELIZA's own words)
    
    def test_verb_form_adjustment(self):
        """Test that verb forms are adjusted."""
        result = self.transformations.post_transform("I am sad")
        assert "are" in result.lower()
    
    def test_is_not_changed(self):
        """Test that 'is' is NOT changed to 'are'."""
        result = self.transformations.post_transform("Your dog is cute")
        assert "is" in result.lower()
        # Should not have "are" where "is" should be
        assert result.lower().count("is") >= result.lower().count("are")
    
    def test_im_preservation(self):
        """Test that 'I'm' in ELIZA's responses is preserved."""
        result = self.transformations.post_transform("I'm here to listen")
        assert "i'm" in result.lower() or "I'm" in result
    
    def test_capitalization(self):
        """Test that first letter is capitalized."""
        result = self.transformations.post_transform("hello world")
        assert result[0].isupper()
    
    def test_tell_me_preservation(self):
        """Test that 'tell me' is preserved."""
        result = self.transformations.post_transform("Tell me more")
        assert "tell me" in result.lower()


class TestScriptTransformations:
    """Test transformations loaded from script."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from eliza.core import Eliza
        self.eliza = Eliza()
        self.transformations = self.eliza.transformations
    
    def test_script_pre_transforms(self):
        """Test that pre-transforms from script are used."""
        # Script should have contraction expansions
        result = self.transformations.pre_transform("I'm")
        assert "i am" in result or "i'm" not in result.lower()
    
    def test_script_post_transforms(self):
        """Test that post-transforms from script are used."""
        # Script should have pronoun switching
        result = self.transformations.post_transform("my dog")
        assert "your" in result.lower()

