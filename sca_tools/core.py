#!/usr/bin/env python3
"""SCA Framework Core Implementation

This module provides the main SCA framework that orchestrates all cognitive
architecture components.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

from .context_mapper import ContextMapperServer
from .decomposition import DecompositionServer
from .synthesis import SynthesisServer
from .memory import MemoryServer


@dataclass
class SCAResult:
    """Result from SCA processing"""
    query: str
    context_map: str
    tasks: List[Dict[str, Any]]
    synthesis: Dict[str, Any]
    timestamp: str
    processing_time: float
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class SCAFramework:
    """Main SCA Framework orchestrator"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        
        # Initialize component servers
        self.context_mapper = ContextMapperServer()
        self.decomposition = DecompositionServer()
        self.synthesis = SynthesisServer()
        self.memory = MemoryServer()
        
        self.logger.info("SCA Framework initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('SCA')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "max_context_size": 2000,
            "memory_enabled": True,
            "cache_ttl": 300,
            "max_tasks": 20,
            "synthesis_approaches": 3
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    self.logger.info(f"Loaded config from {config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
        
        return default_config
    
    async def process(self, query: str, context: Optional[str] = None) -> SCAResult:
        """Process a query through the complete SCA pipeline"""
        start_time = asyncio.get_event_loop().time()
        
        self.logger.info(f"Processing query: {query[:50]}...")
        
        try:
            # Step 1: Context Mapping
            self.logger.debug("Step 1: Context Mapping")
            context_map = await self.context_mapper.create_context_map(query)
            
            # Step 2: Task Decomposition
            self.logger.debug("Step 2: Task Decomposition")
            tasks = await self.decomposition.decompose_query(
                query, context_map, max_tasks=self.config["max_tasks"]
            )
            
            # Step 3: Collect perspectives for synthesis
            perspectives = [
                f"Context analysis: {context_map}",
                f"Task breakdown: {json.dumps([task.to_dict() for task in tasks[:3]])}",
                f"Original query: {query}"
            ]
            
            if context:
                perspectives.append(f"Additional context: {context}")
            
            # Step 4: Synthesis
            self.logger.debug("Step 3: Perspective Synthesis")
            synthesis_result = await self.synthesis.synthesize_perspectives(
                perspectives
            )
            
            # Step 5: Store in memory (if enabled)
            if self.config["memory_enabled"]:
                await self.memory.record_interaction(
                    content=f"Query: {query}\nResult: {synthesis_result}",
                    importance=self._calculate_importance(query, synthesis_result)
                )
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            result = SCAResult(
                query=query,
                context_map=context_map,
                tasks=[task.to_dict() for task in tasks],
                synthesis=synthesis_result,
                timestamp=datetime.now().isoformat(),
                processing_time=processing_time,
                confidence=self._calculate_confidence(synthesis_result)
            )
            
            self.logger.info(f"Processing completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise
    
    def process_sync(self, query: str, context: Optional[str] = None) -> SCAResult:
        """Synchronous wrapper for process method"""
        return asyncio.run(self.process(query, context))
    
    def _calculate_importance(self, query: str, synthesis: Dict[str, Any]) -> int:
        """Calculate importance score for memory storage"""
        # Simple heuristic based on query length and synthesis confidence
        base_score = min(len(query.split()) // 5, 5)
        
        # Boost score if synthesis has high confidence approaches
        if synthesis:
            max_confidence = max(
                approach.get('confidence', 0) 
                for approach in synthesis.values() 
                if isinstance(approach, dict)
            )
            confidence_boost = int(max_confidence * 3)
            base_score = min(base_score + confidence_boost, 5)
        
        return max(base_score, 1)
    
    def _calculate_confidence(self, synthesis: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        if not synthesis:
            return 0.5
        
        confidences = [
            approach.get('confidence', 0.5) 
            for approach in synthesis.values() 
            if isinstance(approach, dict) and 'confidence' in approach
        ]
        
        if not confidences:
            return 0.5
        
        # Weighted average with preference for higher confidences
        sorted_confidences = sorted(confidences, reverse=True)
        weights = [0.5, 0.3, 0.2][:len(sorted_confidences)]
        
        weighted_sum = sum(c * w for c, w in zip(sorted_confidences, weights))
        weight_sum = sum(weights[:len(sorted_confidences)])
        
        return weighted_sum / weight_sum
    
    async def search_memory(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memory for relevant past interactions"""
        if not self.config["memory_enabled"]:
            return []
        
        return await self.memory.search_memory(query, limit)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get framework statistics"""
        return {
            "version": "1.0.0",
            "config": self.config,
            "memory_enabled": self.config["memory_enabled"],
            "components": {
                "context_mapper": "active",
                "decomposition": "active", 
                "synthesis": "active",
                "memory": "active" if self.config["memory_enabled"] else "disabled"
            }
        }


# Convenience function for quick usage
async def process_query(query: str, context: Optional[str] = None, 
                       config_path: Optional[str] = None) -> SCAResult:
    """Convenience function to process a single query"""
    framework = SCAFramework(config_path)
    return await framework.process(query, context)


def process_query_sync(query: str, context: Optional[str] = None,
                      config_path: Optional[str] = None) -> SCAResult:
    """Synchronous convenience function to process a single query"""
    return asyncio.run(process_query(query, context, config_path))