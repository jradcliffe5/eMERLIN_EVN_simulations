from astropy.cosmology import Planck15
import sys, os
import numpy as np
#from tasks import *
#from casa import *
from astropy.io import fits
from astropy import units as u

def FITSredshifter(fitsimage,outname,redshift_old_cmb,redshift_old_lsrk, redshift_new):
	print 'Combining inputs and working out cosmology'
	for i in redshift_new:
		os.system('rm '+outname+'_z_%s.fits' % i)
	name = outname
	z_old_cmb = redshift_old_cmb # CMB-referenced z for cosmological distances from NED
	z_old_lsrk = redshift_old_lsrk # from NED
	z_new = redshift_new
	#
	# angular size distances from CosmoCalc
	da_old = np.array(Planck15.kpc_proper_per_arcmin(z_old_cmb).value)/60. ## convert into kpc/arcsec
	da_new = np.array(Planck15.kpc_proper_per_arcmin(z_new).value)/60.
	#
	# luminosity distances from CosmoCalc
	dl_old = np.array(Planck15.luminosity_distance(z_old_cmb).value)
	dl_new = np.array(Planck15.luminosity_distance(z_new).value)

	cosmo_params = [name, z_old_cmb,z_old_lsrk,z_new, da_old, da_new, dl_old, dl_new]
	print cosmo_params


	for i in range(len(z_new)):
		print 'Loading FITSfile'
		hdulist = fits.open(fitsimage)
		header = hdulist[0].header
		data = hdulist[0].data
		print 'Shifting %s to redshift of %.4f' % (name,z_new[i])
		print 'Adjusting beam first'
		bmaj = header['BMAJ']*u.degree.to(u.arcsec)
		bmin = header['BMIN']*u.degree.to(u.arcsec)
		print 'Beam size = %.4f x %.4f arcsec' % (bmaj,bmin)
		toJyPerPix = 1.0 / (1.1331 * bmaj * bmin)
		print 'Generating gaussian beam conversion = beams/pixel = %.4f' % toJyPerPix
		print 'Using this to adjust flux densities'
		fluxScale = (dl_old/dl_new[i])**2 * (1.0 + z_new[i]) / (1.0 + z_old_cmb)
		print 'Generating flux scale for luminosity distance = %.9f' % fluxScale
		print 'Adjusting peak flux'
		print 'Peak flux = %.9f ' % np.max(data)
		print 'Desired peak = %.9f' % (np.max(data)*fluxScale)
		hdulist[0].data = data*fluxScale

		# Scale pixel size: imhead returns radians; convert to arcsec
		cdelt2 = header['CDELT2']
		oldCell = cdelt2
		print 'Old cell size = %.4f arcsec' % ((oldCell*u.deg).to(u.arcsec).value)
		# Scale for new angular size distance
		newCell = oldCell * da_old / da_new 
		print 'New cell size = %.4f arcsec' % ((newCell[i]*u.deg).to(u.arcsec).value)
		header['CDELT1'] = -1*newCell[0]
		header['CDELT2'] = newCell[0]
		hdulist.writeto(name+'_z_%s.fits' % z_new[i])
		hdulist.close()
	
        '''
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

FITSredshifter(fitsimage='M82_casa.fits',outname='m82',redshift_old_cmb=0.001,redshift_old_lsrk=0.001, redshift_new=[0.002,0.003])
