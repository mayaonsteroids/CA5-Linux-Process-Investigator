# Linux Process Investigator

## 1. Introduction

The Linux Process Investigator is a Python-based system monitoring project developed to explore how Linux manages running processes.

It collects process information directly from the Linux `/proc` filesystem and displays details such as process ID, parent process ID, state, memory usage, and thread count.

The project also uses Linux tools to observe system resources, CPU affinity, and system calls.

## 2. Objectives

- Understand how Linux represents and manages processes.
- Collect process information using the `/proc` filesystem.
- Identify process states and thread counts.
- Investigate CPU affinity and its effect on execution time.
- Observe system calls using `strace`.
- Export collected process information into a CSV file.

## 3. Tools and Technologies

| Tool | Purpose |
|---|---|
| Python 3 | Process investigation and CSV export |
| Linux `/proc` | Process information |
| ps | Process-state analysis |
| vmstat | System resource monitoring |
| taskset | CPU affinity control |
| strace | System-call tracing |
| Bash | Command execution and automation |
| WSL2 Ubuntu | Linux environment |

## 4. Implementation

The main program, `process_investigator.py`, reads process information from `/proc/[PID]/status`.

For each accessible process, it collects:

- PID: Process ID
- PPID: Parent Process ID
- State: Current process state
- Memory: Resident memory usage
- Threads: Number of threads
- Name: Process name

The program sorts processes by memory usage and displays the 15 processes with the highest memory consumption.

An additional CSV export feature saves all detected process records into `process_data.csv`.

## 5. Experiments and Observations

### 5.1 Process State Analysis

The `ps` command was used to inspect Linux process states.

The analysis identified:
- R: Running or runnable
- S: Interruptible sleep
- D: Uninterruptible sleep

The number of processes in each state varied between observations.

### 5.2 Resource Monitoring

The `vmstat 1 5` command was used to collect five resource-monitoring samples.

During the baseline observation, CPU idle time was 100% in each sample, indicating that the system was mostly idle.

### 5.3 CPU Affinity Experiment

The `taskset` command was used to restrict a process to CPU 0.

The restricted process reported an allowed CPU set of `{0}`, while the unrestricted process reported CPUs 0–19.

A CPU workload of 5,000,000 iterations was measured five times under each condition.

| Run | All CPUs (s) | CPU 0 only (s) |
|---|---:|---:|
| 1 | 0.2776 | 0.3111 |
| 2 | 0.2795 | 0.2870 |
| 3 | 0.2808 | 0.3086 |
| 4 | 0.3034 | 0.2812 |
| 5 | 0.2772 | 0.3028 |
| Average | 0.2837 | 0.2981 |

The CPU-restricted condition had an average execution time approximately 5.1% higher than the unrestricted condition.

Individual results varied, so this observation does not establish that CPU restriction always reduces performance.

### 5.4 System Call Tracing

The `strace -c ls` command was used to observe system calls made by the `ls` program.

The recorded experiment showed 152 system calls, including:

- `openat`
- `mmap`
- `close`
- `fstat`
- `read`
- `write`

This demonstrated how Linux programs interact with the operating system through system calls.

## 6. Engineering Improvement

The original process investigator displayed process information only in the terminal.

A CSV export feature was added using Python's built-in `csv` module.

The updated program now:
1. Collects accessible process information.
2. Sorts processes by memory usage.
3. Displays the top 15 processes.
4. Exports all detected process records into a CSV file.

The exported file can be opened in spreadsheet software for further analysis.

## 7. Limitations

- Process information represents a snapshot and can change while the program runs.
- Some processes may not be accessible because of permission restrictions or process termination.
- CPU timing measurements can vary due to background activity.
- The experiments were conducted inside WSL2, not on a standalone Linux installation.
- The CPU affinity experiment used a single-threaded workload.

## 8. Conclusion

The project provided practical experience with Linux process management, process states, resource monitoring, CPU affinity, and system calls.

By combining Python programming with Linux utilities, the project demonstrated how operating-system information can be collected, investigated, and exported for further analysis.

The CSV export feature extended the original investigator by making the collected information easier to store and examine.
