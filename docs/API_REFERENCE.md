# 📚 SCA API Reference

## MCP Server Interfaces

### Context Mapper Server

#### `create_context_map(query: str) -> str`
Analyzes the overall structure and relationships of a given query.

**Parameters:**
- `query` (str): Input query or problem statement

**Returns:**
- Mermaid diagram representing concept relationships

**Example:**
```python
from sca_tools import context_mapper_server

result = context_mapper_server.create_context_map(
    "Implement user authentication system"
)
print(result)  # Returns Mermaid diagram code
```

### Decomposition Server

#### `decompose_query(query: str, context: str) -> List[Task]`
Breaks down complex problems into actionable subtasks.

**Parameters:**
- `query` (str): Problem statement
- `context` (str): Context from mapper server

**Returns:**
- List of Task objects with priorities and dependencies

**Task Object:**
```python
{
    "id": "task_001",
    "title": "Design database schema",
    "priority": 5,
    "dependencies": [],
    "estimated_time": "2h"
}
```

### Synthesis Server  

#### `synthesize_perspectives(inputs: List[str]) -> SynthesisResult`
Integrates multiple perspectives using dialectical synthesis.

**Parameters:**
- `inputs` (List[str]): Multiple information sources or viewpoints

**Returns:**
- SynthesisResult object with integrated solutions

**SynthesisResult Object:**
```python
{
    "conservative_approach": {
        "description": "Low-risk traditional approach",
        "confidence": 0.9,
        "pros": ["Well-tested", "Low risk"],
        "cons": ["Limited innovation"]
    },
    "balanced_approach": {
        "description": "Balanced risk-reward approach", 
        "confidence": 0.85,
        "pros": ["Good balance", "Proven elements"],
        "cons": ["Moderate complexity"]
    },
    "innovative_approach": {
        "description": "High-innovation cutting-edge approach",
        "confidence": 0.7,
        "pros": ["High innovation", "Future-proof"],
        "cons": ["Higher risk", "Unproven"]
    }
}
```

### Memory Server

#### `search_memory(query: str, limit: int = 10) -> List[Memory]`
Searches persistent memory for relevant information.

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum number of results

**Returns:**
- List of Memory objects

#### `record_interaction(content: str, importance: int) -> bool`
Records new information in persistent memory.

**Parameters:**
- `content` (str): Content to store
- `importance` (int): Importance level (1-5)

**Returns:**
- Boolean indicating success

## Configuration

### MCP Server Configuration
```json
{
  "mcpServers": {
    "sca-context-mapper": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "sca_tools.context_mapper_server"],
      "env": {}
    },
    "sca-decomposition": {
      "type": "stdio", 
      "command": "python3",
      "args": ["-m", "sca_tools.decomposition_server"],
      "env": {}
    },
    "sca-synthesis": {
      "type": "stdio",
      "command": "python3", 
      "args": ["-m", "sca_tools.synthesis_server"],
      "env": {}
    }
  }
}
```

### Environment Variables
```bash
SCA_MEMORY_PATH=/path/to/memory/storage
SCA_LOG_LEVEL=INFO
SCA_MAX_MEMORY_SIZE=1GB
```

## Error Handling

All SCA servers return standardized error responses:

```python
{
    "error": {
        "code": "INVALID_INPUT",
        "message": "Query parameter cannot be empty",
        "details": {
            "parameter": "query",
            "received": ""
        }
    }
}
```

## Rate Limits

- Context Mapper: 100 requests/minute
- Decomposition: 50 requests/minute  
- Synthesis: 25 requests/minute
- Memory Operations: 1000 requests/minute

For more examples, see the [examples/](../examples/) directory.