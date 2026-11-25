for k in range(3): add(sfx, pan(tone(1760 + k*220, .9, .05, ((1, 1), (2.7, .3)), 4), .3), .5 + k*.12)   # dükkân kapı zili
add(sfx, pan(lp(noise(int(.25*SR)), 300)*np.hanning(int(.25*SR))*.5, 0), capT('SAYFA') + .5)          # damga
for k in range(4): add(sfx, pan(tone(3200 + 300*k, .25, .04, ((1, 1), (2.4, .4)), 14), (-1)**k*.4), scenes[3] + .4 + k*.2)  # bozuk para
for k in range(18): add(sfx, pan(nz(.05, 1500, 6000, .18, 60), rng.uniform(-.5, .5)), capT('AVUÇ') + k*.05)   # şeker dökülmesi
n = int(1.6*SR); xs = np.arange(n)/SR; add(sfx, pan(bp(noise(n), 200, 2500)*(.6 + .4*np.sign(np.sin(2*np.pi*14*xs)))*np.exp(-xs*.8)*.18, 0), capT('KEPENK') - .6)  # kepenk
