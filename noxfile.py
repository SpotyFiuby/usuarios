"""Entrypoint for nox."""

import nox


@nox.session(reuse_venv=True)
def tests(session):
    """Run all tests."""
    session.install("poetry")
    session.run("poetry", "install", "-E", "testing")

    cmd = ["poetry", "run", "pytest"]

    if session.posargs:
        cmd.extend(session.posargs)

    session.run(*cmd)


@nox.session(reuse_venv=True)
def cop(session):
    """Run all pre-commit hooks."""
    session.install("poetry")
    session.run("poetry", "install")

    session.run("poetry", "run", "pre-commit", "install")
    session.run(
        "poetry", "run", "pre-commit", "run", "--show-diff-on-failure", "--all-files"
    )


@nox.session(reuse_venv=True)
def bandit(session):
    """Run all pre-commit hooks."""
    session.install("poetry")
    session.run("poetry", "install")

    session.run(
        "poetry",
        "run",
        "bandit",
        "-r",
        "taller-2-spotifiuba/",
        "-ll",
        "-c",
        "bandit.yaml",
    )
