# Building ESBMC-PLC v8.4 on macOS (Apple Silicon), without admin rights

`tools/BUILD_AND_RUN.md` gives the reproducible linux/amd64 Docker recipe, and that
remains the reference. This file records a native arm64 macOS build, used when no
container runtime is available. It needs no `sudo` and no Homebrew.

Verified 2026-08-26 on macOS 26.6.2, Apple Silicon, Xcode CLT 26.6, against ESBMC
`61172c6f` (tag v8.4).

**A binary built this way is not the artifact binary.** It uses LLVM 18.1.8 instead of
22.1.6, on a different platform. Run `probe/p0_sanity` before trusting any verdict from it.

## Toolchain (all under `~/esbmc-toolchain`, no admin)

```bash
T=~/esbmc-toolchain; mkdir -p "$T/bin" "$T/src"
# cmake + ninja: official standalone binaries
# boost 1.87: ./bootstrap.sh --with-libraries=date_time,program_options,iostreams,filesystem
# zstd 1.5.6: make -C lib install PREFIX="$T"
# bison 3.8.2: ./configure --prefix="$T" && make && make install
```

## Six blockers, in the order they appear

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | no Darwin LLVM at the pinned version | `Options.cmake` says `# these URLs are all for an x86_64 target`; LLVM 22.1.6 ships no Darwin build | override `ESBMC_LLVM_URL`/`_NAME` to `clang+llvm-18.1.8-arm64-apple-macos11`. `CMakeLists.txt:20` allows majors 11–22 |
| 2 | `zstd::libzstd_static` target not found | LLVM's prebuilt `LLVMExports.cmake` links it; `LLVMConfig.cmake:280` calls `find_package(zstd)`; macOS ships no zstd, not even in the SDK | build zstd, pass `-DCMAKE_PREFIX_PATH=$T` |
| 3 | `Z3 version: <hex>` → "Expected version 4.8.9 or greater" | `libz3.dylib`'s install name is the bare `libz3.dylib`, so CMake's `try_run` probe dies in dyld. The version regex `([0-9]+.[0-9]+.[0-9]+.[0-9]+)` then matches the crash text, since `.` matches any character | `install_name_tool -id "<abs path>" libz3.dylib && codesign -f -s -` |
| 4 | BISON "at least 2.6.1 (found /usr/bin/bison)" | macOS ships bison 2.3 (2006) | build bison 3.8.2, pass `-DBISON_EXECUTABLE` |
| 5 | undefined `boost::filesystem::detail::*` when linking `c2goto` | ESBMC lists filesystem under `OPTIONAL_COMPONENTS` for boost-1.89 compatibility, so configure only warns `missing components: filesystem` | build boost **with** filesystem |
| 6 | `complex.c:1: 'complex.h' file not found` | `c2goto`'s clang driver does not consult the macOS SDK when compiling ESBMC's own libc models | patch `src/c2goto/CMakeLists.txt` to append `--sysroot $(xcrun --show-sdk-path)` on `APPLE`, reusing the option its CHERI configs already pass. Also set `-DENABLE_BUNDLE_LIBC_32BIT=Off` (no i386 in the Apple Silicon SDK) |

Blockers 3 and 6 are worth reporting upstream. Blocker 3 misreports a broken dylib install
name as a version error, which points at entirely the wrong thing. Blocker 6 means ESBMC
v8.4 cannot build its own C library models on macOS at all.

## Configure

```bash
cmake -S . -B build -GNinja -DCMAKE_BUILD_TYPE=Release \
  -DDOWNLOAD_DEPENDENCIES=On -DCMAKE_PREFIX_PATH="$T" \
  -DBISON_EXECUTABLE="$T/bin/bison" -DFLEX_EXECUTABLE=/usr/bin/flex \
  -DENABLE_BUNDLE_LIBC_32BIT=Off \
  -DESBMC_LLVM_URL=".../clang+llvm-18.1.8-arm64-apple-macos11.tar.xz" \
  -DESBMC_LLVM_NAME="clang+llvm-18.1.8-arm64-apple-macos11" \
  -DESBMC_Z3_URL=".../z3-4.13.3-arm64-osx-13.7.zip" \
  -DESBMC_Z3_NAME="z3-4.13.3-arm64-osx-13.7" \
  -DBOOST_ROOT="$T" -DBoost_NO_SYSTEM_PATHS=On \
  -DENABLE_LD_FRONTEND=On -DENABLE_Z3=On \
  -DENABLE_BOOLECTOR=Off -DENABLE_YICES=Off -DENABLE_BITWUZLA=Off \
  -DENABLE_GOTO_CONTRACTOR=Off -DBUILD_TESTING=Off -DENABLE_REGRESSION=Off \
  -DENABLE_SOLIDITY_FRONTEND=Off -DENABLE_JIMPLE_FRONTEND=Off \
  -DENABLE_PYTHON_FRONTEND=Off -DENABLE_CSMITH=Off
cmake --build build --target esbmc -j12
```

Note: macOS has no GNU `timeout`. Use ESBMC's own `--timeout Ns`.
