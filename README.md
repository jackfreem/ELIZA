# ELIZA

Python based implementation of the ELIZA paper for natural language communication.

## Overview

This is a complete implementation of the ELIZA chatbot system described in Joseph Weizenbaum's 1966 paper. ELIZA uses pattern matching, decomposition rules, and reassembly rules to create conversational responses.

## Features

- ✅ Pattern matching with keyword priorities
- ✅ Decomposition and reassembly rules
- ✅ Pre and post-transformations
- ✅ Script system (loads from JSON)
- ✅ Memory system (MEMORY pseudo-keyword)
- ✅ **DLIST (Link Words)** - Words that redirect to other keywords

## Installation

1. Clone this repository
2. Install dependencies (optional, for testing):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```python
from eliza.core import Eliza

eliza = Eliza()
response = eliza.respond("I am sad")
print(response)  # "Why are you sad?"
```

### Command Line Interface

```bash
python3 main.py
```

### Running Tests

```bash
# Install pytest first (in virtual environment)
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core.py -v
```

## Project Structure

```
ELIZA/
├── eliza/
│   ├── __init__.py
│   ├── core.py              # Main ELIZA engine
│   ├── script.py            # Script loader
│   ├── transformations.py   # Text transformations
│   └── memory.py            # Memory system
├── scripts/
│   └── doctor.json          # DOCTOR script
├── tests/                   # Test suite
│   ├── test_core.py
│   ├── test_transformations.py
│   ├── test_script.py
│   └── test_memory.py
├── main.py                  # CLI interface
└── requirements.txt         # Dependencies
```

## Script Format

Scripts are defined in JSON format. See `scripts/doctor.json` for an example.

### DLIST (Link Words)

DLIST allows words to redirect to other keywords for processing. This extends keyword coverage without duplicating patterns.

**Example from `doctor.json`:**
```json
"links": {
  "dislike": "hate",
  "believe": "think",
  "desire": "want",
  "require": "need",
  "nobody": "everyone"
}
```

**How it works:**
- User says: "I believe life is hard"
- "believe" redirects to "think" keyword
- Uses "think" keyword's patterns: "What makes you think life is hard?"

**Benefits:**
- Extend vocabulary without writing new patterns
- Simple and efficient
- No pattern duplication

## Learning Resources

- See `LEARNING_GUIDE.md` for a detailed explanation of how ELIZA works
- See `PROJECT_STRUCTURE.md` for implementation details

## References

- Weizenbaum, J. (1966). ELIZA—a computer program for the study of natural language communication between man and machine. Communications of the ACM, 9(1), 36-45.
