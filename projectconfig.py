class ProjectConfig:
    @property
    def version_tag(self) -> str:
        return "v" + self.version

    def __init__(self, name: str="project", version: str = "0.0.0", description: str=""):
        self.name = name
        self.version = version
        self.description = description


PROJECT = ProjectConfig()

PROJECT.name = "dratini"
PROJECT.version = "0.0.0"
PROJECT.brief = "Dratini AOT Compiler"
PROJECT.description = ''''''
PROJECT.copyright = "Copyright (c) 2025 bonusbyte.org"
