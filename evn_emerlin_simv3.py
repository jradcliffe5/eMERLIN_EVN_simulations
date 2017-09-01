import numpy as np
import sys,os

nameConv="test"

observatory = 'EVN'
target_image = 'm82_z_0.002.fits'
int_time = '3s'

if target_image.endswith('.fits'):
    importfits(fitsimage=target_image,imagename=target_image+'.image')
    target_image = target_image+'.image'
#--- Generate table for antenna inputs ---#

os.system('rm -r evn.tab')
os.system('rm -r '+nameConv+'.ms')
tabname = 'evn.tab'
asciifile = 'evn.cfg.txt'
tb.fromascii(tabname, asciifile,sep=' ')
xx=[]
yy=[]
zz=[]
diam=[]
xx = tb.getcol('X')
yy = tb.getcol('Y')
zz = tb.getcol('Z')
diam = tb.getcol('DIAM')
tb.close()

#--- Generate MS ---#
msname=nameConv+'.ms'
os.system('rm -r '+nameConv+'.ms')
sm.open(msname)


#--- Set spectral windows ---#

freq = [1.59499000,1.61049000,1.62699000,1.64249000,1.65899000,1.67449000,1.69099000,1.70649000]
for i in range(len(freq)):
    sm.setspwindow(spwname=str(i+1), freq='%.9fGHz' % freq[i], deltafreq='500kHz', freqresolution='500kHz', nchannels=32, stokes='RR LL')
'''
#SPW0
sm.setspwindow(spwname = 'SPW0',
               freq = (str(bb_1_start)+'GHz'),
               deltafreq = channel_inc,
               freqresolution = channel_inc,
               nchannels = int(1),
               stokes = 'XX XY YX YY')
#SPW1
sm.setspwindow(spwname = 'SPW1',
               freq = (str(bb_2_start)+'GHz'),
               deltafreq = channel_inc,
               freqresolution = channel_inc,
               nchannels = int(1),
               stokes = 'XX XY YX YY')
#SPW2
sm.setspwindow(spwname = 'SPW2',
               freq = (str(bb_3_start)+'GHz'),
               deltafreq = channel_inc,
               freqresolution = channel_inc,
               nchannels = int(1),
               stokes = 'XX XY YX YY')
#SPW3
sm.setspwindow(spwname = 'SPW3',
               freq = (str(bb_4_start)+'GHz'),
               deltafreq = channel_inc,
               freqresolution = channel_inc,
               nchannels = int(1),
               stokes = 'XX XY YX YY')
'''

observatory_position = me.observatory(observatory)

sm.setconfig(telescopename=observatory, x=xx, y=yy, z=zz, dishdiameter=diam,  mount='alt-az', antname='EVN', coordsystem='local', referencelocation=observatory_position)

sm.setfeed(mode='perfect R L')

#--- Initialize the source and calibrator ---#
sm.setfield(sourcename='Calibrator', sourcedirection=['J2000','09h55m52.2s','+69.41.47.0'], calcode='A')
## Set cal 1 deg away in dec
sm.setfield(sourcename='M82_highz', sourcedirection=['J2000','09h55m52.2s','+69.40.47.0'])

sm.settimes(integrationtime=int_time,
            usehourangle=True)
            #referencetime=ref_time)

sm.setauto(autocorrwt=0.0)

scan = 0

for i in range(len(freq)):
    sm.observe('M82_highz', str(i+1), starttime='0s', stoptime='10s')
# me.doframe(ref_time)
# me.doframe(observatory_position)
# now_time=qa.time(str(start_HA+scanlength_s/2) + 's')#-- CASA 4.1 work around for some reason the qa.time started writing tuples not just strings
# hadec = me.direction('hadec', now_time[0], Dec_central)
# azel = me.measure(hadec, 'azel')
sm.setdata(msselect = 'SCAN_NUMBER==1')
sm.predict(imagename = target_image)

sm.setnoise(mode = 'simplenoise', simplenoise = '5uJy')

#--- Uncomment if want corrupt data ---#
#sm.corrupt()

sm.done()
