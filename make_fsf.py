#!/usr/bin/env python


nev = 8

for ev in range(1,nev+1):
    orthstr = ''
    for n in range(0,nev+1):
        orthstr = f'''{orthstr}set fmri(ortho{str(ev)}.{str(n)}) 0\n'''
    fsfstr = f'set fmri(evtitle{str(ev)}) "0-Back_Face"\n' + \
    f'set fmri(shape{str(ev)}) 3\n' + \
    f'set fmri(convolve{str(ev)}) 3\n' + \
    f'set fmri(convolve_phase{str(ev)}) 0\n' + \
    f'set fmri(tempfilt_yn{str(ev)}) 1\n' + \
    f'set fmri(deriv_yn{str(ev)}) 0\n' + \
    f'set fmri(custom{str(ev)}) "feat-config-example/events_0-Back_Face.tsv"\n' + \
    f'set fmri(gammasigma{str(ev)}) 3\n' + \
    f'set fmri(gammadelay{str(ev)}) 6\n' + \
    f'{orthstr}'
    print(fsfstr)
