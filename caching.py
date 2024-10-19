import pickle
from pathlib import Path
from typing import Callable


class Cache[T]:
    def __init__(self, cache_dir: Path | str):
        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)
        if not cache_dir.exists():
            cache_dir.mkdir()
        if not cache_dir.is_dir():
            raise ValueError(f"{cache_dir} is not a valid directory")

        self.mem_cache: dict[str, T] = {}
        self.cache_dir = cache_dir

    def cached(self, key: str, elem: Callable[[], T]) -> T:
        path = self.cache_dir / key

        if path in self.mem_cache:
            return self.mem_cache[key]
        if path.exists():
            out = self.read(path)
        else:
            out = elem()
            self.write(path, out)
        self.mem_cache[key] = out
        return out

    @staticmethod
    def read(path: Path) -> T:
        with open(path, "rb") as fp:
            return pickle.load(fp)

    @staticmethod
    def write(path: Path, elem: T):
        with open(path, "wb") as fp:
            return pickle.dump(elem, fp)
