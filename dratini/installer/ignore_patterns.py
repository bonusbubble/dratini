import fnmatch


def installer_ignore_patterns(path: str, names: list[str]):
    """Function that can be used as copytree() ignore parameter.

    Patterns is a sequence of glob-style patterns
    that are used to exclude files"""
    ignored_names = [
            ".git",
            ".vscode",
            "build",
            "examples",
            "scripts",
            ".gitattributes",
            ".gitignore"
    ]
    if path.endswith("assets"):
        ignored_names.append("icons")
    # for name in names:
    ignored_names.extend(fnmatch.filter(names, "*.ico"))
    ignored_names.extend(fnmatch.filter(names, "*.spec"))
    return set(ignored_names)
