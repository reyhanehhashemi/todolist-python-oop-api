"""
ID Generator for entities.

This module provides a simple counter-based ID generator
for projects and tasks.
"""

from typing import Dict


class IDGenerator:
    """
    Singleton ID generator for creating sequential integer IDs.

    Maintains separate counters for different entity types.
    """

    _instance = None
    _counters: Dict[str, int] = {}

    def __new__(cls):
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._counters = {}
        return cls._instance

    def generate(self, entity_type: str) -> int:
        """
        Generate next ID for given entity type.

        Args:
            entity_type: Type of entity (e.g., 'project', 'task')

        Returns:
            Next sequential integer ID
        """
        if entity_type not in self._counters:
            self._counters[entity_type] = 0

        self._counters[entity_type] += 1
        return self._counters[entity_type]

    def reset(self, entity_type: str = None) -> None:
        """
        Reset counter(s) for testing purposes.

        Args:
            entity_type: Specific entity type to reset, or None for all
        """
        if entity_type is None:
            self._counters.clear()
        elif entity_type in self._counters:
            self._counters[entity_type] = 0

    def get_current(self, entity_type: str) -> int:
        """
        Get current counter value without incrementing.

        Args:
            entity_type: Type of entity

        Returns:
            Current counter value (0 if not initialized)
        """
        return self._counters.get(entity_type, 0)


# Global singleton instance
id_generator = IDGenerator()
