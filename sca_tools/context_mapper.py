#!/usr/bin/env python3
"""Context Mapper Server Implementation

This module provides context mapping functionality for understanding
the structure and relationships within complex problems.
"""

import asyncio
import json
import re
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import logging


@dataclass
class ConceptNode:
    """Represents a concept in the context map"""
    name: str
    category: str
    importance: float
    connections: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category, 
            "importance": self.importance,
            "connections": self.connections
        }


class ContextMapperServer:
    """Server for creating context maps from queries"""
    
    def __init__(self):
        self.logger = logging.getLogger('SCA.ContextMapper')
        
        # Domain-specific keywords and categories
        self.technical_keywords = {
            'software': ['api', 'database', 'server', 'client', 'framework', 'library', 
                        'code', 'function', 'class', 'method', 'algorithm', 'data structure'],
            'web': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'node', 'express'],
            'data': ['analysis', 'visualization', 'machine learning', 'ai', 'model', 'dataset'],
            'business': ['user', 'customer', 'revenue', 'marketing', 'sales', 'product', 'strategy'],
            'security': ['authentication', 'authorization', 'encryption', 'security', 'vulnerability'],
            'infrastructure': ['docker', 'kubernetes', 'cloud', 'aws', 'deployment', 'monitoring']
        }
        
        # Action verbs that indicate process steps
        self.action_verbs = [
            'create', 'build', 'implement', 'design', 'develop', 'analyze', 'optimize',
            'integrate', 'configure', 'deploy', 'test', 'debug', 'refactor', 'migrate'
        ]
    
    async def create_context_map(self, query: str) -> str:
        """Create a context map for the given query"""
        self.logger.debug(f"Creating context map for: {query[:100]}...")
        
        try:
            # Extract concepts and relationships
            concepts = self._extract_concepts(query)
            relationships = self._identify_relationships(query, concepts)
            
            # Generate Mermaid diagram
            mermaid_diagram = self._generate_mermaid_diagram(concepts, relationships)
            
            return mermaid_diagram
            
        except Exception as e:
            self.logger.error(f"Failed to create context map: {e}")
            return self._generate_fallback_diagram(query)
    
    def _extract_concepts(self, query: str) -> List[ConceptNode]:
        """Extract key concepts from the query"""
        concepts = []
        query_lower = query.lower()
        words = re.findall(r'\b\w+\b', query_lower)
        
        # Extract main subject (usually first noun or key term)
        main_subject = self._identify_main_subject(query)
        if main_subject:
            concepts.append(ConceptNode(
                name=main_subject,
                category="main",
                importance=1.0,
                connections=[]
            ))
        
        # Extract technical concepts
        for category, keywords in self.technical_keywords.items():
            found_keywords = [kw for kw in keywords if kw in query_lower]
            for keyword in found_keywords:
                concepts.append(ConceptNode(
                    name=keyword.title(),
                    category=category,
                    importance=0.8,
                    connections=[]
                ))
        
        # Extract action concepts
        found_actions = [verb for verb in self.action_verbs if verb in query_lower]
        for action in found_actions:
            concepts.append(ConceptNode(
                name=action.title(),
                category="action",
                importance=0.7,
                connections=[]
            ))
        
        # Remove duplicates and limit to most important
        unique_concepts = {}
        for concept in concepts:
            if concept.name not in unique_concepts:
                unique_concepts[concept.name] = concept
            elif concept.importance > unique_concepts[concept.name].importance:
                unique_concepts[concept.name] = concept
        
        return list(unique_concepts.values())[:15]  # Limit to prevent overcrowding
    
    def _identify_main_subject(self, query: str) -> Optional[str]:
        """Identify the main subject of the query"""
        # Common patterns for main subjects
        patterns = [
            r'\b(\w+)\s+(?:system|application|app|platform|tool|service)',
            r'build\s+(?:a|an)?\s+(\w+(?:\s+\w+)?)',
            r'create\s+(?:a|an)?\s+(\w+(?:\s+\w+)?)',
            r'implement\s+(?:a|an)?\s+(\w+(?:\s+\w+)?)',
            r'develop\s+(?:a|an)?\s+(\w+(?:\s+\w+)?)',
            r'design\s+(?:a|an)?\s+(\w+(?:\s+\w+)?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                return match.group(1).title()
        
        # Fallback: look for capitalized words (proper nouns)
        capitalized = re.findall(r'\b[A-Z]\w+\b', query)
        if capitalized:
            return capitalized[0]
        
        return None
    
    def _identify_relationships(self, query: str, concepts: List[ConceptNode]) -> List[Tuple[str, str, str]]:
        """Identify relationships between concepts"""
        relationships = []
        
        # Simple relationship patterns
        relationship_patterns = {
            r'(\w+)\s+uses?\s+(\w+)': 'uses',
            r'(\w+)\s+connects?\s+to\s+(\w+)': 'connects',
            r'(\w+)\s+depends\s+on\s+(\w+)': 'depends',
            r'(\w+)\s+integrates?\s+with\s+(\w+)': 'integrates',
            r'(\w+)\s+manages?\s+(\w+)': 'manages',
            r'(\w+)\s+processes?\s+(\w+)': 'processes'
        }
        
        query_lower = query.lower()
        
        for pattern, relationship_type in relationship_patterns.items():
            matches = re.findall(pattern, query_lower)
            for match in matches:
                source, target = match
                relationships.append((source.title(), relationship_type, target.title()))
        
        # Add implicit relationships based on context
        concept_names = [c.name.lower() for c in concepts]
        
        # If we have a main subject, connect actions to it
        main_concepts = [c for c in concepts if c.category == "main"]
        action_concepts = [c for c in concepts if c.category == "action"]
        
        for main_concept in main_concepts:
            for action_concept in action_concepts:
                relationships.append((action_concept.name, "modifies", main_concept.name))
        
        # Connect technical components to main subject
        technical_concepts = [c for c in concepts if c.category in ['software', 'web', 'data']]
        for main_concept in main_concepts:
            for tech_concept in technical_concepts:
                relationships.append((main_concept.name, "requires", tech_concept.name))
        
        return relationships[:20]  # Limit relationships to prevent overcrowding
    
    def _generate_mermaid_diagram(self, concepts: List[ConceptNode], relationships: List[Tuple[str, str, str]]) -> str:
        """Generate Mermaid diagram from concepts and relationships"""
        diagram_lines = ["graph TD"]
        
        # Add concept nodes with styling based on category
        node_styles = {
            "main": ":::mainStyle",
            "action": ":::actionStyle", 
            "software": ":::techStyle",
            "web": ":::webStyle",
            "data": ":::dataStyle",
            "business": ":::businessStyle",
            "security": ":::securityStyle",
            "infrastructure": ":::infraStyle"
        }
        
        # Generate node IDs (replace spaces and special chars)
        node_ids = {}
        for i, concept in enumerate(concepts):
            clean_name = re.sub(r'[^\w]', '', concept.name)
            node_id = f"{clean_name}_{i}"
            node_ids[concept.name] = node_id
            
            style = node_styles.get(concept.category, "")
            diagram_lines.append(f'    {node_id}["{concept.name}"]{style}')
        
        # Add relationships
        for source, rel_type, target in relationships:
            source_id = node_ids.get(source)
            target_id = node_ids.get(target)
            
            if source_id and target_id:
                arrow_style = self._get_arrow_style(rel_type)
                diagram_lines.append(f'    {source_id} {arrow_style} {target_id}')
        
        # Add styling definitions
        diagram_lines.extend([
            "",
            "    classDef mainStyle fill:#2563eb,stroke:#1e40af,stroke-width:3px,color:#fff",
            "    classDef actionStyle fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff", 
            "    classDef techStyle fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff",
            "    classDef webStyle fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff",
            "    classDef dataStyle fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff",
            "    classDef businessStyle fill:#06b6d4,stroke:#0891b2,stroke-width:2px,color:#fff",
            "    classDef securityStyle fill:#f97316,stroke:#ea580c,stroke-width:2px,color:#fff",
            "    classDef infraStyle fill:#84cc16,stroke:#65a30d,stroke-width:2px,color:#fff"
        ])
        
        return "\n".join(diagram_lines)
    
    def _get_arrow_style(self, relationship_type: str) -> str:
        """Get appropriate arrow style for relationship type"""
        arrow_styles = {
            'uses': '-->', 
            'connects': '<-->', 
            'depends': '-.->',
            'integrates': '==>',
            'manages': '-->',
            'processes': '-->',
            'modifies': '-->',
            'requires': '-.->'
        }
        return arrow_styles.get(relationship_type, '-->')
    
    def _generate_fallback_diagram(self, query: str) -> str:
        """Generate a simple fallback diagram when extraction fails"""
        words = query.split()[:5]  # Take first 5 words
        clean_words = [re.sub(r'[^\w]', '', word) for word in words if len(word) > 2]
        
        diagram_lines = ["graph TD"]
        
        if clean_words:
            main_word = clean_words[0]
            diagram_lines.append(f'    A["{main_word.title()}"]:::mainStyle')
            
            for i, word in enumerate(clean_words[1:], 1):
                node_id = chr(ord('B') + i - 1)
                diagram_lines.append(f'    {node_id}["{word.title()}"]')
                diagram_lines.append(f'    A --> {node_id}')
        
        diagram_lines.append("    classDef mainStyle fill:#2563eb,stroke:#1e40af,stroke-width:3px,color:#fff")
        
        return "\n".join(diagram_lines)


# MCP Server entry point
if __name__ == "__main__":
    import sys
    import json
    
    async def main():
        server = ContextMapperServer()
        
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            result = await server.create_context_map(query)
            print(result)
        else:
            # Interactive mode
            print("SCA Context Mapper Server")
            print("Enter queries to generate context maps (Ctrl+C to exit)")
            
            try:
                while True:
                    query = input("\nQuery: ")
                    if query.strip():
                        result = await server.create_context_map(query)
                        print("\nContext Map:")
                        print(result)
            except KeyboardInterrupt:
                print("\nGoodbye!")
    
    asyncio.run(main())