import utils.settings
import subprocess

subprocess.run(["uvicorn", "main:app", f"--port={utils.settings.setting.app_port}", f"--host={utils.settings.setting.app_host}"])
