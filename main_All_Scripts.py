# -*- coding: utf-8 -*-

import forest
import gvozdemet
import pnevmoteh
import pakt_barab
import pnevmopark

forest = forest.parser('https://www.for-est.ru/catalog/krepezh/gvozd/barabannye_gvozdi/index.php?display=block')



URLS_gvozdemet = ['https://gvozdemet.ru/index.php?route=product/category&path=61_185_72&page=1',
        'https://gvozdemet.ru/index.php?route=product/category&path=61_185_72&page=2',
        ]
for i in URLS_gvozdemet:
        gvozdemet.parser(i)

gvozdemet.upd_gvozdemet()



pnevmoteh = pnevmoteh.parser('https://www.pnevmoteh.ru/barabannye-gvozdi')


pakt_barab = pakt_barab.parser('https://www.pakt-group.ru/catalog/barabannie-gvozdi/c1690/')

URLS_pnevmopark = ['https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=1',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=2',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=3',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=4',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_otsinkovannye/?display=list',
        ]

for i in URLS_pnevmopark:
        pnevmopark.parser(i)

pnevmopark.upd()
