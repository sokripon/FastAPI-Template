import subprocess

import utils.settings

start_command = ["uvicorn", "main:app", f"--port={utils.settings.setting.app_port}", f"--host={utils.settings.setting.app_host}"]
if utils.settings.setting.debug:
    start_command.append("--reload")
if utils.settings.setting.root_path:
    start_command.append(f"--root-path={utils.settings.setting.root_path}")

subprocess.run(start_command)
