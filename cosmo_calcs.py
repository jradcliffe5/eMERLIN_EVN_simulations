from astropy.cosmology import Planck15
import sys, os
import numpy as np
#from tasks import *
#from casa import *

name = str(sys.argv[1])
z_old_cmb = float(sys.argv[2]) # CMB-referenced z for cosmological distances from NED
z_old_lsrk = float(sys.argv[3]) # from NED
z_new = float(sys.argv[4])
#
# angular size distances from CosmoCalc
da_old = Planck15.kpc_proper_per_arcmin(z_old_cmb).value/60. ## convert into kpc/arcsec
da_new = Planck15.kpc_proper_per_arcmin(z_new).value/60.
#
# luminosity distances from CosmoCalc
dl_old = Planck15.luminosity_distance(z_old_cmb).value
dl_new = Planck15.luminosity_distance(z_new).value

print da_old, da_new, dl_old, dl_new
os.system('rm cosmo_params.npy')
np.save('cosmo_params.npy',[name, z_old_cmb,z_old_lsrk,z_new, da_old, da_new, dl_old, dl_new])
