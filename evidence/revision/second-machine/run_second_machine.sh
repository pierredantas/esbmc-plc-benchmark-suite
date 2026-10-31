#!/usr/bin/env bash
# Second-machine timing run for R1.2: builds ESBMC 8.4 and 8.6 with the ladder front end,
# then runs the suite (release v1.3.1) five times, records BMC depths, and packs the records.
# Target: fresh Ubuntu 22.04, x86-64, 8 vCPU, 16 GB RAM, 60 GB disk.
# Usage: nohup bash run_second_machine.sh > run.log 2>&1 &
set -uo pipefail
W=$HOME/r12
mkdir -p "$W" && cd "$W"
JOBS=$(nproc)

stage() { echo; echo "=== $(date -u +%FT%TZ) $* ==="; }

stage "1/6 environment"
{
  date -u; uname -a; lsb_release -a 2>/dev/null
  lscpu; free -h; df -h "$W"
  cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || true
  curl -s --max-time 2 http://169.254.169.254/latest/meta-data/instance-type 2>/dev/null || true
} > env.txt 2>&1

stage "2/6 packages"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y -qq build-essential cmake ninja-build git curl wget unzip \
  gcc-13 g++-13 g++-multilib libc6-dev-i386 libboost-all-dev libgmp-dev libssl-dev \
  bison flex python3 python3-yaml time rsync ca-certificates

build() {  # $1 = tag, $2 = label
  stage "3/6 build ESBMC $1"
  [ -d "esbmc-$2" ] || git clone --depth 1 --branch "$1" https://github.com/esbmc/esbmc.git "esbmc-$2"
  ( cd "esbmc-$2" &&
    cmake -S . -B build -GNinja -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_COMPILER=gcc-13 -DCMAKE_CXX_COMPILER=g++-13 \
      -DDOWNLOAD_DEPENDENCIES=On -DENABLE_BOOLECTOR=Off -DENABLE_YICES=Off \
      -DENABLE_BITWUZLA=Off -DENABLE_GOTO_CONTRACTOR=Off -DBUILD_TESTING=Off \
      -DENABLE_REGRESSION=Off -DENABLE_SOLIDITY_FRONTEND=Off -DENABLE_JIMPLE_FRONTEND=Off \
      -DENABLE_PYTHON_FRONTEND=Off -DENABLE_CSMITH=Off -DENABLE_LD_FRONTEND=On -DENABLE_Z3=On &&
    cmake --build build --target esbmc -j"$JOBS" ) || { echo "BUILD FAILED for $1"; return 1; }
  B="$W/esbmc-$2/build/src/esbmc/esbmc"
  "$B" --version | tee "version-$2.txt"
  ( cd "esbmc-$2" && git rev-parse HEAD ) | tee "commit-$2.txt"
  "$B" --help 2>&1 | grep -c "ld-props" | sed 's/^/ld-props lines: /'
}
build v8.4 84 || exit 1
build v8.6 86 || exit 1

stage "4/6 suite v1.3.1"
[ -d suite ] || git clone --depth 1 --branch v1.3.1 https://github.com/pierredantas/esbmc-plc-benchmark-suite.git suite
( cd suite && git rev-parse HEAD ) | tee suite-commit.txt

for v in 84 86; do   # peak-RSS wrappers (GNU time, kilobytes -> bytes)
  cat > "$W/esbmc$v.sh" <<EOF
#!/bin/bash
T=\$(mktemp)
/usr/bin/time -v -o "\$T" "$W/esbmc-$v/build/src/esbmc/esbmc" "\$@"
rc=\$?
RSS=\$(awk '/Maximum resident set size/{print \$NF*1024}' "\$T")
printf '%s\t%s\n' "\$1" "\$RSS" >> "$W/mem$v.tsv"
rm -f "\$T"
exit \$rc
EOF
  chmod +x "$W/esbmc$v.sh"
done

stage "5/6 five repetitions (do not run anything else on this machine)"
for i in 1 2 3 4 5; do
  rm -rf "rep$i"; mkdir "rep$i"; rsync -a --exclude results/records --exclude .git suite/ "rep$i/suite/"
  mkdir -p "rep$i/suite/results/records"
  ( cd "rep$i/suite" &&
    python3 runner/record_all.py --tool v8.4="$W/esbmc84.sh" --tool v8.6="$W/esbmc86.sh" \
      --timeout 120 > "../record_all.log" 2>&1 )
  echo "rep$i done: $(ls rep$i/suite/results/records | wc -l) records"
done

stage "6/7 depth pass (violations, rep1 records)"
python3 "$HOME/depth_linux.py" | tee depth_linux.txt
cp "$HOME/depths_linux.json" . 2>/dev/null || true

stage "7/7 pack"
tar czf r12_results.tar.gz env.txt version-*.txt commit-*.txt suite-commit.txt mem84.tsv mem86.tsv \
  depth_linux.txt depths_linux.json rep*/record_all.log rep*/suite/results/records
ls -la r12_results.tar.gz
echo "ALL_DONE"
