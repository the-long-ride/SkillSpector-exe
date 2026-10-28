# Windows x64 single-file executable

This fork has an opt-in GitHub Actions workflow at
[`.github/workflows/build-windows-exe.yml`](../.github/workflows/build-windows-exe.yml).
It uses Python 3.12, the checked-in `uv.lock`, PyInstaller 6.22.3, and a
Windows runner to package the **existing SkillSpector CLI** into one executable.

## Download

1. Open **Actions → Build Windows single EXE** for this repository.
2. Select a successful workflow run on `build/windows-single-exe`.
3. Download the `SkillSpector-windows-x64-onefile` artifact.
4. Extract the artifact ZIP. `SkillSpector.exe` is the only executable.
   The ZIP also contains `SHA256SUMS.txt`, `LICENSE`, and
   `THIRD_PARTY_NOTICES.md` for verification and redistribution notices.

The Windows executable bundles the Python runtime and package data; Python
and uv are required **only to build it**, not to run it. PyInstaller's one-file
bootloader extracts its bundled files to a temporary directory when launched,
so startup can be slower than a normal Python command. Windows x64 only.

## Usage

In PowerShell:

```powershell
.\SkillSpector.exe --version
.\SkillSpector.exe --help
.\SkillSpector.exe scan "C:\path\to\my-skill" --no-llm
.\SkillSpector.exe scan "C:\path\to\my-skill" --no-llm --format json > "C:\Reports\report.json"
```

On Windows, SkillSpector intentionally **rejects `--output FILE`** because
its safe, no-follow file-write implementation is unavailable. To save a JSON
report, redirect stdout to a **new file outside the scan target** as shown
above. Inspect the exit code before treating that report as a successful scan.
Do not weaken the scanner's file-output safeguards to enable `--output`.

The `--no-llm` mode performs local static analysis without an LLM API key.
Optional LLM providers may make network requests and require separate
credentials or local provider executables, depending on provider settings.
Some runtime integrations can require externally installed programs such
as Git or model-serving software; a one-file EXE does not bundle them.

## Building and verification

The workflow installs application dependencies with
`uv sync --locked --extra mcp --no-dev`, then installs an explicitly pinned
PyInstaller into the build environment. It produces `dist/SkillSpector.exe`
and smoke-tests **that EXE** in a different directory containing spaces,
including `--version`, `--help`, and an offline scan with a JSON report.
Successful runs upload the executable and its SHA-256 digest.

To validate the digest from PowerShell:

```powershell
(Get-FileHash .\SkillSpector.exe -Algorithm SHA256).Hash.ToLowerInvariant()
Get-Content .\SHA256SUMS.txt
```

The two hexadecimal hashes should match. A passing smoke test checks basic
CLI functionality, not every provider, MCP transport, or antivirus environment.

This workflow does **not** publish releases, install or remove MCP entries
for AI agents, or change the default branch.
