from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["GitRepoController"]


@dataclass
class GitRepoController:
    repo_path: Path
    fresh: bool = False  # Won't be deactivated at init
    _deactivated_git: str = field(default=".git.deactivated", init=False)
    _activated_git: str = field(default=".git", init=False)

    @property
    def activated_path(self) -> Path:
        return self.repo_path / self._activated_git

    @property
    def deactivated_path(self) -> Path:
        return self.repo_path / self._deactivated_git

    def disable(self):
        """
        Disable the Git repository by renaming the hidden ".git/" directory to
        ".git.deactivated".
        """
        self.activated_path.rename(self.deactivated_path)
        assert self.deactivated_path.exists(), "Failed to deactivate"

    def enable(self):
        """
        Enable a previously disabled Git repository by renaming the ".git.deactivated/"
        directory back to ".git/".
        """
        assert self.repo_path.exists(), f"Repo path {self.repo_path} does not exist"
        if not self.fresh:
            self.deactivated_path.rename(self.activated_path)
        assert self.activated_path.exists(), "Failed to activate"

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()
