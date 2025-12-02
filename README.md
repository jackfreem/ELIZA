# ELIZA

A faithful Python implementation of the groundbreaking 1966 ELIZA chatbot by Joseph Weizenbaum.

## What is ELIZA?

ELIZA was one of the first chatbots ever created, simulating a Rogerian psychotherapist through clever pattern matching and text manipulation. Despite its simplicity, ELIZA demonstrated how machines could create the illusion of understanding human language.

This implementation stays true to the original paper while using modern Python practices.

## What's Implemented

This implementation includes **~97% of the features** described in the original 1966 paper:

### ✅ Core Features
- **Pattern Matching** - Keywords trigger specific conversation patterns
- **Decomposition & Reassembly** - Extracts parts of your sentences and uses them in responses
- **Keyword Ranking** - Higher priority keywords are matched first
- **Transformations** - Normalizes input and adjusts responses (pronoun switching, contractions)
- **Memory System** - Remembers things you say and brings them up later
- **Script System** - Easy-to-edit conversation patterns in JSON format
- **DLIST (Link Words)** - Words that redirect to other keywords (e.g., "believe" uses "think" patterns)

### ❌ Not Implemented
- **NEWKEY mechanism** - Dynamic keyword switching (high complexity, low value)
- **Tag mechanism** - Systematic rule cycling (randomization works well enough)
- **NONE keyword** - Using default responses instead (simpler approach)

## Installation

1. Clone this repository
2. Install dependencies (optional, for testing):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Quick Start

### Try it out!

```bash
python3 main.py
```

Then have a conversation:

```
ELIZA: Is something troubling you?

You: my mother hates me
ELIZA: Tell me more about your family.

You: I feel sad
ELIZA: Do you often feel sad?

You: I believe nobody understands me
ELIZA: Can you think of anyone in particular?
```

### Use in Your Code

```python
from eliza.core import Eliza

# Create an ELIZA instance
eliza = Eliza()

# Have a conversation
response = eliza.respond("I am sad")
print(response)  # "Why are you sad?"

response = eliza.respond("I believe life is hard")
print(response)  # "What makes you think life is hard?"
```

### Running Tests

```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run all 101 tests
pytest tests/ -v

# Run specific test file
pytest tests/test_dlist.py -v
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

## How ELIZA Works

ELIZA creates the illusion of understanding through a simple but clever process:

1. **Pattern Matching** - Looks for keywords in your input ("sad", "mother", "feel")
2. **Decomposition** - Extracts parts of your sentence using patterns
3. **Reassembly** - Plugs those parts into response templates
4. **Transformations** - Switches pronouns so responses make sense

**Example:**
```
You: "I am sad"
  ↓ Keyword: "am"
  ↓ Pattern: ".*i am (.*)" captures "sad"
  ↓ Template: "Why are you {0}?"
  ↓ Result: "Why are you sad?"
```

### Link Words (DLIST)

Link words let you extend ELIZA's vocabulary without writing new patterns. When ELIZA sees a link word, it redirects to another keyword.

**Example:**
```
You: "I believe life is hard"
  ↓ "believe" links to "think"
  ↓ Uses "think" keyword's patterns
  ↓ Result: "What makes you think life is hard?"
```

Current links: `dislike→hate`, `believe→think`, `desire→want`, `require→need`, `nobody→everyone`, and more.

### Memory System

ELIZA remembers things you say (sentences with "my") and brings them up later:

```
You: my dog is cute
ELIZA: What about your dog is cute?

You: potato
ELIZA: Earlier you said your dog is cute.
```

## Customization

All conversation patterns are in `scripts/doctor.json`. You can:
- Add new keywords and patterns
- Add more link words
- Modify response templates
- Create entirely new conversation scripts

See `LEARNING_GUIDE.md` for detailed documentation on the script format.

## Learn More

- **`LEARNING_GUIDE.md`** - Detailed explanation of how ELIZA works
- **`FEATURE_PARITY.md`** - Comparison with the original 1966 paper
- **`DLIST_IMPLEMENTATION.md`** - Technical details on link words
- **`PROJECT_STRUCTURE.md`** - Code architecture overview

## References

- Weizenbaum, J. (1966). [ELIZA—a computer program for the study of natural language communication between man and machine](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf). Communications of the ACM, 9(1), 36-45.
