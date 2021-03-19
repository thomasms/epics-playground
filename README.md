# A Playground for EPICS

```bash
git clone https://github.com/thomasms/epics-playground
cd epics-playground
cp ExampleRELEASE.local configure/RELEASE.local
pico configure/RELEASE.local  // change EPICS7_DIR and PVXS to match your env
make
```

## Dependencies
Third party
- [epics-base](https://github.com/thomasms/epics-base)
- [PVXS](https://github.com/thomasms/pvxs)

Other
- perl
- make
- C & C++ compilers (gcc)

## Example One
Testing out pvDatabase

## Notes
The skeleton and infrastructure of the project (Makefiles + config) are based on [epics-base/exampleCPP](https://github.com/epics-base/exampleCPP) with the license @ [LICENSE.base](./LICENSE.base).