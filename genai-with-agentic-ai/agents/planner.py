"""
planner.py
Simple planner that decomposes high-level goals into tasks and enqueues them.
"""
import logging
from typing import List, Dict
from scraper.sources import NEWS_SOURCES
from agents import task_queue

logger = logging.getLogger(__name__)


def create_plan(goal: str) -> Dict:
    """Create a simple plan for news collection based on a goal string.
    For now, supports goals like 'collect latest news' or 'collect technology news'.
    Returns a plan dict with tasks.
    """
    goal_lower = goal.lower() if goal else "collect latest news"
    # Determine target category
    target_category = None
    for cat in NEWS_SOURCES.keys():
        if cat.lower() in goal_lower:
            target_category = cat
            break

    tasks = []
    # If a category is specified, plan to collect only that category
    if target_category:
        sources = NEWS_SOURCES.get(target_category, [])
        for src in sources:
            tasks.append({
                "type": "collect_source",
                "payload": {"source": src, "category": target_category, "max_articles": 3},
                "priority": 50,
            })
    else:
        # plan across all categories
        for category, sources in NEWS_SOURCES.items():
            for src in sources[:3]:
                tasks.append({
                    "type": "collect_source",
                    "payload": {"source": src, "category": category, "max_articles": 3},
                    "priority": 50,
                })

    plan = {"goal": goal, "tasks": tasks, "created_by": "planner"}

    # Enqueue tasks
    enqueue_results = []
    for task in tasks:
        res = task_queue.enqueue_task(task["type"], task["payload"], priority=task.get("priority", 50))
        enqueue_results.append(res)

    plan["enqueue_results"] = enqueue_results
    logger.info(f"Planner created {len(tasks)} tasks for goal='{goal}'")
    return plan
