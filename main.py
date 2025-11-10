import wmi
import subprocess

def WMIProcessCreation(name):
    c = wmi.WMI()
    # Create returns a tuple (process_id, return_value) depending on environment;
    # capture the full result to avoid unpack errors on different platforms.
    result = c.Win32_Process.Create(CommandLine=name)
    print("WMI Create result:", result)
    try:
        # Try to unpack if possible for nicer output
        pid, returnValue = result
        print(f"Process {name} created with PID {pid} (ReturnValue={returnValue})")
    except Exception:
        # Fallback: print the raw result
        print(f"Process {name} created — raw result: {result}")

def PSProcessCreation(name):
    # This runs PowerShell to start the process and print the PID
    ps_command = (
        f"Start-Process -FilePath '{name}' -PassThru | Select-Object -ExpandProperty Id"
    )
    p = subprocess.run(
        ["powershell", "-Command", ps_command],
        capture_output=True,
        text=True
    )
    if p.returncode == 0:
        pid = p.stdout.strip()
        print(f"Process {name} created with PowerShell, PID {pid}")
    else:
        print("PowerShell command failed.")
        print("stdout:", p.stdout)
        print("stderr:", p.stderr)

if __name__ == "__main__":
    command = "notepad.exe"
    WMIProcessCreation(command)
    PSProcessCreation(command)
