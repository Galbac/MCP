from pathlib import Path


class UnsafePathError(ValueError):
    pass


class FileService:
    def __init__(self, allowed_root: Path) -> None:
        self.allowed_root = allowed_root.resolve()

    def _resolve_safe_path(self, relative_path: str) -> Path:
        candidate = (self.allowed_root / relative_path).resolve()

        if candidate != self.allowed_root and self.allowed_root not in candidate.parents:
            raise UnsafePathError("Path escapes allowed root")

        return candidate

    def list_files(self, subdir: str = ".") -> list[str]:
        target = self._resolve_safe_path(relative_path=subdir)

        if not target.exists():
            raise FileNotFoundError(f"Directory not found: {subdir}")
        if not target.is_dir():
            raise NotADirectoryError(f"Not a directory: {subdir}")

        return sorted(
            [
                item.relative_to(self.allowed_root).as_posix()
                for item in target.iterdir()
            ]
        )

    def read_text_file(self, relative_path: str, encoding: str = "utf-8") -> str:
        target = self._resolve_safe_path(relative_path)

        if not target.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        if not target.is_file():
            raise IsADirectoryError(f"Expected file, got directory: {relative_path}")

        return target.read_text(encoding=encoding)