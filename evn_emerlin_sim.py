import numpy as np

os.system('rm -r evn.tab')
os.system('rm -r NEW1.ms')
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
sm.open('NEW1.ms')
posevn = me.observatory('EVN')
sm.setconfig(telescopename='EVN', x=xx, y=yy, z=zz, dishdiameter=diam,  mount='alt-az', antname='EVN', coordsystem='local', referencelocation=posevn)

## Set frequencies, these are slightly wrong??!!
freq = [1.59499000,1.61049000,1.62699000,1.64249000,1.65899000,1.67449000,1.69099000,1.70649000]
for i in range(8):
	sm.setspwindow(spwname=str(i+1), freq='%.9fGHz' % freq[i], deltafreq='500kHz', freqresolution='500kHz', nchannels=32, stokes='RR LL LR RL')

# Initialize the source and calibrater 
sm.setfield(sourcename='Calibrator', sourcedirection=['J2000','09h55m52.2s','+69.41.47.0'], calcode='A') 
## Set cal 1 deg away in dec
sm.setfield(sourcename='M82_highz', sourcedirection=['J2000','09h55m52.2s','+69.40.47.0'])
sm.settimes(integrationtime='3s', usehourangle=False,  referencetime=me.epoch('utc', 'today'))

for i in range(8):
	sm.observe('M82_highz',str(i+1), starttime='0s', stoptime='10s');
	sm.observe('Calibrator',str(i+1), starttime='10s', stoptime='20s')

sm.setdata(spwid=0, fieldid=1)
sm.predict(imagename='test')
sm.close()
