"""Docstring generator utility module."""

import ast
import inspect
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class DocstringTemplate:
    """Docstring template for various Python objects."""

    summary: str
    description: Optional[str] = None
    args: List[Tuple[str, str, str]] = None  # (name, type, description)
    returns: Optional[Tuple[str, str]] = None  # (type, description)
    raises: List[Tuple[str, str]] = None  # (exception, description)

    def generate(self) -> str:
        """Generate formatted docstring.

        Returns:
            str: Formatted docstring following Google style
        """
        lines = [self.summary]

        if self.description:
            lines.extend(["", self.description])

        if self.args:
            lines.append("")
            lines.append("Args:")
            for name, type_, desc in self.args:
                lines.append(f"    {name} ({type_}): {desc}")

        if self.returns:
            lines.append("")
            lines.append("Returns:")
            lines.append(f"    {self.returns[0]}: {self.returns[1]}")

        if self.raises:
            lines.append("")
            lines.append("Raises:")
            for exc, desc in self.raises:
                lines.append(f"    {exc}: {desc}")

        return "\n".join(lines)


class DocstringGenerator:
    """Utility class for generating docstrings."""

    def __init__(self) -> None:
        """Initialize the docstring generator."""
        self.ast_parser = ast.parse

    def analyze_function(self, func: Any) -> DocstringTemplate:
        """Analyze a function and create a docstring template.

        Args:
            func: Function to analyze

        Returns:
            DocstringTemplate: Template containing function information

        Raises:
            ValueError: If the input is not a valid function
        """
        if not inspect.isfunction(func):
            raise ValueError("Input must be a function")

        sig = inspect.signature(func)
        args = []

        for name, param in sig.parameters.items():
            param_type = (
                param.annotation.__name__
                if param.annotation != inspect.Parameter.empty
                else "Any"
            )
            args.append((name, param_type, f"Description for {name}"))

        return_type = (
            sig.return_annotation.__name__
            if sig.return_annotation != inspect.Parameter.empty
            else "None"
        )

        return DocstringTemplate(
            summary=f"Generated docstring for {func.__name__}",
            args=args,
            returns=(return_type, "Description of return value"),
        )

    def analyze_class(self, cls: Any) -> DocstringTemplate:
        """Analyze a class and create a docstring template.

        Args:
            cls: Class to analyze

        Returns:
            DocstringTemplate: Template containing class information

        Raises:
            ValueError: If the input is not a valid class
        """
        if not inspect.isclass(cls):
            raise ValueError("Input must be a class")

        return DocstringTemplate(
            summary=f"Generated docstring for {cls.__name__}",
            description=f"Class representing {cls.__name__}",
        )

    def apply_docstring(self, obj: Any, template: DocstringTemplate) -> None:
        """Apply generated docstring to an object.

        Args:
            obj: Object to apply docstring to
            template: Docstring template to apply

        Raises:
            ValueError: If the object is not valid for docstring application
        """
        if not (inspect.isfunction(obj) or inspect.isclass(obj)):
            raise ValueError("Object must be a function or class")

        obj.__doc__ = template.generate()
