set -e
echo "[1/5] apt deps..."; export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq build-essential cmake ninja-build git wget curl \
  gcc-12 g++-12 g++-multilib libc6-dev-i386 libboost-all-dev libgmp-dev libssl-dev \
  bison flex python3 patchelf ca-certificates >/dev/null
echo "[2/5] copy source to container fs..."; cp -r /src-ro /work && cd /work
echo "[3/5] cmake configure (DOWNLOAD_DEPENDENCIES fetches clang/llvm/z3)..."
cmake -S . -B build -GNinja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=gcc-12 -DCMAKE_CXX_COMPILER=g++-12 \
  -DDOWNLOAD_DEPENDENCIES=On -DENABLE_BOOLECTOR=Off -DENABLE_YICES=Off \
  -DENABLE_BITWUZLA=Off -DENABLE_GOTO_CONTRACTOR=Off -DBUILD_TESTING=Off \
  -DENABLE_REGRESSION=Off -DENABLE_SOLIDITY_FRONTEND=Off -DENABLE_JIMPLE_FRONTEND=Off \
  -DENABLE_PYTHON_FRONTEND=Off -DENABLE_CSMITH=Off -DENABLE_LD_FRONTEND=On -DENABLE_Z3=On
echo "[4/5] building esbmc (-j6)..."; cmake --build build --target esbmc -j6
echo "[5/5] bundling binary + libz3..."
Z3_LIB=$(find build -name "libz3.so*" | head -1); echo "z3: $Z3_LIB"; cp "$Z3_LIB" /out/libz3.so 2>/dev/null || true
patchelf --set-rpath /usr/local/lib build/src/esbmc/esbmc 2>/dev/null || true
cp build/src/esbmc/esbmc /out/esbmc-linux-amd64
export LD_LIBRARY_PATH=/out:$LD_LIBRARY_PATH
echo "=== VERSION ==="; /out/esbmc-linux-amd64 --version 2>&1 | head -2
echo "=== ld-props present? ==="; /out/esbmc-linux-amd64 --help 2>&1 | grep -c "ld-props" || echo 0
echo "BUILD_DONE_OK"
