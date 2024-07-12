# Modeling the ELWR

## Model 1. AP600 (17x17)


For our first model, we try a conservative approach of modeling just an infinite fuel assembly of the ELWR. The active fuel height is around 12 feet, or 3.66 meters.

# Running MCODE
(Mainly notes for Patrick)

## Recompiling MCODE for Windows
First, if you are using Windows like I am, you'll need to re-compile MCODE.
1. In `mcode12.h`, change `OPSYS==1` for Windows.
2. [Install MSYS2.](https://www.msys2.org/)
3. Install mingw-w64 in the MSYS2 `ucrt64.exe` terminal: `pacman -S mingw-w64-ucrt-x86_64-gcc`
4. Press Enter to auto-download the recommended packages.
5. Now using the `ucrt64.exe` terminal you can call `gcc` to build C software for Windows.
6. Compile using the following code:
```sh 
gcc C:/MCNP_SOURCE/MCODE12/mcode12.c -o C:/MCNP_SOURCE/MCODE12/mcode12.exe
```
with the proper substitution of file directory for `mcode12`. Repeat for `mcodeout12`.

## Setting up MCODE on Linux
1. Adding MCODE permissions. Set basic execution permission:
```sh
chmod +x ./MCODE12/mcode12
chmod +x ./MCODE12/mcodeout12
```

Set ACL for user:
```sh
setfacl -m u:patrick:rwx ./MCODE12/mcode12
setfacl -m u:patrick:rwx ./MCODE12/mcodeout12
```

2. If you're uploading text files from Windows to Linux, then you need to strip DOS return carriages from every line of your file. Install `dos2unix`:
```sh
sudo apt-get install dos2unix
```

You will run into problems with MCODE not recongizing DOS return characters if you don't manually put a space at the end of every line. (I had problems with MCODE recognizing the `WGU`, `begin_mcode_ACT`, `end_mcode_ACT` keywords.)

3. Set up MCNP `DATAPATH` in the Linux shell:
```sh
DATAPATH=/opt/MCNP/MCNP_DATA/
export DATAPATH
printenv DATAPATH
sudo nano ~/.bashrc
export DATAPATH=/opt/MCNP/MCNP_DATA/
source ~/.bashrc
```

## Executing MCODE

1. Create complete MCNP input deck, add `ksrc 0 0 0`, run, keep `.s` file.
2. Now we need to set up the MCODE input file. Here's an example:
```
$ TITLE line
TTL ELWR AP600 Model
$   CTRL command initial-inp
MCD  1   /opt/MCNP/MCNP_CODE/bin/mcnp6  elwr-caseAP600-blanket3.inp  o_elwr-caseAP600-blanket3.s
$    ORIGEN-COMMAND              ORIGEN-LIBRARY-PATH       decay-lib     gamma-lib
ORG /home/patrick/ORIGEN22/origen22  /home/patrick/ORIGEN22/LIBS   DECAY.LIB  GXUO2BRM.LIB
$  total#  CELL-ID TYPE    IHM(g)  VOL(cm3)  ORG-XS-LIB
CEL  2       11    1     477.5223    50.2655   PWRUE.LIB
             21    1     477.5223    50.2655   PWRUE.LIB
$ TOTAL VOLUME (cm3)
VOL  50.2655
$ power density, opt: WGU=W/gIHM, KWL=kW/(liter core)
PDE  38.0 WGU
$ NORMALIZATION option, 1=FLUX, 2=POWER
NOR 2
$ Predictor-Corrector option, 1=ON, 0=OFF
COR 0
$ opt E=MWd/kg, D=EFPD
$ points 0    1    2    3    4    5    6    7
DEP  E   0  0.1    1   10   20   30   40   50
NMD       18    36   36   36   36   36   36
STA  0  $  starting point
END  7  $    ending point
```
3. `TTL`: Set title
4. `MCD`: Set path to MCNP6.exe, path to MCNP input, and path to equilibrium source distribution file (optional)
5. `ORG`: Set paths to origen22.exe, Origen data libraries, decay library, and gamma library.
6. 