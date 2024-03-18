import shutil
from pathlib import Path

from git import Repo

deactivated_git_path = ".git.deactivated"
active_git_path = ".git"


def disable_repository(repo_path):
    """
    Disable a Git repository by renaming the hidden .git/ directory.
    """
    git_path = repo_path / active_git_path
    deactivated_git_path = repo_path / deactivated_git_path
    git_path.rename(deactivated_git_path)


def enable_repository(repo_path):
    """
    Enable a previously disabled Git repository by renaming the .git.deactivated/ directory back to .git/.
    """
    deactivated_git_path = repo_path / deactivated_git_path
    git_path = repo_path / active_git_path
    deactivated_git_path.rename(git_path)


def refresh_repo():
    """
    Function to refresh the repository.
    """
    # Perform necessary actions to pull changes, etc.
    ...


class GitRepoContextManager:
    """
    Context manager for Git repository activation and deactivation.
    """

    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)

    def __enter__(self):
        enable_repository(self.repo_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        disable_repository(self.repo_path)


# Example usage:
repo_path = "path/to/repository"

# Disable the repository and perform operations
with GitRepoContextManager(repo_path):
    refresh_repo()

# Repository is automatically re-enabled outside the context manager
refresh_repo()
