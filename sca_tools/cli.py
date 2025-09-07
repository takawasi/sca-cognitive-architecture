#!/usr/bin/env python3
"""SCA Command Line Interface

This module provides a command-line interface for the SCA framework.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

from .core import SCAFramework, process_query_sync
from .context_mapper import ContextMapperServer
from .decomposition import DecompositionServer
from .synthesis import SynthesisServer
from .memory import MemoryServer


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser"""
    parser = argparse.ArgumentParser(
        description="SCA - Symbiotic Cognitive Architecture Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a query through the full SCA pipeline
  sca "Build a React dashboard with user analytics"
  
  # Use specific components
  sca context "Design a microservices architecture"
  sca decompose "Implement user authentication system"
  sca synthesize "Use React" "Use Vue" "Use Angular"
  
  # Memory operations
  sca memory search "authentication"
  sca memory stats
  
  # Configuration
  sca config --show
  sca config --validate
"""
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="SCA Framework 1.0.0"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "text", "yaml"],
        default="text",
        help="Output format (default: text)"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )
    
    # Main process command (default)
    process_parser = subparsers.add_parser(
        "process",
        help="Process a query through the full SCA pipeline"
    )
    process_parser.add_argument(
        "query",
        help="Query to process"
    )
    process_parser.add_argument(
        "--context",
        help="Additional context for the query"
    )
    
    # Context mapping command
    context_parser = subparsers.add_parser(
        "context",
        help="Create context map for a query"
    )
    context_parser.add_argument(
        "query",
        help="Query to map"
    )
    
    # Task decomposition command
    decompose_parser = subparsers.add_parser(
        "decompose",
        help="Decompose query into tasks"
    )
    decompose_parser.add_argument(
        "query",
        help="Query to decompose"
    )
    decompose_parser.add_argument(
        "--context",
        default="",
        help="Context for decomposition"
    )
    decompose_parser.add_argument(
        "--max-tasks",
        type=int,
        default=20,
        help="Maximum number of tasks to generate"
    )
    
    # Synthesis command
    synthesize_parser = subparsers.add_parser(
        "synthesize",
        help="Synthesize multiple perspectives"
    )
    synthesize_parser.add_argument(
        "perspectives",
        nargs="+",
        help="Perspectives to synthesize"
    )
    
    # Memory commands
    memory_parser = subparsers.add_parser(
        "memory",
        help="Memory operations"
    )
    memory_subparsers = memory_parser.add_subparsers(
        dest="memory_command",
        help="Memory operations"
    )
    
    # Memory search
    search_parser = memory_subparsers.add_parser(
        "search",
        help="Search memory"
    )
    search_parser.add_argument(
        "query",
        help="Search query"
    )
    search_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum results"
    )
    
    # Memory stats
    memory_subparsers.add_parser(
        "stats",
        help="Show memory statistics"
    )
    
    # Memory insights
    insights_parser = memory_subparsers.add_parser(
        "insights",
        help="Show recent insights"
    )
    insights_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of insights"
    )
    
    # Config commands
    config_parser = subparsers.add_parser(
        "config",
        help="Configuration operations"
    )
    config_parser.add_argument(
        "--show",
        action="store_true",
        help="Show current configuration"
    )
    config_parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration"
    )
    
    # Demo command
    demo_parser = subparsers.add_parser(
        "demo",
        help="Run SCA demo"
    )
    demo_parser.add_argument(
        "--example",
        choices=["web-app", "data-analysis", "api-design"],
        default="web-app",
        help="Demo example to run"
    )
    
    return parser


async def cmd_process(args) -> dict:
    """Process command"""
    result = process_query_sync(args.query, args.context, args.config)
    return result.to_dict()


async def cmd_context(args) -> dict:
    """Context mapping command"""
    server = ContextMapperServer()
    result = await server.create_context_map(args.query)
    return {"query": args.query, "context_map": result}


async def cmd_decompose(args) -> dict:
    """Decomposition command"""
    server = DecompositionServer()
    tasks = await server.decompose_query(args.query, args.context, args.max_tasks)
    return {
        "query": args.query,
        "context": args.context,
        "tasks": [task.to_dict() for task in tasks]
    }


async def cmd_synthesize(args) -> dict:
    """Synthesis command"""
    server = SynthesisServer()
    result = await server.synthesize_perspectives(args.perspectives)
    return {
        "perspectives": args.perspectives,
        "synthesis": result
    }


async def cmd_memory(args) -> dict:
    """Memory commands"""
    server = MemoryServer()
    
    if args.memory_command == "search":
        results = await server.search_memory(args.query, args.limit)
        return {"query": args.query, "results": results}
    
    elif args.memory_command == "stats":
        stats = await server.get_memory_stats()
        return {"stats": stats}
    
    elif args.memory_command == "insights":
        insights = await server.get_recent_insights(args.limit)
        return {"insights": insights}
    
    return {"error": "Unknown memory command"}


def cmd_config(args) -> dict:
    """Configuration commands"""
    if args.show:
        config_path = args.config or "config/sca_config.json"
        if Path(config_path).exists():
            with open(config_path) as f:
                config = json.load(f)
            return {"config_path": config_path, "config": config}
        else:
            return {"error": f"Configuration file not found: {config_path}"}
    
    elif args.validate:
        config_path = args.config or "config/sca_config.json"
        try:
            framework = SCAFramework(config_path)
            return {
                "valid": True, 
                "config_path": config_path,
                "stats": framework.get_stats()
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    return {"error": "No config command specified"}


async def cmd_demo(args) -> dict:
    """Demo command"""
    examples = {
        "web-app": "Build a React dashboard with real-time user analytics and authentication",
        "data-analysis": "Analyze customer churn patterns in our SaaS product using machine learning",
        "api-design": "Design a RESTful API for a multi-tenant e-commerce platform"
    }
    
    query = examples[args.example]
    print(f"\n🚀 SCA Demo: {args.example}")
    print(f"Query: {query}\n")
    
    result = process_query_sync(query, None, args.config)
    
    return {
        "demo_type": args.example,
        "query": query,
        "result": result.to_dict()
    }


def format_output(data: dict, format_type: str, verbose: bool = False) -> str:
    """Format output based on format type"""
    if format_type == "json":
        return json.dumps(data, indent=2)
    
    elif format_type == "yaml":
        try:
            import yaml
            return yaml.dump(data, default_flow_style=False)
        except ImportError:
            return json.dumps(data, indent=2)
    
    else:  # text format
        return format_text_output(data, verbose)


def format_text_output(data: dict, verbose: bool = False) -> str:
    """Format data as human-readable text"""
    output = []
    
    # Handle different result types
    if "context_map" in data:
        output.append("📊 Context Map:")
        output.append(data["context_map"])
    
    if "tasks" in data:
        output.append(f"\n📋 Tasks ({len(data['tasks'])}):")
        for i, task in enumerate(data["tasks"], 1):
            priority = task.get("priority_name", task.get("priority", "N/A"))
            output.append(f"{i:2d}. [{priority}] {task['title']}")
            if verbose:
                output.append(f"    Time: {task.get('estimated_time', 'N/A')}")
                output.append(f"    Category: {task.get('category', 'N/A')}")
                if task.get('dependencies'):
                    output.append(f"    Dependencies: {', '.join(task['dependencies'])}")
    
    if "synthesis" in data:
        output.append("\n🔄 Synthesis Results:")
        synthesis = data["synthesis"]
        
        for approach_name, approach_data in synthesis.items():
            if approach_name == "meta_analysis":
                continue
                
            if isinstance(approach_data, dict):
                confidence = approach_data.get("confidence", 0)
                output.append(f"\n{approach_name.replace('_', ' ').title()}:")
                output.append(f"  Confidence: {confidence:.1%}")
                output.append(f"  Description: {approach_data.get('description', 'N/A')}")
                
                if verbose:
                    pros = approach_data.get("pros", [])
                    cons = approach_data.get("cons", [])
                    if pros:
                        output.append("  Pros: " + ", ".join(pros[:2]))
                    if cons:
                        output.append("  Cons: " + ", ".join(cons[:2]))
        
        # Add meta analysis
        if "meta_analysis" in synthesis:
            meta = synthesis["meta_analysis"]
            output.append(f"\nRecommended: {meta.get('recommended_approach', 'N/A').replace('_', ' ').title()}")
    
    if "results" in data:  # Memory search results
        output.append(f"\n🔍 Search Results ({len(data['results'])}):")
        for result in data["results"][:5]:  # Limit to first 5
            importance = result.get("importance", 0)
            content = result.get("content", "")[:100]
            output.append(f"  [{importance}] {content}...")
    
    if "insights" in data:
        output.append(f"\n💡 Recent Insights ({len(data['insights'])}):")
        for insight in data["insights"]:
            importance = insight.get("importance", 0)
            content = insight.get("content", "")[:80]
            output.append(f"  [{importance}] {content}...")
    
    if "stats" in data:
        stats = data["stats"]
        output.append("\n📈 Memory Statistics:")
        output.append(f"  Total entries: {stats.get('total_entries', 0)}")
        output.append(f"  Size: {stats.get('total_size_mb', 0)} MB")
        output.append(f"  Categories: {', '.join(stats.get('categories', {}).keys())}")
    
    if "config" in data:
        config = data["config"]
        output.append("\n⚙️  Configuration:")
        if "framework" in config:
            fw = config["framework"]
            output.append(f"  Name: {fw.get('name', 'N/A')}")
            output.append(f"  Version: {fw.get('version', 'N/A')}")
    
    return "\n".join(output)


async def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle no command (default to process if query given as first arg)
    if not args.command and len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Treat first non-option argument as a query to process
        args.command = "process"
        args.query = sys.argv[1]
        args.context = None
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Route to appropriate command handler
        if args.command == "process":
            result = await cmd_process(args)
        elif args.command == "context":
            result = await cmd_context(args)
        elif args.command == "decompose":
            result = await cmd_decompose(args)
        elif args.command == "synthesize":
            result = await cmd_synthesize(args)
        elif args.command == "memory":
            result = await cmd_memory(args)
        elif args.command == "config":
            result = cmd_config(args)
        elif args.command == "demo":
            result = await cmd_demo(args)
        else:
            result = {"error": f"Unknown command: {args.command}"}
        
        # Format and print output
        output = format_output(result, args.format, args.verbose)
        print(output)
        
    except Exception as e:
        error_result = {"error": str(e), "command": args.command}
        if args.verbose:
            import traceback
            error_result["traceback"] = traceback.format_exc()
        
        output = format_output(error_result, args.format)
        print(output, file=sys.stderr)
        sys.exit(1)


def cli_main():
    """Synchronous entry point for console scripts"""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()