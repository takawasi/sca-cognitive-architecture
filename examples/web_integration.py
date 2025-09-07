#!/usr/bin/env python3
"""SCA Framework Web Integration Examples

This script shows how to integrate SCA with web frameworks like FastAPI and Flask.
"""

import asyncio
import json
from typing import Optional
from dataclasses import asdict

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not installed. Install with: pip install fastapi uvicorn")

try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not installed. Install with: pip install flask")

from sca_tools import SCAFramework


class QueryRequest(BaseModel):
    """Request model for SCA queries"""
    query: str
    context: Optional[str] = None
    max_tasks: Optional[int] = 20


class ComponentRequest(BaseModel):
    """Request model for individual components"""
    query: str
    component: str  # 'context', 'decompose', 'synthesize'
    options: Optional[dict] = None


# Global SCA instance (in production, use proper dependency injection)
sca_framework = None


def get_sca_framework() -> SCAFramework:
    """Get or create SCA framework instance"""
    global sca_framework
    if sca_framework is None:
        sca_framework = SCAFramework()
    return sca_framework


# FastAPI Application
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="SCA Framework API",
        description="Symbiotic Cognitive Architecture API for AI collaboration",
        version="1.0.0"
    )
    
    @app.get("/")
    async def root():
        """API root endpoint"""
        return {
            "message": "SCA Framework API",
            "version": "1.0.0",
            "docs": "/docs",
            "endpoints": {
                "process": "/api/process",
                "context": "/api/context",
                "decompose": "/api/decompose", 
                "synthesize": "/api/synthesize",
                "memory": "/api/memory"
            }
        }
    
    @app.post("/api/process")
    async def process_query(request: QueryRequest):
        """Process a query through the complete SCA pipeline"""
        try:
            sca = get_sca_framework()
            result = await sca.process(request.query, request.context)
            
            return {
                "success": True,
                "data": result.to_dict()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/context")
    async def create_context_map(request: QueryRequest):
        """Create context map for a query"""
        try:
            sca = get_sca_framework()
            context_map = await sca.context_mapper.create_context_map(request.query)
            
            return {
                "success": True,
                "data": {
                    "query": request.query,
                    "context_map": context_map
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/decompose")
    async def decompose_query(request: QueryRequest):
        """Decompose query into tasks"""
        try:
            sca = get_sca_framework()
            context = request.context or ""
            
            tasks = await sca.decomposition.decompose_query(
                request.query, context, request.max_tasks
            )
            
            return {
                "success": True,
                "data": {
                    "query": request.query,
                    "context": context,
                    "tasks": [task.to_dict() for task in tasks]
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/synthesize")
    async def synthesize_perspectives(perspectives: list[str]):
        """Synthesize multiple perspectives"""
        try:
            sca = get_sca_framework()
            result = await sca.synthesis.synthesize_perspectives(perspectives)
            
            return {
                "success": True,
                "data": {
                    "perspectives": perspectives,
                    "synthesis": result
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/memory/search")
    async def search_memory(query: str, limit: int = 10):
        """Search memory for relevant entries"""
        try:
            sca = get_sca_framework()
            results = await sca.search_memory(query, limit)
            
            return {
                "success": True,
                "data": {
                    "query": query,
                    "results": results
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/memory/stats")
    async def get_memory_stats():
        """Get memory system statistics"""
        try:
            sca = get_sca_framework()
            stats = await sca.memory.get_memory_stats()
            
            return {
                "success": True,
                "data": {"stats": stats}
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        try:
            sca = get_sca_framework()
            stats = sca.get_stats()
            
            return {
                "status": "healthy",
                "timestamp": asyncio.get_event_loop().time(),
                "framework_stats": stats
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Flask Application
if FLASK_AVAILABLE:
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def flask_root():
        """Flask root endpoint"""
        return jsonify({
            "message": "SCA Framework API (Flask)",
            "version": "1.0.0",
            "endpoints": {
                "process": "/api/process",
                "context": "/api/context",
                "decompose": "/api/decompose"
            }
        })
    
    @flask_app.route('/api/process', methods=['POST'])
    def flask_process_query():
        """Process query endpoint for Flask"""
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "Query is required"}), 400
            
            query = data['query']
            context = data.get('context')
            
            # Flask doesn't handle async natively, so we need to run in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                sca = get_sca_framework()
                result = loop.run_until_complete(sca.process(query, context))
                
                return jsonify({
                    "success": True,
                    "data": result.to_dict()
                })
            finally:
                loop.close()
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @flask_app.route('/api/context', methods=['POST'])
    def flask_create_context():
        """Create context map for Flask"""
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "Query is required"}), 400
            
            query = data['query']
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                sca = get_sca_framework()
                context_map = loop.run_until_complete(
                    sca.context_mapper.create_context_map(query)
                )
                
                return jsonify({
                    "success": True,
                    "data": {
                        "query": query,
                        "context_map": context_map
                    }
                })
            finally:
                loop.close()
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Client example
class SCAClient:
    """Client for SCA API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        
    async def process_query(self, query: str, context: Optional[str] = None) -> dict:
        """Process query via API"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            payload = {"query": query}
            if context:
                payload["context"] = context
                
            async with session.post(f"{self.base_url}/api/process", json=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result["data"]
                else:
                    error = await resp.text()
                    raise Exception(f"API Error: {error}")
    
    async def create_context_map(self, query: str) -> str:
        """Create context map via API"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            payload = {"query": query}
            async with session.post(f"{self.base_url}/api/context", json=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result["data"]["context_map"]
                else:
                    error = await resp.text()
                    raise Exception(f"API Error: {error}")


async def demo_client():
    """Demo SCA client usage"""
    print("📱 SCA Client Demo")
    print("=" * 30)
    
    # This assumes SCA API server is running
    client = SCAClient("http://localhost:8000")
    
    try:
        query = "Create a REST API for user management"
        print(f"Query: {query}\n")
        
        # Process complete query
        result = await client.process_query(query)
        
        print(f"Processing time: {result['processing_time']:.2f}s")
        print(f"Tasks generated: {len(result['tasks'])}")
        print(f"Confidence: {result['confidence']:.1%}\n")
        
        # Show first few tasks
        print("Sample tasks:")
        for i, task in enumerate(result['tasks'][:3], 1):
            print(f"{i}. [{task['priority_name']}] {task['title']}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure SCA API server is running: uvicorn web_integration:app")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "client-demo":
        # Run client demo
        asyncio.run(demo_client())
    
    elif FASTAPI_AVAILABLE:
        print("🚀 Starting SCA FastAPI Server")
        print("Run with: uvicorn web_integration:app --reload")
        print("API docs: http://localhost:8000/docs")
        print("\nOr run client demo: python web_integration.py client-demo")
        
        # Note: In production, use uvicorn to run the app
        # uvicorn web_integration:app --reload
        
    else:
        print("Install FastAPI and uvicorn to run the web server:")
        print("pip install fastapi uvicorn")
        print("\nThen run: uvicorn web_integration:app --reload")