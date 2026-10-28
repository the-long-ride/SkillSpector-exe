# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""PyInstaller entry point for the existing SkillSpector Typer CLI."""

from skillspector.cli_entry import app


if __name__ == "__main__":
    app()
