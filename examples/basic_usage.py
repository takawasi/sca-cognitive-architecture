#!/usr/bin/env python3
"""Basic SCA Framework Usage Examples

This script demonstrates how to use the SCA framework for various tasks.
"""

import asyncio
import json
from sca_tools import SCAFramework, process_query_sync
from sca_tools.context_mapper import ContextMapperServer
from sca_tools.decomposition import DecompositionServer
from sca_tools.synthesis import SynthesisServer


async def example_1_complete_workflow():
    """Example 1: Complete SCA workflow"""
    print("🚀 Example 1: Complete SCA Workflow")
    print("=" * 50)
    
    # Initialize the SCA framework
    sca = SCAFramework()
    
    # Process a complex query
    query = "Build a real-time chat application with user authentication and message persistence"
    print(f"Query: {query}\n")
    
    result = await sca.process(query)
    
    print(f"Processing time: {result.processing_time:.2f} seconds")
    print(f"Confidence: {result.confidence:.1%}\n")
    
    # Display context map
    print("📊 Context Map:")
    print(result.context_map)
    print()
    
    # Display tasks
    print(f"📋 Tasks ({len(result.tasks)}):")
    for i, task in enumerate(result.tasks[:5], 1):  # Show first 5 tasks
        print(f"{i:2d}. [{task['priority_name']}] {task['title']}")
        print(f"    Time: {task['estimated_time']}, Category: {task['category']}")
    
    if len(result.tasks) > 5:
        print(f"    ... and {len(result.tasks) - 5} more tasks")
    print()
    
    # Display synthesis results
    print("🔄 Synthesis Results:")
    for approach_name, approach_data in result.synthesis.items():
        if approach_name != "meta_analysis" and isinstance(approach_data, dict):
            confidence = approach_data.get("confidence", 0)
            description = approach_data.get("description", "N/A")
            print(f"  {approach_name.replace('_', ' ').title()}: {confidence:.1%}")
            print(f"    {description}")
    
    recommended = result.synthesis.get("meta_analysis", {}).get("recommended_approach", "N/A")
    print(f"\n✅ Recommended: {recommended.replace('_', ' ').title()}")


async def example_2_individual_components():
    """Example 2: Using individual SCA components"""
    print("\n\n🔧 Example 2: Individual Components")
    print("=" * 50)
    
    query = "Design a microservices architecture for e-commerce"
    print(f"Query: {query}\n")
    
    # 1. Context Mapping
    print("📊 Step 1: Context Mapping")
    context_mapper = ContextMapperServer()
    context_map = await context_mapper.create_context_map(query)
    print("Context map created (Mermaid diagram)")
    print(context_map[:200] + "..." if len(context_map) > 200 else context_map)
    print()
    
    # 2. Task Decomposition
    print("📋 Step 2: Task Decomposition")
    decomposer = DecompositionServer()
    tasks = await decomposer.decompose_query(query, context_map, max_tasks=8)
    
    for i, task in enumerate(tasks, 1):
        print(f"{i:2d}. [{task.priority.name}] {task.title}")
        print(f"    Time: {task.estimated_time}, Complexity: {task.complexity}/5")
    print()
    
    # 3. Perspective Synthesis
    print("🔄 Step 3: Perspective Synthesis")
    synthesizer = SynthesisServer()
    
    perspectives = [
        "Use Docker containers for each microservice",
        "Implement API Gateway for request routing",
        "Use event-driven architecture with message queues",
        "Deploy on Kubernetes for orchestration"
    ]
    
    synthesis_result = await synthesizer.synthesize_perspectives(perspectives)
    
    for approach_name, approach_data in synthesis_result.items():
        if approach_name != "meta_analysis" and isinstance(approach_data, dict):
            confidence = approach_data.get("confidence", 0)
            description = approach_data.get("description", "N/A")
            print(f"  {approach_name.replace('_', ' ').title()}: {confidence:.1%}")
            print(f"    {description[:100]}...")


def example_3_synchronous_usage():
    """Example 3: Synchronous usage (easier for simple scripts)"""
    print("\n\n🔄 Example 3: Synchronous Usage")
    print("=" * 50)
    
    queries = [
        "Create a Python web scraper for product prices",
        "Set up automated testing for a React application",
        "Design a database schema for a blogging platform"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 40)
        
        # Use synchronous wrapper
        result = process_query_sync(query)
        
        print(f"Processing time: {result.processing_time:.2f}s")
        print(f"Tasks generated: {len(result.tasks)}")
        print(f"Confidence: {result.confidence:.1%}")
        
        # Show top 3 tasks
        print("Top tasks:")
        for j, task in enumerate(result.tasks[:3], 1):
            print(f"  {j}. {task['title']} ({task['estimated_time']})")


async def example_4_memory_usage():
    """Example 4: Memory system usage"""
    print("\n\n🧠 Example 4: Memory System")
    print("=" * 50)
    
    sca = SCAFramework()
    
    # Record some interactions
    print("Recording interactions in memory...")
    
    interactions = [
        ("Built a React dashboard with authentication", 4),
        ("Implemented JWT token validation in Node.js", 3), 
        ("Created responsive CSS layout using Grid and Flexbox", 3),
        ("Set up PostgreSQL database with proper indexing", 4),
        ("Deployed application using Docker and nginx", 3)
    ]
    
    for content, importance in interactions:
        await sca.memory.record_interaction(content, importance)
    
    # Search memory
    print("\nSearching memory for 'authentication'...")
    results = await sca.search_memory("authentication", limit=3)
    
    for result in results:
        print(f"  [{result['importance']}] {result['content'][:80]}...")
        print(f"      Relevance: {result.get('relevance_score', 0):.2f}")
    
    # Get insights
    print("\nRecent insights:")
    insights = await sca.memory.get_recent_insights(3)
    
    for insight in insights:
        print(f"  [{insight['importance']}] {insight['content'][:80]}...")
    
    # Memory stats
    stats = await sca.memory.get_memory_stats()
    print(f"\nMemory stats: {stats['total_entries']} entries, {stats['total_size_mb']} MB")


async def example_5_custom_configuration():
    """Example 5: Custom configuration"""
    print("\n\n⚙️  Example 5: Custom Configuration")
    print("=" * 50)
    
    # Create custom config
    custom_config = {
        "max_context_size": 1000,
        "max_tasks": 10,
        "memory_enabled": True,
        "synthesis_approaches": 3
    }
    
    # You could save this to a file and load it
    # For demo, we'll pass it directly (not implemented in current version)
    sca = SCAFramework()  # Would use: SCAFramework(custom_config)
    
    query = "Optimize database queries for better performance"
    result = await sca.process(query)
    
    print(f"Query: {query}")
    print(f"Tasks generated: {len(result.tasks)} (limited by config)")
    print(f"Framework stats: {json.dumps(sca.get_stats(), indent=2)}")


async def main():
    """Run all examples"""
    print("🎆 SCA Framework Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use the SCA framework.\n")
    
    try:
        await example_1_complete_workflow()
        await example_2_individual_components()
        example_3_synchronous_usage()
        await example_4_memory_usage()
        await example_5_custom_configuration()
        
        print("\n\n✨ All examples completed successfully!")
        print("\nNext steps:")
        print("- Try the CLI: `sca \"your query here\"`")
        print("- Explore the API documentation")
        print("- Build your own SCA-powered applications")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())