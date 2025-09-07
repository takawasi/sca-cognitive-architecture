#!/usr/bin/env python3
"""Task Decomposition Server Implementation

This module provides intelligent task decomposition functionality
for breaking down complex queries into actionable subtasks.
"""

import asyncio
import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging


class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    OPTIONAL = 1


@dataclass
class Task:
    """Represents a decomposed task"""
    id: str
    title: str
    description: str
    priority: Priority
    estimated_time: str
    dependencies: List[str]
    category: str
    complexity: int  # 1-5 scale
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "priority_name": self.priority.name,
            "estimated_time": self.estimated_time,
            "dependencies": self.dependencies,
            "category": self.category,
            "complexity": self.complexity
        }


class DecompositionServer:
    """Server for decomposing complex queries into actionable tasks"""
    
    def __init__(self):
        self.logger = logging.getLogger('SCA.Decomposition')
        
        # Task templates for different domains
        self.task_templates = {
            'software_development': {
                'setup': {
                    'tasks': ['Set up development environment', 'Initialize project structure', 'Configure version control'],
                    'time_estimates': ['30 min', '45 min', '15 min'],
                    'priorities': [Priority.HIGH, Priority.HIGH, Priority.MEDIUM]
                },
                'design': {
                    'tasks': ['Design system architecture', 'Create database schema', 'Design API endpoints'],
                    'time_estimates': ['2 hours', '1.5 hours', '1 hour'],
                    'priorities': [Priority.CRITICAL, Priority.HIGH, Priority.HIGH]
                },
                'implementation': {
                    'tasks': ['Implement core functionality', 'Create user interface', 'Add error handling'],
                    'time_estimates': ['4 hours', '3 hours', '1 hour'],
                    'priorities': [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM]
                },
                'testing': {
                    'tasks': ['Write unit tests', 'Implement integration tests', 'Perform user testing'],
                    'time_estimates': ['2 hours', '1.5 hours', '1 hour'],
                    'priorities': [Priority.HIGH, Priority.MEDIUM, Priority.MEDIUM]
                },
                'deployment': {
                    'tasks': ['Configure production environment', 'Set up CI/CD pipeline', 'Deploy application'],
                    'time_estimates': ['1.5 hours', '2 hours', '30 min'],
                    'priorities': [Priority.HIGH, Priority.MEDIUM, Priority.HIGH]
                }
            },
            'data_analysis': {
                'preparation': {
                    'tasks': ['Collect and validate data', 'Clean and preprocess data', 'Explore data structure'],
                    'time_estimates': ['2 hours', '3 hours', '1 hour'],
                    'priorities': [Priority.CRITICAL, Priority.CRITICAL, Priority.HIGH]
                },
                'analysis': {
                    'tasks': ['Perform statistical analysis', 'Create visualizations', 'Identify patterns'],
                    'time_estimates': ['2 hours', '1.5 hours', '2 hours'],
                    'priorities': [Priority.HIGH, Priority.HIGH, Priority.HIGH]
                },
                'reporting': {
                    'tasks': ['Generate analysis report', 'Create presentation slides', 'Document methodology'],
                    'time_estimates': ['2 hours', '1 hour', '1.5 hours'],
                    'priorities': [Priority.HIGH, Priority.MEDIUM, Priority.MEDIUM]
                }
            },
            'business_strategy': {
                'research': {
                    'tasks': ['Conduct market research', 'Analyze competitors', 'Identify target audience'],
                    'time_estimates': ['4 hours', '3 hours', '2 hours'],
                    'priorities': [Priority.HIGH, Priority.HIGH, Priority.HIGH]
                },
                'planning': {
                    'tasks': ['Define objectives', 'Create action plan', 'Set success metrics'],
                    'time_estimates': ['2 hours', '3 hours', '1 hour'],
                    'priorities': [Priority.CRITICAL, Priority.CRITICAL, Priority.HIGH]
                },
                'execution': {
                    'tasks': ['Implement strategies', 'Monitor progress', 'Adjust based on feedback'],
                    'time_estimates': ['ongoing', 'weekly', 'as needed'],
                    'priorities': [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM]
                }
            }
        }
        
        # Keywords that indicate different task categories
        self.category_keywords = {
            'setup': ['setup', 'install', 'configure', 'initialize', 'prepare'],
            'design': ['design', 'architect', 'plan', 'model', 'schema'],
            'implementation': ['build', 'create', 'implement', 'develop', 'code'],
            'testing': ['test', 'validate', 'verify', 'debug', 'qa'],
            'deployment': ['deploy', 'launch', 'release', 'publish', 'production'],
            'analysis': ['analyze', 'examine', 'study', 'evaluate', 'assess'],
            'research': ['research', 'investigate', 'explore', 'survey', 'study'],
            'documentation': ['document', 'write', 'explain', 'describe', 'record']
        }
    
    async def decompose_query(self, query: str, context: str, max_tasks: int = 20) -> List[Task]:
        """Decompose a query into actionable tasks"""
        self.logger.debug(f"Decomposing query: {query[:100]}...")
        
        try:
            # Identify domain and project type
            domain = self._identify_domain(query)
            project_phases = self._identify_project_phases(query, context)
            
            # Extract explicit tasks from query
            explicit_tasks = self._extract_explicit_tasks(query)
            
            # Generate template-based tasks
            template_tasks = self._generate_template_tasks(domain, project_phases, query)
            
            # Combine and prioritize tasks
            all_tasks = explicit_tasks + template_tasks
            prioritized_tasks = self._prioritize_tasks(all_tasks, query)
            
            # Add dependencies
            tasks_with_deps = self._add_dependencies(prioritized_tasks)
            
            # Limit to max_tasks and return
            return tasks_with_deps[:max_tasks]
            
        except Exception as e:
            self.logger.error(f"Failed to decompose query: {e}")
            return self._generate_fallback_tasks(query)
    
    def _identify_domain(self, query: str) -> str:
        """Identify the domain/field of the query"""
        query_lower = query.lower()
        
        # Domain indicators
        domain_indicators = {
            'software_development': [
                'app', 'application', 'software', 'code', 'programming', 'development',
                'api', 'database', 'web', 'mobile', 'system', 'platform', 'framework'
            ],
            'data_analysis': [
                'data', 'analysis', 'analytics', 'statistics', 'visualization', 'chart',
                'dataset', 'metrics', 'insights', 'pattern', 'trend', 'machine learning'
            ],
            'business_strategy': [
                'business', 'strategy', 'marketing', 'sales', 'customer', 'revenue',
                'growth', 'market', 'competitive', 'plan', 'objective', 'goal'
            ],
            'design': [
                'design', 'ui', 'ux', 'interface', 'user experience', 'prototype',
                'wireframe', 'mockup', 'branding', 'visual', 'layout'
            ],
            'research': [
                'research', 'study', 'investigation', 'survey', 'experiment',
                'hypothesis', 'methodology', 'findings', 'literature review'
            ]
        }
        
        domain_scores = {}
        for domain, keywords in domain_indicators.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return 'software_development'  # Default domain
    
    def _identify_project_phases(self, query: str, context: str) -> List[str]:
        """Identify which project phases are relevant"""
        combined_text = (query + " " + context).lower()
        relevant_phases = []
        
        phase_indicators = {
            'setup': ['start', 'begin', 'initial', 'first', 'setup', 'prepare'],
            'design': ['design', 'architect', 'plan', 'structure', 'model'],
            'implementation': ['build', 'create', 'implement', 'develop', 'make'],
            'testing': ['test', 'verify', 'validate', 'check', 'debug'],
            'deployment': ['deploy', 'launch', 'release', 'publish', 'go live'],
            'analysis': ['analyze', 'examine', 'evaluate', 'assess', 'measure'],
            'research': ['research', 'investigate', 'study', 'explore', 'learn'],
            'documentation': ['document', 'explain', 'describe', 'write', 'record']
        }
        
        for phase, indicators in phase_indicators.items():
            if any(indicator in combined_text for indicator in indicators):
                relevant_phases.append(phase)
        
        # If no specific phases identified, assume full project lifecycle
        if not relevant_phases:
            relevant_phases = ['setup', 'design', 'implementation', 'testing']
        
        return relevant_phases
    
    def _extract_explicit_tasks(self, query: str) -> List[Task]:
        """Extract tasks explicitly mentioned in the query"""
        tasks = []
        
        # Look for explicit task patterns
        task_patterns = [
            r'(?:need to|should|must|have to)\s+([^.]+)',
            r'(?:create|build|implement|develop|design)\s+([^.]+)',
            r'(?:add|include|incorporate)\s+([^.]+)',
            r'(?:setup|configure|install)\s+([^.]+)'
        ]
        
        task_id = 1
        for pattern in task_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                task_text = match.strip()
                if len(task_text) > 5:  # Avoid very short matches
                    tasks.append(Task(
                        id=f"explicit_{task_id}",
                        title=task_text.title(),
                        description=f"Explicit requirement: {task_text}",
                        priority=Priority.HIGH,
                        estimated_time=self._estimate_time(task_text),
                        dependencies=[],
                        category=self._categorize_task(task_text),
                        complexity=self._assess_complexity(task_text)
                    ))
                    task_id += 1
        
        return tasks
    
    def _generate_template_tasks(self, domain: str, phases: List[str], query: str) -> List[Task]:
        """Generate tasks based on domain templates"""
        tasks = []
        
        if domain not in self.task_templates:
            return tasks
        
        domain_templates = self.task_templates[domain]
        task_id = 1
        
        for phase in phases:
            if phase in domain_templates:
                phase_data = domain_templates[phase]
                task_list = phase_data['tasks']
                time_estimates = phase_data['time_estimates']
                priorities = phase_data['priorities']
                
                for i, (task_title, time_est, priority) in enumerate(zip(task_list, time_estimates, priorities)):
                    # Customize task based on query context
                    customized_title = self._customize_task_title(task_title, query)
                    
                    tasks.append(Task(
                        id=f"{domain}_{phase}_{task_id}",
                        title=customized_title,
                        description=f"{phase.title()} phase task: {customized_title}",
                        priority=priority,
                        estimated_time=time_est,
                        dependencies=[],
                        category=phase,
                        complexity=self._assess_task_complexity(phase, i)
                    ))
                    task_id += 1
        
        return tasks
    
    def _customize_task_title(self, template_title: str, query: str) -> str:
        """Customize generic task titles based on query context"""
        query_lower = query.lower()
        
        # Extract key terms from query
        key_terms = []
        
        # Look for technology/framework mentions
        tech_terms = ['react', 'angular', 'vue', 'node', 'python', 'java', 'javascript']
        for term in tech_terms:
            if term in query_lower:
                key_terms.append(term.title())
        
        # Look for application types
        app_types = ['dashboard', 'website', 'api', 'mobile app', 'web app', 'system']
        for app_type in app_types:
            if app_type in query_lower:
                key_terms.append(app_type)
        
        # Customize template with context
        customized = template_title
        if key_terms:
            context = " ".join(key_terms[:2])  # Use first 2 key terms
            customized = template_title.replace('system', context.lower())
            customized = customized.replace('application', context.lower())
            customized = customized.replace('project', f"{context} project".lower())
        
        return customized
    
    def _prioritize_tasks(self, tasks: List[Task], query: str) -> List[Task]:
        """Prioritize tasks based on query urgency and importance"""
        # Look for urgency indicators
        urgency_keywords = ['urgent', 'asap', 'immediately', 'quickly', 'fast', 'priority']
        query_lower = query.lower()
        
        is_urgent = any(keyword in query_lower for keyword in urgency_keywords)
        
        # Adjust priorities based on urgency
        if is_urgent:
            for task in tasks:
                if task.priority.value < Priority.HIGH.value:
                    # Boost priority for urgent requests
                    task.priority = Priority(min(task.priority.value + 1, Priority.CRITICAL.value))
        
        # Sort by priority (descending) then by complexity (ascending)
        return sorted(tasks, key=lambda t: (-t.priority.value, t.complexity))
    
    def _add_dependencies(self, tasks: List[Task]) -> List[Task]:
        """Add logical dependencies between tasks"""
        # Define dependency rules based on categories
        dependency_rules = {
            'setup': [],
            'design': ['setup'],
            'implementation': ['setup', 'design'],
            'testing': ['implementation'],
            'deployment': ['testing', 'implementation'],
            'analysis': ['preparation'],
            'research': [],
            'documentation': ['implementation', 'analysis']
        }
        
        # Build category to task ID mapping
        category_to_tasks = {}
        for task in tasks:
            if task.category not in category_to_tasks:
                category_to_tasks[task.category] = []
            category_to_tasks[task.category].append(task.id)
        
        # Add dependencies
        for task in tasks:
            if task.category in dependency_rules:
                required_categories = dependency_rules[task.category]
                for req_category in required_categories:
                    if req_category in category_to_tasks:
                        # Add first task from required category as dependency
                        task.dependencies.extend(category_to_tasks[req_category][:1])
        
        return tasks
    
    def _categorize_task(self, task_text: str) -> str:
        """Categorize a task based on its content"""
        task_lower = task_text.lower()
        
        for category, keywords in self.category_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                return category
        
        return 'implementation'  # Default category
    
    def _estimate_time(self, task_text: str) -> str:
        """Estimate time required for a task"""
        task_lower = task_text.lower()
        
        # Simple heuristics based on complexity indicators
        if any(word in task_lower for word in ['setup', 'install', 'configure']):
            return '30 min'
        elif any(word in task_lower for word in ['design', 'plan', 'architecture']):
            return '2 hours'
        elif any(word in task_lower for word in ['implement', 'build', 'develop']):
            return '4 hours'
        elif any(word in task_lower for word in ['test', 'debug', 'validate']):
            return '1.5 hours'
        else:
            return '2 hours'  # Default estimate
    
    def _assess_complexity(self, task_text: str) -> int:
        """Assess complexity of a task (1-5 scale)"""
        complexity_indicators = {
            'simple': ['setup', 'install', 'configure', 'add', 'update'],
            'moderate': ['create', 'build', 'implement', 'design'],
            'complex': ['integrate', 'optimize', 'architect', 'analyze'],
            'advanced': ['machine learning', 'ai', 'distributed', 'scalable']
        }
        
        task_lower = task_text.lower()
        
        if any(word in task_lower for word in complexity_indicators['advanced']):
            return 5
        elif any(word in task_lower for word in complexity_indicators['complex']):
            return 4
        elif any(word in task_lower for word in complexity_indicators['moderate']):
            return 3
        elif any(word in task_lower for word in complexity_indicators['simple']):
            return 2
        else:
            return 3  # Default complexity
    
    def _assess_task_complexity(self, phase: str, task_index: int) -> int:
        """Assess complexity based on phase and task order"""
        phase_complexity = {
            'setup': 2,
            'design': 4,
            'implementation': 5,
            'testing': 3,
            'deployment': 3,
            'analysis': 4,
            'research': 3,
            'documentation': 2
        }
        
        base_complexity = phase_complexity.get(phase, 3)
        # First tasks in a phase are usually simpler
        if task_index == 0:
            base_complexity = max(1, base_complexity - 1)
        
        return base_complexity
    
    def _generate_fallback_tasks(self, query: str) -> List[Task]:
        """Generate basic fallback tasks when decomposition fails"""
        return [
            Task(
                id="fallback_1",
                title="Analyze Requirements",
                description=f"Analyze and understand the requirements for: {query}",
                priority=Priority.HIGH,
                estimated_time="1 hour",
                dependencies=[],
                category="analysis",
                complexity=3
            ),
            Task(
                id="fallback_2",
                title="Plan Implementation", 
                description="Create detailed implementation plan",
                priority=Priority.HIGH,
                estimated_time="2 hours",
                dependencies=["fallback_1"],
                category="design",
                complexity=4
            ),
            Task(
                id="fallback_3",
                title="Execute Plan",
                description="Implement the planned solution",
                priority=Priority.CRITICAL,
                estimated_time="4 hours",
                dependencies=["fallback_2"],
                category="implementation",
                complexity=4
            )
        ]


# MCP Server entry point
if __name__ == "__main__":
    import sys
    
    async def main():
        server = DecompositionServer()
        
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            tasks = await server.decompose_query(query, "")
            
            print(f"\nTask Decomposition for: {query}\n")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title}")
                print(f"   Priority: {task.priority.name}")
                print(f"   Time: {task.estimated_time}")
                print(f"   Category: {task.category}")
                if task.dependencies:
                    print(f"   Dependencies: {', '.join(task.dependencies)}")
                print()
        else:
            print("SCA Task Decomposition Server")
            print("Usage: python decomposition.py <query>")
    
    asyncio.run(main())