from git import Repo

from ..path_utils import aws_oa_dir
from .repo_suspender import GitRepoController

__all__ = ["clone_repository", "pull_changes"]


def clone_repository():
    """
    GitPython equivalent for:

    ```sh
    git clone -n --depth=1 --filter=tree:0
    git@github.com:APIs-guru/openapi-directory.git
    cd openapi-directory
    git sparse-checkout set --no-cone APIs/amazonaws.com
    git checkout
    ```
    """
    repo_url = "git@github.com:APIs-guru/openapi-directory.git"
    sparse_pattern = "APIs/amazonaws.com"
    repo = Repo.clone_from(
        url=repo_url,
        to_path=aws_oa_dir,
        no_checkout=True,
        depth=1,
        filter="tree:0",
    )
    with GitRepoController(repo_path=aws_oa_dir, fresh=True):
        repo.git.sparse_checkout("set", "--no-cone", sparse_pattern)
        repo.git.checkout()


def pull_changes():
    """
    GitPython equivalent for:

    ```sh
    cd openapi-directory
    git pull --depth=1
    ```
    """
    with GitRepoController(repo_path=aws_oa_dir):
        repo = Repo(aws_oa_dir)
        repo.git.pull(depth=1)
