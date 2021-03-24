# A Playground for EPICS
![build](https://github.com/thomasms/epics-playground/actions/workflows/build.yml/badge.svg)

```bash
git clone https://github.com/thomasms/epics-playground
source scripts/build_all.sh
```
or more if you already have epics-base and PVXS elsewhere then do
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

Optionally, there are python examples given in the `py` directory, and of course will require Python 3. In addition to this please see the requirements.txt file in the directory to see all required packages.

## Examples
### Servers
A variety of server examples are provided in the server subdir.

#### **Simple**
The most basic example using pvAccess + pvDatabase.

### Clients

todo...

## Notes
The skeleton and infrastructure of the project (Makefiles + config) are based on [epics-base/exampleCPP](https://github.com/epics-base/exampleCPP) with the license @ [LICENSE.base](./LICENSE.base).