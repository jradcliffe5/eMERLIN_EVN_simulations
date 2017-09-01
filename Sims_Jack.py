nameConv="SomeSims"

channel_inc="something"

#--- Generate MS ---#
msname=nameConv+'.ms'
os.system('rm -r '+nameConv+'.ms')
sm.open(msname)

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


observatory_position = me.observatory(observatory)

sm.setconfig(telescopename = observatory,
	x = xx,
	y = yy,
	z = zz,
	dishdiameter = diam.tolist(),
	mount = 'ALT-AZ',
	coordsystem = 'local',
	referencelocation = observatory_position)

sm.setfeed(mode='perfect R L')

sm.setfield(sourcename='ALMA_OST',
	sourcedirection = me.direction("J2000", RA_central, Dec_central))

sm.settimes(integrationtime = int_time,
	usehourangle=True,
	referencetime=ref_time)

sm.setlimits(shadowlimit=0.001,
	elevationlimit=elevation_limit)

sm.setauto(autocorrwt=0.0)

scan = 0

sm.observe('ALMA_OST', 'SPW0', starttime = start_HA_array_str[0], stoptime = end_HA_array_str[0])
sm.observe('ALMA_OST', 'SPW1', starttime = start_HA_array_str[0], stoptime = end_HA_array_str[0])
sm.observe('ALMA_OST', 'SPW2', starttime = start_HA_array_str[0], stoptime = end_HA_array_str[0])
sm.observe('ALMA_OST', 'SPW3', starttime = start_HA_array_str[0], stoptime = end_HA_array_str[0])

# me.doframe(ref_time)
# me.doframe(observatory_position)
# now_time=qa.time(str(start_HA+scanlength_s/2) + 's')#-- CASA 4.1 work around for some reason the qa.time started writing tuples not just strings
# hadec = me.direction('hadec', now_time[0], Dec_central)
# azel = me.measure(hadec, 'azel')
sm.setdata(msselect = 'SCAN_NUMBER==1')
sm.predict(imagename = yourimage)

sm.setnoise(mode = 'simplenoise', simplenoise = '0.1mJy')

sm.corrupt()

sm.done()
