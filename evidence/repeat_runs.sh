#!/bin/bash
for i in 1 2 3 4 5; do
  D=/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/run86/rep$i
  rm -rf $D && mkdir -p $D && rsync -a --exclude results/records /private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/60591968-b130-4d59-88a4-09fab0de0530/scratchpad/run/suite/ $D/suite/ && mkdir -p $D/suite/results/records
  (cd $D/suite && python3 runner/record_all.py --tool v8.4=/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/run86/esbmc84_mem.sh --tool v8.6=/private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/run86/esbmc86_mem.sh --timeout 120 > /private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/run86/rep$i.log 2>&1)
done
echo done > /private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/run86/done.flag
