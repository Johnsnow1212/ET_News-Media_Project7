# Part 1 Deliverable: Environment Inspection Report

## 1. Environment Comparison (`sys.executable` & `sys.prefix`)

### Global Execution (`global_env_output.txt`)
- **`sys.executable`**: Points to the host operating system's global Python interpreter (e.g., `C:\Users\<User>\AppData\Local\Programs\Python\...` or system WindowsApps).
- **`sys.prefix`**: Points to the base Python installation directory, matching `sys.base_prefix`.
- **`Is in Virtual Environment?`**: Evaluates to `False`.

### Isolated Execution (`uv_env_output.txt`)
- **`sys.executable`**: Points directly to the isolated binary inside the local project folder: `.../ET Project 7/.venv/Scripts/python.exe`.
- **`sys.prefix`**: Points to the root of the virtual environment (`.../ET Project 7/.venv`), diverging from `sys.base_prefix`.
- **`Is in Virtual Environment?`**: Evaluates to `True`.

---

## 2. Dynamic Isolation Mechanism in `uv run`

Traditional virtual environment workflows require manually activating an environment script (`source .venv/bin/activate` on POSIX or `.venv\Scripts\Activate.ps1` on Windows), which modifies the current shell session's `PATH` and sets `VIRTUAL_ENV`.

`uv run` eliminates manual activation through **ephemeral child process manipulation**:
1. **Dynamic Detection**: `uv` traverses up the directory tree, discovers `pyproject.toml` and `.venv`, and inspects the runtime requirements.
2. **Subprocess Environment Injection**: When launching the command, `uv` forks the process and injects `.venv/Scripts` (or `.venv/bin`) at the very front of the child process's `PATH`.
3. **Environment Variables**: It sets `VIRTUAL_ENV` directly for the subprocess.
4. **Shell Hygiene**: Because these environment modifications are applied exclusively to the spawned child process, the host shell remains completely unmodified and unpolluted.


## Part 2: Live API Connection & 12-Factor Secret Hygiene

### 1. Git Status Output
*Paste the output of `git status` proving that `.env` is omitted and `.env.template` is tracked:*

```bash
$ git status
On branch feature/part-1-Kiran
Your branch is based on 'origin/feature/part-1-Kiran', but the upstream is gone.
  (use "git branch --unset-upstream" to fixup)

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .gitignore
	modified:   pyproject.toml
	deleted:    src/epita_kiran_kumar_ganesan/scripts/inspect_env.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.env.template
	src/epita_kiran_kumar_ganesan/client.py
	src/epita_kiran_kumar_ganesan/config.py
	uv.lock

no changes added to commit (use "git add" and/or "git commit -a")

Live API Response : fetch_live_data()
{
  "status": "LIVE_SUCCESS",
  "articles_count": 5,
  "headline_source": "Al Jazeera English",
  "sample_headline": "Trump says US will stop giving Israel aid after year-end - Al Jazeera",
  "total_results": 36
}


## Part 3: Dependency Hygiene & Semantic Versioning

### 1. Dependency Tree (`uv tree`)
*Paste output of `uv tree`:*

```text
epita-kiran-kumar-ganesan v0.1.0
├── python-dotenv v1.2.4
├── requests v2.34.2
│   ├── certifi v2026.10.23
│   ├── charset-normalizer v3.5.2
│   ├── idna v3.20
│   └── urllib3 v2.8.0
├── rich v15.0.0
│   ├── markdown-it-py v4.2.0
│   │   └── mdurl v0.1.2
│   └── pygments v2.21.0
└── pytest v9.2.0 (group: dev)
    ├── colorama v0.4.6
    ├── iniconfig v2.3.1
    ├── packaging v26.3
    ├── pluggy v1.7.0
    └── pygments v2.21.0

## Part 4: Package Build & TestPyPI Deployment

### 1. TestPyPI Deployment Details
- **TestPyPI Package Name:** `epita-kiran-kumar-ganesan`
- **Public URL:** `https://test.pypi.org/project/epita-kiran-kumar-ganesan/`
- **CLI installation and execution output:**
```text
$ uv run --index-url [https://test.pypi.org/simple/](https://test.pypi.org/simple/) --extra-index-url [https://pypi.org/simple/](https://pypi.org/simple/) epita-kiran-kumar-ganesan-cli
╭────────────────── Live System Telemetry: LIVE_SUCCESS ───────────────────╮
│ Property        │ Value                                                  │
│─────────────────┼────────────────────────────────────────────────────────│
│ status          │ LIVE_SUCCESS                                           │
│ total_results   │ 37                                                     │
│ articles_count  │ 4                                                      │
│ headline_source │ CNBC                                                   │
│ sample_headline │ Midterm elections 2026 live updates: Economy, infla... │
╰──────────────────────────────────────────────────────────────────────────╯
```
### 2. Packaging Theory
- - **What is the difference between an `sdist` (.tar.gz) and a Wheel (.whl)?**
  A source distribution (`sdist`, `.tar.gz`) is an unbuilt archive containing raw source code and metadata; it requires the target machine to parse `pyproject.toml`, run a build backend, and potentially compile extensions at install time. A Wheel (`.whl`) is a built, standardized distribution format containing pre-compiled files and metadata that unpacks directly into `site-packages` without running arbitrary build scripts.

- **Why are Wheels significantly faster and safer to install on client machines?** 
  1. **Speed**: Wheels are pre-built ZIP archives; installation only involves extracting files directly into the target directory, bypassing source discovery, parsing, and compilation.
  2. **Security**: Installing an `sdist` runs build hooks and arbitrary Python code on the client machine with user privileges. Wheels contain only static files, eliminating arbitrary code execution during installation.


  ## Part 5: Professional Debugging Challenge (No `print()`!)

### 1. Root Cause Analysis
- **Observed types in the debugger:**  
  - Runtime type of `record['volume']`: `str`
  - Runtime type of `record['weight']`: `str`
- **Why did Python fail or miscalculate without crashing initially?**  
  `parse_api_record` splits raw CSV entries using `.split(",")` without type conversion, leaving the parsed fields as string objects. Because strings are valid dictionary values, record construction succeeded without errors. At calculation time, `volume * weight` attempted invalid string multiplication, and `total_volume += record["volume"]` performed string concatenation rather than numeric addition, causing distorted telemetry and eventual runtime failures.

### 2. Call Stack Inspection
*Describe the Call Stack frames observed when paused at the conditional breakpoint inside `compute_weighted_metric`:*
```text
Frame 1: <module> (scripts/debug_challenge.py:66)
Frame 2: aggregate_telemetry (scripts/debug_challenge.py:31)
Frame 3: compute_weighted_metric (scripts/debug_challenge.py:20)
 
 Challenges:
### 1. Root Cause Analysis
- **Observed types in the debugger:**  
  - Runtime type of `record['volume']`: `str`
  - Runtime type of `record['weight']`: `str`
- **Why did Python fail or miscalculate without crashing initially?**  
  `parse_api_record` split the raw CSV lines with `.split(",")` without type casting, keeping numerical values as strings. In Python, string values are valid dictionary items, so record creation succeeded without throwing errors. At runtime, multiplying strings or adding strings (`total_volume += record["volume"]`) performed string concatenation instead of numeric addition, producing corrupted aggregation values.

### 2. Call Stack Inspection
*Describe the Call Stack frames observed when paused at the conditional breakpoint inside `compute_weighted_metric`:*
```text
Frame 1: <module> (scripts/debug_challenge.py:66)
Frame 2: aggregate_telemetry (scripts/debug_challenge.py:31)
Frame 3: compute_weighted_metric (scripts/debug_challenge.py:20)

