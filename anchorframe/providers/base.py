from abc import ABC, abstractmethod

class BackendProvider(ABC):
    """
    Abstract interface for ComfyUI backends (Local vs Cloud).
    """
    @abstractmethod
    def queue_prompt(self, workflow: dict) -> str:
        pass
        
    @abstractmethod
    def is_reachable(self) -> bool:
        pass
