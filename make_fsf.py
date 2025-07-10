#!/usr/bin/env python

# Basic waveform shape (EV 1)
# 0 : Square
# 1 : Sinusoid
# 2 : Custom (1 entry per volume)
# 3 : Custom (3 column format)
# 4 : Interaction
# 10 : Empty (all zeros)
#set fmri(shape1) 3

# Convolution (EV 1)
# 0 : None
# 1 : Gaussian
# 2 : Gamma
# 3 : Double-Gamma HRF
# 4 : Gamma basis functions
# 5 : Sine basis functions
# 6 : FIR basis functions
# 8 : Alternate Double-Gamma
#set fmri(convolve1) 2


nev = 8

for ev in range(1,nev+1):

    orthstr = ''
    for n in range(0,nev+1):
        orthstr = f'''{orthstr}set fmri(ortho{str(ev)}.{str(n)}) 0\n'''

    fsfstr = f'set fmri(evtitle{str(ev)}) "0-Back_Face"\n' + \
    f'set fmri(shape{str(ev)}) 3\n' + \
    f'set fmri(convolve{str(ev)}) 2\n' + \
    f'set fmri(convolve_phase{str(ev)}) 0\n' + \
    f'set fmri(tempfilt_yn{str(ev)}) 1\n' + \
    f'set fmri(deriv_yn{str(ev)}) 0\n' + \
    f'set fmri(custom{str(ev)}) "SUBJDIR/events_0-Back_Face.tsv"\n' + \
    f'set fmri(gammasigma{str(ev)}) 3\n' + \
    f'set fmri(gammadelay{str(ev)}) 6\n' + \
    f'{orthstr}'

    print(fsfstr)
