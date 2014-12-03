import os

# change gamma_1
os.system('python age.py 5000 0.0025 0.0005 0 100 sf 1 0 0 0.05')
print '1 of 4 done'
os.system('python age.py 5000 0.0025 0.0005 0 100 r 1 0 0 0.05')
print '2 of 4 done'

# change N
os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 0 0.05')
print '3 of 4 done'
os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 0 0.05')
print '4 of 4 done'