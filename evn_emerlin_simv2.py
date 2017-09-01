import numpy as np
import sys,os

def redshift_FITS(fitsimage,outname,redshift_old_cmb,redshift_old_lsrk, redshift_new):
	os.system('rm -rf '+outname+'.image')
	importfits(fitsimage=fitsimage, imagename=outname+'.image')
	cosmo_params = np.load('cosmo_params.npy')
	if cosmo_params[0] != outname:
		print 'Please run cosmo_calc.py with matching names'
	else:
		print 'All good! Converting cosmo_params.npy params into useful params'
		z_old_cmb = float(cosmo_params[1])
		z_old_lsrk = float(cosmo_params[2]) 
		z_new = float(cosmo_params[3])
		#
		# angular size distances from cosmo_calc.py / Astropy
		da_old = float(cosmo_params[4])
		da_new = float(cosmo_params[5])
		#
		# luminosity distances from cosmo_calc.py / Astropy
		dl_old = float(cosmo_params[6])
		dl_new = float(cosmo_params[7])
		imagename = outname+'.image'
		
		print 'Redshifting %s from %.2f to %.2f' % (outname,z_old_cmb,z_new)
		
		print 'Getting beam sizes'
		# Get the major and minor axes of the model clean beam
		bmaj = imhead(imagename=imagename,mode='get',hdkey='beammajor')
		bmin = imhead(imagename=imagename,mode='get',hdkey='beamminor')
		# Convert radians to 1-arcsecond pixels using the qa tool
		bmaj = qa.convert(bmaj,'arcsec')['value']
		bmin = qa.convert(bmin,'arcsec')['value']
		print 'Beams are: %.4f x %.4f arcsec' % (bmaj,bmin) 
		
		print 'Flux density conversion'
		# Gaussian beam conversion = beams / pixel
		toJyPerPix = 1.0 / (1.1331 * bmaj * bmin)
		print 'Generating gaussian beam conversion = beams/pixel = %.4f' % toJyPerPix
		# Correct flux density for luminosity distance
		fluxScale = (dl_old/dl_new)**2 * (1.0 + z_new) / (1.0 + z_old_cmb)
		print 'Generating flux scale for luminosity distance = %.9f' % fluxScale
		# Current peak flux (Jy / pixel)
		peak = imstat(imagename)['max'][0] * toJyPerPix
		print 'Current peak flux = %.4f Jy/pixel' % peak
		# Desired peak flux (using Python formatting convention)
		inbright = "%fJy/pixel" % (peak*fluxScale)
		print 'Desired peak flux = %s' % (inbright)
		
		print 'Angular Size Scaling'
		'''
		#The sky coordinates axes of the model need to be adjusted (1) to place M51 in the southern hemisphere and (2) to correct for the new angular size distance. These tasks can be accomplished by the simobserve parameters indirection (to change the location of M51 on the sky) and incell (to change the angular scale of an input pixel). To perform task (1), we'll just flip the sign of the declination using imhead. We'll use the qa tool to convert radians to sexagesimal units.
		# For clarity, build up "indirection" string one term at a time.
		indirection = "J2000 " # Epoch
		# RA
		crval1 = imhead(imagename=cubeName,mode='get',hdkey='crval1')['value']
		indirection += qa.formxxx(str(crval1)+'rad',format='hms') + " " 
		# Dec * -1
		crval2 = imhead(imagename=cubeName,mode='get',hdkey='crval2')['value']
		indirection += qa.formxxx('%frad' % (-1*float(crval2)),format='dms')
		'''
		# Scale pixel size: imhead returns radians; convert to arcsec
		cdelt2 = imhead(imagename=imagename,mode='get',hdkey='cdelt2')['value']
		oldCell = cdelt2 * 206265
		print 'Old cell size = %.4f arcsec' % oldCell
		# Scale for new angular size distance
		newCell = oldCell * da_old / da_new 
		print 'New cell size = %.4f arcsec' % newCell
		# Format the new pixel size for input to simobserve
		incell = "%farcsec" % (newCell)
		'''
		if adjust_freq = True
			# Move freq to z_new
			oldFreq = imhead(imagename=imagename,mode='get',hdkey='crval3')['value']
			newFreq = oldFreq * (1.0 + z_old_lsrk) / (1.0 + z_new)
			nchan = imstat("NGC5194.bima12m.cm.fits")['trc'][2]
			# Adjust frequency channelwidth for new z
			oldDnu = imhead(imagename=cubeName,mode='get',hdkey='cdelt3')['value']
			newDnu = abs((1.0+z_old_lsrk) /(1.0+z_new)*oldDnu) # make channel widths positive
			inwidth = "%fHz" % newDnu
			# Specify the observing frequency at the center of the observing band:
			incenter = "%fHz" % (newFreq + 0.5*nchan*newDnu)
		else:
			oldFreq = imhead(imagename=imagename,mode='get',hdkey='crval3')['value']
		'''
		return inbright, incell
			


print redshift_FITS(fitsimage='M82_C-BAND_E-MERLIN+JVLA.FITS',outname='M82',redshift_old_cmb=1,redshift_old_lsrk=1, redshift_new=2)
