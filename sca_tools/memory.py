#!/usr/bin/env python3
"""Memory Server Implementation

This module provides persistent memory functionality for storing and
retrieving past interactions and insights.
"""

import asyncio
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import logging


@dataclass
class MemoryEntry:
    """Represents a memory entry"""
    id: str
    content: str
    timestamp: str
    importance: int
    category: str
    tags: List[str]
    context_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MemoryStats:
    """Memory system statistics"""
    total_entries: int
    total_size_mb: float
    oldest_entry: str
    newest_entry: str
    categories: Dict[str, int]
    importance_distribution: Dict[int, int]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MemoryServer:
    """Server for managing persistent memory storage and retrieval"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.logger = logging.getLogger('SCA.Memory')
        
        # Set up database path
        if db_path is None:
            memory_dir = Path.home() / '.sca' / 'memory'
            memory_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(memory_dir / 'sca_memory.db')
        
        self.db_path = db_path
        self._init_database()
        
        # Memory management settings
        self.max_entries = 10000
        self.max_size_mb = 100
        
        self.logger.info(f"Memory server initialized with database: {db_path}")
    
    def _init_database(self):
        """Initialize the SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create memories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    importance INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    context_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for faster searching
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_context_hash ON memories(context_hash)")
            
            # Create full-text search virtual table
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    content, tags, category,
                    content_id UNINDEXED
                )
            """)
            
            conn.commit()
    
    async def record_interaction(self, content: str, importance: int, 
                               category: str = "general", tags: Optional[List[str]] = None) -> bool:
        """Record a new interaction in memory"""
        try:
            # Generate unique ID
            content_hash = hashlib.md5(content.encode()).hexdigest()[:16]
            timestamp = datetime.now().isoformat()
            entry_id = f"{timestamp[:10]}_{content_hash}"
            
            # Process tags
            if tags is None:
                tags = self._extract_tags(content)
            tags_str = json.dumps(tags)
            
            # Create context hash for deduplication
            context_hash = hashlib.md5(f"{content[:100]}{category}".encode()).hexdigest()
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check for near-duplicates
                cursor.execute(
                    "SELECT id FROM memories WHERE context_hash = ? AND importance >= ?",
                    (context_hash, importance - 1)
                )
                
                if cursor.fetchone():
                    self.logger.debug("Similar memory already exists, skipping")
                    return False
                
                # Insert new memory
                cursor.execute("""
                    INSERT INTO memories (id, content, timestamp, importance, category, tags, context_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (entry_id, content, timestamp, importance, category, tags_str, context_hash))
                
                # Update FTS table
                cursor.execute("""
                    INSERT INTO memories_fts (content, tags, category, content_id)
                    VALUES (?, ?, ?, ?)
                """, (content, " ".join(tags), category, entry_id))
                
                conn.commit()
            
            self.logger.debug(f"Recorded memory: {entry_id}")
            
            # Perform cleanup if needed
            await self._cleanup_old_memories()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record interaction: {e}")
            return False
    
    async def search_memory(self, query: str, limit: int = 10, 
                          category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search memory for relevant entries"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Use FTS for text search
                if category:
                    cursor.execute("""
                        SELECT m.id, m.content, m.timestamp, m.importance, m.category, m.tags
                        FROM memories_fts f
                        JOIN memories m ON f.content_id = m.id
                        WHERE memories_fts MATCH ? AND m.category = ?
                        ORDER BY m.importance DESC, m.timestamp DESC
                        LIMIT ?
                    """, (query, category, limit))
                else:
                    cursor.execute("""
                        SELECT m.id, m.content, m.timestamp, m.importance, m.category, m.tags
                        FROM memories_fts f  
                        JOIN memories m ON f.content_id = m.id
                        WHERE memories_fts MATCH ?
                        ORDER BY m.importance DESC, m.timestamp DESC
                        LIMIT ?
                    """, (query, limit))
                
                results = cursor.fetchall()
                
                # Convert to list of dictionaries
                memories = []
                for row in results:
                    entry = {
                        'id': row[0],
                        'content': row[1],
                        'timestamp': row[2], 
                        'importance': row[3],
                        'category': row[4],
                        'tags': json.loads(row[5]) if row[5] else [],
                        'relevance_score': self._calculate_relevance(query, row[1])
                    }
                    memories.append(entry)
                
                return memories
                
        except Exception as e:
            self.logger.error(f"Failed to search memory: {e}")
            return []
    
    async def get_recent_insights(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent high-importance memories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, content, timestamp, importance, category, tags
                    FROM memories
                    WHERE importance >= 4
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
                
                results = cursor.fetchall()
                
                insights = []
                for row in results:
                    insight = {
                        'id': row[0],
                        'content': row[1][:200] + '...' if len(row[1]) > 200 else row[1],
                        'timestamp': row[2],
                        'importance': row[3],
                        'category': row[4],
                        'tags': json.loads(row[5]) if row[5] else []
                    }
                    insights.append(insight)
                
                return insights
                
        except Exception as e:
            self.logger.error(f"Failed to get recent insights: {e}")
            return []
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total entries
                cursor.execute("SELECT COUNT(*) FROM memories")
                total_entries = cursor.fetchone()[0]
                
                # Database size
                db_size_bytes = Path(self.db_path).stat().st_size
                db_size_mb = db_size_bytes / (1024 * 1024)
                
                # Date range
                cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM memories")
                date_range = cursor.fetchone()
                
                # Categories
                cursor.execute("SELECT category, COUNT(*) FROM memories GROUP BY category")
                categories = dict(cursor.fetchall())
                
                # Importance distribution
                cursor.execute("SELECT importance, COUNT(*) FROM memories GROUP BY importance")
                importance_dist = dict(cursor.fetchall())
                
                return {
                    'total_entries': total_entries,
                    'total_size_mb': round(db_size_mb, 2),
                    'oldest_entry': date_range[0] if date_range[0] else 'N/A',
                    'newest_entry': date_range[1] if date_range[1] else 'N/A', 
                    'categories': categories,
                    'importance_distribution': importance_dist,
                    'database_path': self.db_path
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get memory stats: {e}")
            return {}
    
    async def analyze_memory_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in stored memories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Most common tags
                cursor.execute("SELECT tags FROM memories WHERE tags != '[]'")
                all_tags = []
                for row in cursor.fetchall():
                    tags = json.loads(row[0])
                    all_tags.extend(tags)
                
                from collections import Counter
                tag_frequency = Counter(all_tags).most_common(10)
                
                # Category trends over time
                cursor.execute("""
                    SELECT 
                        DATE(timestamp) as date,
                        category,
                        COUNT(*) as count
                    FROM memories 
                    WHERE timestamp >= date('now', '-30 days')
                    GROUP BY DATE(timestamp), category
                    ORDER BY date DESC
                """)
                
                category_trends = cursor.fetchall()
                
                # Quality score (based on importance and recency)
                cursor.execute("""
                    SELECT AVG(
                        importance * 
                        (julianday('now') - julianday(timestamp)) / -365.0
                    ) as quality_score
                    FROM memories
                    WHERE timestamp >= date('now', '-90 days')
                """)
                
                quality_score = cursor.fetchone()[0] or 0
                
                return {
                    'top_tags': tag_frequency,
                    'category_trends': category_trends,
                    'quality_score': round(quality_score, 2),
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Failed to analyze memory patterns: {e}")
            return {}
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content"""
        import re
        
        # Simple tag extraction based on keywords
        tag_patterns = {
            'technical': r'\b(api|database|server|client|framework|library)\b',
            'programming': r'\b(python|javascript|react|node|sql)\b',
            'development': r'\b(build|implement|deploy|test|debug)\b',
            'analysis': r'\b(analyze|data|metrics|performance)\b',
            'design': r'\b(design|architecture|pattern|structure)\b'
        }
        
        tags = []
        content_lower = content.lower()
        
        for tag_type, pattern in tag_patterns.items():
            if re.search(pattern, content_lower):
                tags.append(tag_type)
        
        # Add specific technology tags
        tech_keywords = ['react', 'vue', 'angular', 'python', 'javascript', 'sql', 'api', 'database']
        for keyword in tech_keywords:
            if keyword in content_lower:
                tags.append(keyword)
        
        return list(set(tags))  # Remove duplicates
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate relevance score between query and content"""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(content_words)
        return len(intersection) / len(query_words)
    
    async def _cleanup_old_memories(self):
        """Clean up old memories if limits are exceeded"""
        try:
            stats = await self.get_memory_stats()
            
            if stats['total_entries'] > self.max_entries:
                # Remove oldest low-importance memories
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Delete oldest memories with importance <= 2
                    cursor.execute("""
                        DELETE FROM memories
                        WHERE id IN (
                            SELECT id FROM memories
                            WHERE importance <= 2
                            ORDER BY timestamp ASC
                            LIMIT ?
                        )
                    """, (stats['total_entries'] - self.max_entries,))
                    
                    # Clean up FTS table
                    cursor.execute("DELETE FROM memories_fts WHERE content_id NOT IN (SELECT id FROM memories)")
                    
                    conn.commit()
                    
                self.logger.info(f"Cleaned up old memories, removed {cursor.rowcount} entries")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup memories: {e}")
    
    async def record_session_start(self, session_context: str) -> str:
        """Record the start of a new session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        await self.record_interaction(
            content=f"Session started: {session_context}",
            importance=3,
            category="session",
            tags=["session_start"]
        )
        return session_id
    
    async def end_session(self, session_summary: str) -> bool:
        """Record the end of a session with summary"""
        return await self.record_interaction(
            content=f"Session ended: {session_summary}",
            importance=3,
            category="session",
            tags=["session_end"]
        )


# MCP Server entry point
if __name__ == "__main__":
    import sys
    
    async def main():
        server = MemoryServer()
        
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "stats":
                stats = await server.get_memory_stats()
                print(json.dumps(stats, indent=2))
                
            elif command == "search" and len(sys.argv) > 2:
                query = " ".join(sys.argv[2:])
                results = await server.search_memory(query)
                print(f"\nSearch results for: {query}")
                for result in results:
                    print(f"- [{result['importance']}] {result['content'][:100]}...")
                    
            elif command == "record" and len(sys.argv) > 3:
                content = sys.argv[2]
                importance = int(sys.argv[3]) if len(sys.argv) > 3 else 3
                success = await server.record_interaction(content, importance)
                print(f"Recording {'successful' if success else 'failed'}")
                
            elif command == "insights":
                insights = await server.get_recent_insights()
                print("\nRecent insights:")
                for insight in insights:
                    print(f"- [{insight['importance']}] {insight['content']}")
                    
            else:
                print("Unknown command")
        else:
            print("SCA Memory Server")
            print("Usage: python memory.py <command>")
            print("Commands: stats, search <query>, record <content> [importance], insights")
    
    asyncio.run(main())