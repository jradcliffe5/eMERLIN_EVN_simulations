import numpy as np
from AIPS import AIPS, AIPSDisk
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage, AIPSCat
from Wizardry.AIPSData import AIPSUVData as WizAIPSUVData

AIPS.userno = 1002
modelimage = AIPSImage('M82','ICLN',1,1)

uvcon = AIPSTask('UVCON')
uvcon.infile = 'PWD:evn_aips.txt'
uvcon.in2data = modelimage
uvcon.cmodel = 'IMAG'
uvcon.aparm[1] = 1.59499000 ## Frequency of channel 1
uvcon.aparm[7] = 36000 ## Integration time
uvcon.aparm[8] = 5 ## channel increment
uvcon.aparm[9] = 32 ## no. of frequency channels
uvcon.cparm[1] = 8
uvcon.cparm[2:] = [1594.99000,1610.49000,1626.99000,1642.49000,1658.99000,1674.49000,1690.99000,1706.49000]
uvcon.go()
