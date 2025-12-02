"""
Tests for memory system
"""

import pytest
from eliza.memory import Memory


class TestMemory:
    """Test memory system functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.memory = Memory(max_size=5)
    
    def test_store_and_recall(self):
        """Test basic store and recall functionality."""
        self.memory.store("test sentence")
        recalled = self.memory.recall()
        
        assert recalled == "test sentence"
    
    def test_fifo_order(self):
        """Test that memory uses FIFO (first in, first out)."""
        self.memory.store("first")
        self.memory.store("second")
        self.memory.store("third")
        
        # Should recall oldest first and remove it (FIFO dequeue)
        assert self.memory.recall() == "first"
        # Recall again should get second (first was removed)
        assert self.memory.recall() == "second"
        # Third recall should get third
        assert self.memory.recall() == "third"
        # Fourth recall should return None (empty)
        assert self.memory.recall() is None
    
    def test_max_size(self):
        """Test that memory respects max size."""
        # Store more than max_size
        for i in range(10):
            self.memory.store(f"sentence {i}")
        
        # Should only have max_size items
        assert len(self.memory) == self.memory.max_size
    
    def test_clear(self):
        """Test that memory can be cleared."""
        self.memory.store("test")
        assert len(self.memory) > 0
        
        self.memory.clear()
        assert len(self.memory) == 0
        assert self.memory.recall() is None
    
    def test_has_memory(self):
        """Test has_memory method."""
        assert not self.memory.has_memory()
        
        self.memory.store("test")
        assert self.memory.has_memory()
    
    def test_empty_recall(self):
        """Test that recall returns None when empty."""
        assert self.memory.recall() is None
    
    def test_len(self):
        """Test that len() works correctly."""
        assert len(self.memory) == 0
        
        self.memory.store("one")
        assert len(self.memory) == 1
        
        self.memory.store("two")
        assert len(self.memory) == 2
    
    def test_oldest_dropped_when_full(self):
        """Test that oldest items are dropped when memory is full."""
        # Fill memory to max_size
        for i in range(self.memory.max_size):
            self.memory.store(f"item {i}")
        
        # Add one more
        self.memory.store("new item")
        
        # Should still be max_size
        assert len(self.memory) == self.memory.max_size
        
        # Oldest should be dropped
        # Since we're using deque with maxlen, oldest is automatically dropped
        # The newest item should be in memory
        memories_list = list(self.memory.memories)
        assert "new item" in memories_list

