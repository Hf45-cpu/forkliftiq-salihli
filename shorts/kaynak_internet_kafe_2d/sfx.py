for k in range(40): add(sfx, pan(click(.18), rng.uniform(-.7, .7)), scenes[1] + .3 + k*.17 + rng.random()*.05)   # klavye
for k in range(8): add(sfx, pan(beep(880 + 220*(k % 4), .08, .05), (-1)**k*.3), capT('TAKIMLAR') + k*.18)          # oyun bipleri
n = int(.8*SR); xs = np.arange(n)/SR; add(sfx, pan(sq(55, n)*np.exp(-xs*2)*.12, 0), capT('TİTREŞİM'))                # titreşim vızıltısı
for k in range(6): add(sfx, pan(beep(1400 if k % 2 else 1000, .14, .06), 0), capT('SÜRENİZ') + k*.25)             # süre alarmı
add(sfx, pan(lp(noise(int(.4*SR)), 400)*np.hanning(int(.4*SR))*.3, 0), capT('ARTIK'))                               # ekran kapanma
