# Second-machine timing run (R1.2)

Why: all timings in Section 6.4 come from one Apple-silicon Mac. This repeats the five-run
measurement on Linux x86-64 with ESBMC 8.4 and 8.6 built from their release tags with the
ladder front end (the Linux release binaries do not include it).

1. Rent an Ubuntu 22.04 x86-64 VM: 8 vCPU (dedicated if offered), 16 GB RAM, 60 GB disk.
   Note the provider and instance type.
2. Copy both scripts (run_second_machine.sh and depth_linux.py) and start it detached:
   `scp second-machine/run_second_machine.sh ubuntu@<ip>:~/`
   `ssh ubuntu@<ip>` then `nohup bash run_second_machine.sh > run.log 2>&1 &`
3. Watch with `tail -f run.log`. Builds take about 30 to 60 minutes each; the runs take minutes.
   The last line is `ALL_DONE`.
4. Download `~/r12/r12_results.tar.gz` and `~/run.log` with `scp`, then delete the VM.
