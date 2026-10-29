#!/bin/bash
set -e
cd /private/tmp/claude-502/-Users-user-Claude-4-Papers-ESBMC-Benchmark-Suite--Springer---Scientific-Reports-/9808ce5c-61da-4ccd-9a0e-9bfc09950a37/scratchpad/esbmc86src
export PATH=/Users/user/esbmc-toolchain/cmake-4.4.3-macos-universal/CMake.app/Contents/bin:$PATH
cmake -S . -B build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBOOST_ROOT=/Users/user/esbmc-toolchain -DBoost_DIR=/Users/user/esbmc-toolchain/lib/cmake/Boost-1.87.0 -DCMAKE_PREFIX_PATH=/Users/user/esbmc-toolchain -DClang_DIR=/opt/homebrew/opt/llvm@22/lib/cmake/clang -DLLVM_DIR=/opt/homebrew/opt/llvm@22/lib/cmake/llvm -DZ3_DIR=/Users/user/esbmc-toolchain/src/esbmc-master/build/Z3/z3-4.13.3-arm64-osx-13.7 -DENABLE_Z3=On -DENABLE_LD_FRONTEND=On -DENABLE_PYTHON_FRONTEND=OFF -DENABLE_SOLIDITY_FRONTEND=OFF -DENABLE_REGRESSION=OFF -DBUILD_TESTING=OFF -DDOWNLOAD_DEPENDENCIES=On -DCMAKE_OSX_SYSROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk
cmake --build build -j12 --target esbmc
