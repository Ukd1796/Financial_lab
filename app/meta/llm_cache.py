# app/meta/llm_cache.py
#
# Disk-backed cache for LLM prompt → response_text.
#
# Why: gpt-4o with temperature=0.0 + seed=0 is best-effort determinism but
# OpenAI does not guarantee identical outputs across calls (backend path
# variation, moving model alias). A tiny weight shift cascades into different
# fills, trades, and PnL — making A/B comparisons of NON-prompt changes
# (clamp, gate, sizing, exits) impossible. The cache freezes the LLM stream
# so every non-prompt iteration is reproducible.
#
# Cache key = SHA-256(model + "\x00" + prompt). Storage: a single JSON file
# (default runs/llm_cache.json). Atomic writes via tmp+rename. The file is
# safe to commit to git so teammates / future-you reproduce backtests exactly.
#
# Env:
#   LLM_CACHE_ENABLED   "0" disables the cache (every call hits the API).
#                       Default: "1" (enabled).
#   LLM_CACHE_PATH      Path to cache file. Default: "runs/llm_cache.json".

import atexit
import hashlib
import json
import os
from pathlib import Path
from typing import Callable


class LLMResponseCache:

    def __init__(self, path: str | None = None):
        self.enabled = os.environ.get("LLM_CACHE_ENABLED", "1") != "0"
        self.path = Path(path or os.environ.get("LLM_CACHE_PATH", "runs/llm_cache.json"))
        self.store: dict[str, str] = {}
        self.hits = 0
        self.misses = 0
        self._summary_printed = False
        if self.enabled and self.path.exists():
            try:
                with open(self.path) as f:
                    self.store = json.load(f)
            except Exception as e:
                print(f"  [LLMCache] WARN: failed to load {self.path}: {e}")
                self.store = {}

    @staticmethod
    def make_key(prompt: str, model: str) -> str:
        h = hashlib.sha256()
        h.update(model.encode("utf-8"))
        h.update(b"\x00")
        h.update(prompt.encode("utf-8"))
        return h.hexdigest()

    def get_or_call(self, prompt: str, model: str, call_fn: Callable[[], str]) -> str:
        """Return cached response text, or call `call_fn()` and cache the result."""
        if not self.enabled:
            return call_fn()
        key = self.make_key(prompt, model)
        if key in self.store:
            self.hits += 1
            return self.store[key]
        text = call_fn()
        self.store[key] = text
        self.misses += 1
        self._flush()
        return text

    def _flush(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(self.path.suffix + ".tmp")
            with open(tmp, "w") as f:
                json.dump(self.store, f, indent=2, sort_keys=True)
            os.replace(tmp, self.path)
        except Exception as e:
            print(f"  [LLMCache] WARN: failed to flush {self.path}: {e}")

    def summary(self) -> str:
        if not self.enabled:
            return "[LLMCache] disabled"
        total = self.hits + self.misses
        rate = (self.hits / total * 100) if total else 0
        return (
            f"[LLMCache] hits={self.hits} misses={self.misses} "
            f"({rate:.0f}% hit rate, {len(self.store)} cached entries, "
            f"file={self.path})"
        )

    def print_summary_once(self) -> None:
        if self._summary_printed:
            return
        if self.hits + self.misses == 0:
            return
        print(f"  {self.summary()}")
        self._summary_printed = True


_default_cache: LLMResponseCache | None = None


def get_default_cache() -> LLMResponseCache:
    global _default_cache
    if _default_cache is None:
        _default_cache = LLMResponseCache()
        atexit.register(_default_cache.print_summary_once)
    return _default_cache
