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