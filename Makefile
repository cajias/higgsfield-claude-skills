# ==============================================================================
# higgsfield-claude-skills — local dev gate
#
# Conventions reused from github.com/cajias/lint-configs:
#   - Python linting via the shared ruff.toml resolved from the lint_configs pkg
#   - mypy + black for the Python toolchain (managed by uv)
#   - markdownlint + prettier for docs (managed by npm, optional/guarded)
#
# Usage:
#   make            # show this help (default)
#   make install    # sync python deps + npm deps
#   make check      # full local gate: lint + validate + test
#
# Notes:
#   - RUFF_CFG is resolved dynamically from the shared lint-configs package.
#   - npm-based targets are guarded: they no-op if package.json is absent.
#   - Recipes use TABS (required by GNU make).
# ==============================================================================

.PHONY: help install lint lint-py lint-md format format-check validate test check

# ------------------------------------------------------------------------------
# help (default target): list available targets
# ------------------------------------------------------------------------------
help:
	@echo "Available targets:"
	@echo "  install       Sync Python deps (uv) and npm deps (if package.json)"
	@echo "  lint          Run all linters (lint-py + lint-md)"
	@echo "  lint-py       Ruff (shared config) + mypy on tests/"
	@echo "  lint-md       markdownlint via npm (if package.json)"
	@echo "  format        Auto-format: black + prettier (if package.json)"
	@echo "  format-check  Check formatting: black --check + prettier --check"
	@echo "  validate      Validate marketplace + both plugins (claude --strict)"
	@echo "  test          Run structural tests (tests/validate_structure.py)"
	@echo "  check         Full local gate: lint validate test"

# ------------------------------------------------------------------------------
# install: sync python + npm dependencies
# ------------------------------------------------------------------------------
install:
	uv sync --group dev
	@if [ -f package.json ] && command -v npm >/dev/null 2>&1; then \
		npm ci; \
	else \
		echo "skip: npm ci (no package.json or npm not installed)"; \
	fi

# ------------------------------------------------------------------------------
# lint: aggregate Python + Markdown linting
# ------------------------------------------------------------------------------
lint: lint-py lint-md

# lint-py: resolve the shared ruff config, then run ruff + mypy
lint-py:
	@RUFF_CFG=$$(uv run python -c "from lint_configs import get_ruff_config_path as g; print(g())") && uv run ruff check --config "$$RUFF_CFG" tests/
	uv run mypy tests/

# lint-md: markdownlint via npm (guarded)
lint-md:
	@if [ -f package.json ] && command -v npm >/dev/null 2>&1; then \
		npm run lint:md; \
	else \
		echo "skip: npm run lint:md (no package.json or npm not installed)"; \
	fi

# ------------------------------------------------------------------------------
# format: auto-format sources
# ------------------------------------------------------------------------------
format:
	uv run black tests/
	@if [ -f package.json ] && command -v npm >/dev/null 2>&1; then \
		npm run format; \
	else \
		echo "skip: npm run format (no package.json or npm not installed)"; \
	fi

# format-check: verify formatting without writing
format-check:
	uv run black --check tests/
	@if [ -f package.json ] && command -v npm >/dev/null 2>&1; then \
		npm run format:check; \
	else \
		echo "skip: npm run format:check (no package.json or npm not installed)"; \
	fi

# ------------------------------------------------------------------------------
# validate: strict validation of marketplace + both plugins
# ------------------------------------------------------------------------------
validate:
	claude plugin validate . --strict
	claude plugin validate ./plugins/higgsfield-prompts --strict
	claude plugin validate ./plugins/higgsfield-automation --strict

# ------------------------------------------------------------------------------
# test: deterministic structural test
# ------------------------------------------------------------------------------
test:
	uv run python tests/validate_structure.py

# ------------------------------------------------------------------------------
# check: the full local gate
# ------------------------------------------------------------------------------
check: lint validate test
