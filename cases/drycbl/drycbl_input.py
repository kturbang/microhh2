import numpy as np
import netCDF4 as nc

float_type = "f8"
# float_type = "f4"

# set the height (ktot = 512)
kmax = 512
dn   = 1./kmax

n = np.linspace(dn, 1.-dn, kmax)

nloc1 = 80.*dn
nbuf1 = 16.*dn

nloc2 = 512.*dn
nbuf2 = 72.*dn

dz1 = 0.001
dz2 = 0.002
dz3 = 0.016

# set the height (ktot = 1024)
"""
kmax = 1024
dn   = 1./kmax

n  = np.linspace(dn, 1.-dn, kmax)

nloc1 = 150.*dn
nbuf1 = 32.*dn

nloc2 = 1024.*dn
nbuf2 = 192.*dn

dz1 = 0.0004 #z0 is calculated as 7.37e-4
dz2 = 0.0009765625
dz3 = 0.008
"""

dzdn1 = dz1/dn
dzdn2 = dz2/dn
dzdn3 = dz3/dn

dzdn = dzdn1 + 0.5*(dzdn2-dzdn1)*(1. + np.tanh((n-nloc1)/nbuf1)) + 0.5*(dzdn3-dzdn2)*(1. + np.tanh((n-nloc2)/nbuf2))

dz = dzdn*dn

z       = np.zeros(dz.size)
stretch = np.zeros(dz.size)

z      [0] = 0.5*dz[0]
stretch[0] = 1.

for k in range(1,kmax):
  z      [k] = z[k-1] + 0.5*(dz[k-1]+dz[k])
  stretch[k] = dz[k]/dz[k-1]

zsize = z[kmax-1] + 0.5*dz[kmax-1]
print('zsize = ', zsize)

b0    = 1.
delta = 4.407731e-3
N2    = 3.

b = np.zeros(z.size)

for k in range(kmax):
  b[k] = N2*z[k]

nc_file = nc.Dataset("drycbl_input.nc", mode="w", datamodel="NETCDF4", clobber=False)

nc_file.createDimension("z", kmax)
nc_z  = nc_file.createVariable("z" , float_type, ("z"))

nc_group_init = nc_file.createGroup("init");
nc_b = nc_group_init.createVariable("b", float_type, ("z"))

nc_z[:] = z[:]
nc_b[:] = b[:]

nc_file.close()

"""
#plot the grid
figure()
subplot(131)
plot(n,z)
subplot(132)
plot(n,dz)
subplot(133)
plot(n,stretch)
"""
