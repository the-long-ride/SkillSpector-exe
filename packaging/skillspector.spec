# -*- mode: python ; coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Build the existing SkillSpector CLI as one Windows executable."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules, copy_metadata

project_root = Path(SPECPATH).resolve().parent

# Preserve the project's packaged provider YAML files, YARA rules, and modules.
datas, binaries, hiddenimports = collect_all("skillspector")
datas += copy_metadata("skillspector", recursive=True)
datas.append((str(project_root / "model_registry.yaml"), "."))

# Providers, LangGraph nodes, and MCP tools are in part imported dynamically.
# Their Python code must be available even when the app starts with --no-llm.
for package in (
    "langgraph",
    "langchain_core",
    "langchain_openai",
    "langchain_anthropic",
    "langchain_aws",
    "mcp",
):
    hiddenimports.extend(collect_submodules(package))

analysis = Analysis(
    [str(project_root / "packaging" / "skillspector_entry.py")],
    pathex=[str(project_root / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=sorted(set(hiddenimports)),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(analysis.pure)

exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="SkillSpector",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
