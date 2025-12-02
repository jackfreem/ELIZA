# ELIZA Project Structure & Implementation Overview

## Project Structure

```
ELIZA/
├── eliza/
│   ├── __init__.py              # Package initialization
│   ├── core.py                  # Core ELIZA engine (pattern matching, decomposition, reassembly)
│   ├── script.py                # Script loading and management (DOCTOR script)
│   ├── transformations.py       # Text preprocessing and transformations
│   └── memory.py                # Memory system (optional, for remembering context)
│
├── scripts/
│   └── doctor.json              # DOCTOR script definition (keywords, decomposition rules, reassembly rules)
│
├── tests/
│   ├── __init__.py
│   ├── test_core.py             # Tests for core ELIZA functionality
│   ├── test_script.py           # Tests for script loading
│   ├── test_transformations.py  # Tests for text preprocessing
│   └── test_memory.py           # Tests for memory system
│
├── examples/
│   └── demo.py                  # Example usage and demonstration
│
├── main.py                      # CLI entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## Implementation Overview

### Phase 1: Core Architecture

#### 1.1 Text Transformations (`transformations.py`)
- **Purpose**: Preprocess user input before pattern matching
- **Key Functions**:
  - Normalize punctuation and capitalization
  - Handle contractions (e.g., "I'm" → "I am")
  - Apply word substitutions (e.g., "you're" → "you are")
  - Clean and tokenize input

#### 1.2 Script System (`script.py`)
- **Purpose**: Load and manage conversation scripts (like DOCTOR)
- **Key Components**:
  - Script data structure (keywords, decomposition rules, reassembly rules)
  - Script loader (from JSON)
  - Keyword priority system
  - Rule matching logic

#### 1.3 Core Engine (`core.py`)
- **Purpose**: Main ELIZA processing logic
- **Key Components**:
  - **Pattern Matching**: Find keywords in user input
  - **Decomposition Rules**: Break sentences into parts using patterns
  - **Reassembly Rules**: Construct responses from matched patterns
  - **Keyword Priority**: Handle multiple keyword matches
  - **Response Selection**: Choose appropriate response template

### Phase 2: DOCTOR Script Implementation

#### 2.1 Script Definition (`scripts/doctor.json`)
- **Structure**:
  ```json
  {
    "keywords": [
      {
        "word": "mother",
        "rank": 10,
        "decomposition": [
          {
            "pattern": ".* mother .*",
            "reassembly": [
              "Tell me more about your family.",
              "Who else in your family?"
            ]
          }
        ]
      }
    ],
    "pre": [
      ["dont", "don't"],
      ["cant", "can't"]
    ],
    "post": [
      ["am", "are"],
      ["your", "my"]
    ],
    "synon": {
      "be": ["am", "is", "are", "was"]
    },
    "quit": ["bye", "goodbye", "quit", "exit"]
  }
  ```

#### 2.2 Key DOCTOR Patterns
- Greeting responses
- Reflection patterns (e.g., "I feel X" → "Do you often feel X?")
- Family-related keywords
- Memory integration (optional)

### Phase 3: Advanced Features

#### 3.1 Memory System (`memory.py`)
- **Purpose**: Remember and reference previous conversation context
- **Features**:
  - Store important facts mentioned by user
  - Reference memory in responses
  - Memory decay/forgetting mechanism

#### 3.2 Response Variability
- Multiple reassembly rules per decomposition pattern
- Random selection to avoid repetition
- Context-aware response selection

### Phase 4: User Interface

#### 4.1 CLI Interface (`main.py`)
- Interactive conversation loop
- Command-line arguments
- Exit handling
- Pretty printing of responses

#### 4.2 Example Usage (`examples/demo.py`)
- Demonstration of ELIZA capabilities
- Sample conversations
- Usage examples

### Phase 5: Testing & Refinement

#### 5.1 Unit Tests
- Test each component in isolation
- Test pattern matching accuracy
- Test decomposition/reassembly correctness
- Test edge cases

#### 5.2 Integration Tests
- End-to-end conversation tests
- Script loading tests
- Memory system tests

## Key Concepts from the Paper

### 1. Pattern Matching
- Keywords are matched in order of priority (rank)
- Patterns use regular expressions or similar matching
- Multiple keywords can match, highest priority wins

### 2. Decomposition Rules
- Break input into parts using patterns
- Capture groups for reassembly
- Example: "I am X" → captures X for use in response

### 3. Reassembly Rules
- Multiple response templates per decomposition pattern
- Use captured groups from decomposition
- Apply post-transformations (e.g., "your" → "my")

### 4. Transformations
- **Pre-transformations**: Applied before matching (normalization)
- **Post-transformations**: Applied to responses (pronoun switching)

### 5. Memory (Optional)
- Store important information
- Reference in later responses
- "Earlier you mentioned that..."

## Implementation Order

1. **Start Simple**: Basic pattern matching and response generation
2. **Add Transformations**: Text preprocessing and post-processing
3. **Implement Script System**: Load DOCTOR script from JSON
4. **Add Decomposition/Reassembly**: Full rule system
5. **Enhance with Memory**: Optional memory system
6. **Polish UI**: Better CLI and examples
7. **Test Thoroughly**: Comprehensive test suite

## Dependencies

- `re` (built-in): Regular expressions for pattern matching
- `json` (built-in): Script loading
- `random` (built-in): Response selection
- `typing` (built-in): Type hints
- `pytest` (optional): Testing framework

## Notes

- Stay true to the paper's algorithm
- DOCTOR script should match classic ELIZA behavior
- Keep it simple - ELIZA is intentionally simple
- Focus on pattern matching, not understanding

