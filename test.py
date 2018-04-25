# let me see if this fucker will synchronize

a = 0.026499 # P[ Z < 0.25 ] E[z | z <0.25]
p = 0.778801 # P [ Z > 0.25 ]
t01 = 1
t12 = (a+p)/(1-p)
t02 = (t01+a+p*0.25)/(1-p)
t02

# P[Z_1 < 0.25] = 1 - p

# P[Z_1+Z_2 < 0.25 ] E[ Z_2 | Z_1+Z_2 < 0.25 ]
# = Integrate[E^(-s - t) t, {s, 0, 0.25}, {t, 0, 0.25 - s}]
b = 0.0021615/(1-p);

# P[z_1+z_2 > 0.25, z_2 < 0.25 | z_1 < 0.25]
# Integrate[E^(-s-t), {s, 0, 0.25}, {t, 0.25 - s, 0.25}]
q = 0.0224301/(1-p)

# P[z_1+z_2 > 0.25, z_2 < 0.25 | z_1 < 0.25] E[z2 | z2 < 0.25 ]
#Integrate[ t E^(-s-t),  {s, 0, 0.25}, {t, 0.25 - s, 0.25}] = 0.00370007
#c = q*0.25 + 0.00370007/(1-p)
#c = q*(1-a/(1-p)  )
c = 0.00370007/(1-p)

# and instead of 0.25*p in the last term :
# d = P[z_1+z_2 > 0.25, z_2 > 0.25 | z_1 < 0.25] E[z1|z_1 < 0.25] + 0.25*p
d = (1+0.25 + a/(1-p))*p #+ a*p/(1-p)

t03 = ( t02 + (b+c+d)/(1-q))* (1-q)/(1-q-p)
t03

# __author__ = 'fj'
#
# #integral_0^0.25 t/e^t dt
# a  = 0.026499
# #integral_0.25^infinity e^(-t)  dt = 0.778801
# p = 0.778801
# t01 = 1;
# # t12 = a + p(0.25 + t02)
# # t02 = t01 + t12
# t02 = (t01 + a + p*0.25)/(1-p)
# print(t02)
# # t23 = a + p(0.25 + t03)
# # t03 = t02 + t23
# t03 = (t02 + a + p*0.25)/(1-p)
# print(t03)
#
#
from numpy.random import exponential as erv
from numpy import mean

times = [];
for _ in range(500000):
    x = [];
    curr_t = 0;
    while len(x) < 3:
        curr_t += erv();
        x = [ _x_ for _x_ in x if _x_ > curr_t - 0.25 ] + [curr_t]

    times.append(curr_t)

mean(times)




## test the effect of mean subtraction on the estimates of