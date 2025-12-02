"""
Memory system for ELIZA

Implements the MEMORY pseudo-keyword from the original ELIZA paper.
When "my" is the highest-ranked keyword, sentences are stored in memory.
When no keyword matches, MEMORY can be used to reference earlier statements.
"""

from typing import List, Optional, Deque
from collections import deque


class Memory:
    """
    Memory system for ELIZA.
    
    Stores transformed sentences when "my" is the highest-ranked keyword.
    References stored memories when no keyword matches.
    """
    
    def __init__(self, max_size: int = 5):
        """
        Initialize memory system.
        
        Args:
            max_size: Maximum number of memories to store (FIFO)
        """
        self.memories: Deque[str] = deque(maxlen=max_size)
        self.max_size = max_size
        self._recall_index = 0  # Track which memory to recall next
    
    def store(self, sentence: str) -> None:
        """
        Store a sentence in memory.
        
        Called when "my" is the highest-ranked keyword and a pattern matches.
        The sentence should be transformed (post-transformed) before storing.
        
        Args:
            sentence: The transformed sentence to store
        """
        if sentence and sentence.strip():
            self.memories.append(sentence.strip())
            # Reset recall index when new memory is added
            # This ensures we start from the beginning of the queue
            self._recall_index = 0
    
    def recall(self, remove: bool = True) -> Optional[str]:
        """
        Recall a memory from storage.
        
        By default, removes the memory after recalling (FIFO dequeue).
        This matches the original ELIZA behavior - memories are consumed.
        
        Args:
            remove: If True, remove the recalled memory (dequeue) - default.
                   If False, just peek at the memory without removing.
        
        Returns:
            A stored memory, or None if memory is empty
        """
        if not self.memories:
            return None
        
        if remove:
            # Remove oldest memory (true FIFO dequeue)
            # Reset recall index since we're removing
            self._recall_index = 0
            return self.memories.popleft()
        else:
            # Just peek at the oldest memory without removing
            return self.memories[0]
    
    def clear(self) -> None:
        """Clear all memories."""
        self.memories.clear()
        self._recall_index = 0
    
    def has_memory(self) -> bool:
        """Check if there are any stored memories."""
        return len(self.memories) > 0
    
    def __len__(self) -> int:
        """Return number of stored memories."""
        return len(self.memories)

