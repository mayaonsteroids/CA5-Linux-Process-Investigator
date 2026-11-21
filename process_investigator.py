import os
import csv

def get_process_info(pid):
    status_file = f"/proc/{pid}/status"

    try:
        info = {}

        with open(status_file, "r") as file:
            for line in file:
                parts = line.split(":", 1)

                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    info[key] = value

        return {
            "PID": pid,
            "Name": info.get("Name", "Unknown"),
            "PPID": info.get("PPid", "Unknown"),
            "State": info.get("State", "Unknown"),
            "Memory": info.get("VmRSS", "0 kB"),
            "Threads": info.get("Threads", "0")
        }

    except (FileNotFoundError, PermissionError, ProcessLookupError):
        return None


def export_to_csv(processes):
    filename = "process_data.csv"

    with open(filename, "w", newline="") as file:
        fieldnames = ["PID", "Name", "PPID", "State", "Memory", "Threads"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processes)

    print(f"\nProcess data exported successfully to {filename}")


def main():
    processes = []

    for entry in os.listdir("/proc"):
        if entry.isdigit():
            process = get_process_info(entry)

            if process:
                processes.append(process)

    processes.sort(
        key=lambda p: int(p["Memory"].split()[0])
        if p["Memory"].split()[0].isdigit() else 0,
        reverse=True
    )

    print("\n========== LINUX PROCESS INVESTIGATOR ==========\n")
    print(f"Total processes detected: {len(processes)}\n")

    print(f"{'PID':<8} {'PPID':<8} {'STATE':<18} {'MEMORY':<12} {'THREADS':<8} {'NAME'}")
    print("-" * 85)

    for process in processes[:15]:
        print(
            f"{process['PID']:<8} "
            f"{process['PPID']:<8} "
            f"{process['State']:<18} "
            f"{process['Memory']:<12} "
            f"{process['Threads']:<8} "
            f"{process['Name']}"
        )

    export_to_csv(processes)


if __name__ == "__main__":
    main()
