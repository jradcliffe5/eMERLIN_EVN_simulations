import os,sys
import numpy as np
from tasks import *
from casa import *

def redshift_FITS(fitsimage,outname,redshift_old_cmb,redshift_old_lsrk, redshift_new):
	os.system('rm -rf '+outname)
	importfits(fitsimage=fitsimage, imagename=outname)
	os.system('python2.7 cosmo_calcs.py %.9f %.9f %.9f' % (redshift_old,redshift_old_lsrk,redshift_new))
	cosmo_params = np.load('cosmo_params.npy')
	print cosmo_params
	'''
	# in CASA
	# Get the major and minor axes of the model clean beam
	bmaj = imhead(imagename=cubeName,mode='get',hdkey='beammajor')
	bmin = imhead(imagename=cubeName,mode='get',hdkey='beamminor')
	# Convert radians to 1-arcsecond pixels using the qa tool
	bmaj = qa.convert(bmaj,'arcsec')['value']
	bmin = qa.convert(bmin,'arcsec')['value']
	# Gaussian beam conversion = beams / pixel
	toJyPerPix = 1.0 / (1.1331 * bmaj * bmin)
	# in CASA
	# Correct flux density for luminosity distance
	fluxScale = (dl_old/dl_new)**2 * (1.0 + z_new) / (1.0 + z_old_cmb)
	# Current peak flux (Jy / pixel)
	peak = imstat(cubeName)['max'][0] * toJyPerPix
	# Desired peak flux (using Python formatting convention)
	inbright = "%fJy/pixel" % (peak*fluxScale)
	Angular Size Scaling
	#The sky coordinates axes of the model need to be adjusted (1) to place M51 in the southern hemisphere and (2) to correct for the new angular size distance. These tasks can be accomplished by the simobserve parameters indirection (to change the location of M51 on the sky) and incell (to change the angular scale of an input pixel). To perform task (1), we'll just flip the sign of the declination using imhead. We'll use the qa tool to convert radians to sexagesimal units.
	# For clarity, build up "indirection" string one term at a time.
	indirection = "J2000 " # Epoch
	# RA
	crval1 = imhead(imagename=cubeName,mode='get',hdkey='crval1')['value']
	indirection += qa.formxxx(str(crval1)+'rad',format='hms') + " " 
	# Dec * -1
	crval2 = imhead(imagename=cubeName,mode='get',hdkey='crval2')['value']
	indirection += qa.formxxx('%frad' % (-1*float(crval2)),format='dms')
	# in CASA
	# Scale pixel size: imhead returns radians; convert to arcsec
	cdelt2 = imhead(imagename=cubeName,mode='get',hdkey='cdelt2')['value']
	oldCell = cdelt2 * 206265
	# Scale for new angular size distance
	newCell = oldCell * da_old / da_new 
	# Format the new pixel size for input to simobserve
	incell = "%farcsec" % (newCell)
	# in CASA
	# Move freq to z_new
	oldFreq = imhead(imagename=cubeName,mode='get',hdkey='crval3')['value']
	newFreq = oldFreq * (1.0 + z_old_lsrk) / (1.0 + z_new)
	nchan = imstat("NGC5194.bima12m.cm.fits")['trc'][2]
	# Adjust frequency channelwidth for new z
	oldDnu = imhead(imagename=cubeName,mode='get',hdkey='cdelt3')['value']
	newDnu = abs((1.0+z_old_lsrk) /(1.0+z_new)*oldDnu) # make channel widths positive
	inwidth = "%fHz" % newDnu
	# Specify the observing frequency at the center of the observing band:
	incenter = "%fHz" % (newFreq + 0.5*nchan*newDnu)
	'''

