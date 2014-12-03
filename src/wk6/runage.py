import os

# RUN 1
# # change gamma_1
# os.system('python age.py 5000 0.0025 0.0005 0 100 sf 1 0 0 0.05')
# print '1 of 4 done'
# os.system('python age.py 5000 0.0025 0.0005 0 100 r 1 0 0 0.05')
# print '2 of 4 done'

# # change N
# os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 0 0.05')
# print '3 of 4 done'
# os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 0 0.05')
# print '4 of 4 done'


# RUN 2
# mortality analysis here
# # change gamma_0
# os.system('python age.py 5000 0.0025 0.001 0 100 sf 1 0 1 0.05')
# print '1 of 4 done'
# os.system('python age.py 5000 0.0025 0.001 0 100 r 1 0 1 0.05')
# print '2 of 4 done'
# os.system('python age.py 5000 0.005 0.001 0 100 sf 1 0 1 0.05')
# print '3 of 4 done'
# os.system('python age.py 5000 0.005 0.001 0 100 r 1 0 1 0.05')
# print '4 of 4 done'


# RUN 3
# # # Change gamma_0
# # os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.005 0.001 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.0015 0.001 0 100 r 1 0 0 0.05')
# # os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 0 0.05')
# os.system('python age.py 2500 0.005 0.001 0 100 sf 1 0 0 0.05')
# os.system('python age.py 2500 0.0015 0.001 0 100 sf 1 0 0 0.05')
# print 'gamma_0 done'

# # # Change gamma_1
# # os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.0025 0.0005 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.0025 0.00025 0 100 r 1 0 0 0.05')
# # os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 0 0.05')
# os.system('python age.py 2500 0.0025 0.0005 0 100 sf 1 0 0 0.05')
# os.system('python age.py 2500 0.0025 0.00025 0 100 sf 1 0 0 0.05')
# print 'gamma_1 done'

# # # Change N
# # os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 0 0.05')
# # os.system('python age.py 5000 0.0025 0.001 0 100 r 1 0 0 0.05')
# os.system('python age.py 1000 0.0025 0.001 0 100 r 1 0 0 0.05')
# # os.system('python age.py 5000 0.0025 0.001 0 100 sf 1 0 0 0.05')
# # os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 0 0.05')
# os.system('python age.py 1000 0.0025 0.001 0 100 sf 1 0 0 0.05')
# print 'N done'

# RUN 4 - gamma0_0.csv
# os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.005 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0015 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.005 0.001 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0015 0.001 0 100 sf 1 0 1 0.05')

# RUN 5 - gamma1.csv
# os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0005 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.00025 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0005 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.00025 0 100 sf 1 0 1 0.05')

# RUN 6 - N.csv
# os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 5000 0.0025 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 1000 0.0025 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 5000 0.0025 0.001 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.001 0 100 sf 1 0 1 0.05')
# os.system('python age.py 1000 0.0025 0.001 0 100 sf 1 0 1 0.05')

# RUN 7 - gamma0_1.csv
# os.system('python age.py 2500 0.0025 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.005 0.001 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0015 0.001 0 100 r 1 0 1 0.05')

# RUN 8 - Fig. 5A - vary gamma_0
# os.system('python age.py 2500 0.0075 0 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.00375 0 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.0025 0 0 100 r 1 0 0 0.05')
# os.system('python age.py 2500 0.0075 0 0 100 sf 1 0 0 0.05')
# os.system('python age.py 2500 0.00375 0 0 100 sf 1 0 0 0.05')
# os.system('python age.py 2500 0.0025 0 0 100 sf 1 0 0 0.05')

### FIXED BUG IN GAMMA_1 - FIXING PROBABILITY

# RUN 9 - reproducing paper data
# C. elegans
# os.system('python age.py 700 0.001 0.0045 0.024 100 r 1 0 0 0.05')
# os.system('python age.py 700 0.001 0.0045 0.024 100 sf 1 0 0 0.05')
# print 'C. elegans done'

# Fig 5B - vary gamma_1
# os.system('python age.py 2500 0.00625 0.003 0 100 r 1 0 0 0.05')
# print '1 done'
# os.system('python age.py 2500 0.00625 0.006 0 100 r 1 0 0 0.05')
# print '2 done'
# os.system('python age.py 2500 0.00625 0.009 0 100 r 1 0 0 0.05')
# print '3 done'
# os.system('python age.py 2500 0.00625 0.003 0 100 sf 1 0 0 0.05')
# print '4 done'
# os.system('python age.py 2500 0.00625 0.006 0 100 sf 1 0 0 0.05')
# print '5 done'
# os.system('python age.py 2500 0.00625 0.009 0 100 sf 1 0 0 0.05')
# print '6 done'
# print 'gamma_1 done'

# Fig 5C - vary N
# os.system('python age.py 2500 0.00625 0 0 100 r 1 0 0 0.05')
# print '1 done'
# os.system('python age.py 250 0.00625 0 0 100 r 1 0 0 0.05')
# print '2 done'
# os.system('python age.py 25 0.00625 0 0 100 r 1 0 0 0.05')
# print '3 done'
# os.system('python age.py 2500 0.00625 0 0 100 sf 1 0 0 0.05')
# print '4 done'
# os.system('python age.py 250 0.00625 0 0 100 sf 1 0 0 0.05')
# print '5 done'
# os.system('python age.py 25 0.00625 0 0 100 sf 1 0 0 0.05')
# print '6 done'
# print 'N done'

# Fig 5D - vary d
# os.system('python age.py 2500 0.0025 0.0025 0.14 100 r 1 0 0 0.05')
# print '1 done'
# os.system('python age.py 2500 0.0025 0.0025 0.12 100 r 1 0 0 0.05')
# print '2 done'
# os.system('python age.py 2500 0.0025 0.0025 0.1 100 r 1 0 0 0.05')
# print '3 done'
# os.system('python age.py 2500 0.0025 0.0025 0.14 100 sf 1 0 0 0.05')
# print '4 done'
# os.system('python age.py 2500 0.0025 0.0025 0.12 100 sf 1 0 0 0.05')
# print '5 done'
# os.system('python age.py 2500 0.0025 0.0025 0.1 100 sf 1 0 0 0.05')
# print '6 done'
# print 'd done'

# RUN 10 - graph mortality curves for all

# # gamma_0
# os.system('python age.py 2500 0.0075 0 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.00375 0 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0075 0 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.00375 0 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0 0 100 sf 1 0 1 0.05')
# print 'gamma_0 done'

# # gamma_1
# os.system('python age.py 2500 0.00625 0.003 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.00625 0.006 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.00625 0.009 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.00625 0.003 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.00625 0.006 0 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.00625 0.009 0 100 sf 1 0 1 0.05')
# print 'gamma_1 done'

# # N
# os.system('python age.py 2500 0.00625 0 0 100 r 1 0 1 0.05')
# os.system('python age.py 250 0.00625 0 0 100 r 1 0 1 0.05')
# os.system('python age.py 25 0.00625 0 0 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.00625 0 0 100 sf 1 0 1 0.05')
# os.system('python age.py 250 0.00625 0 0 100 sf 1 0 1 0.05')
# os.system('python age.py 25 0.00625 0 0 100 sf 1 0 1 0.05')
# print 'N done'

# # d
# os.system('python age.py 2500 0.0025 0.0025 0.14 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0025 0.12 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0025 0.1 100 r 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0025 0.14 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0025 0.12 100 sf 1 0 1 0.05')
# os.system('python age.py 2500 0.0025 0.0025 0.1 100 sf 1 0 1 0.05')
# print 'd done'

# RUN 11 - different parameters

# save graphs
# os.system('python age.py 10000 0.0075 0.003 0 100 r 1 1 0 0.05')
# print 'r saved'
# os.system('python age.py 10000 0.0075 0.003 0 100 sf 1 1 0 0.05')
# print 'sf saved'

# # Fig. 5A - vary gamma_0
# os.system('python age.py 2500 0.0075 0.003 0 100 r 1 0 0 0.05')
# print '1 done'
# os.system('python age.py 2500 0.00375 0.003 0 100 r 1 0 0 0.05')
# print '2 done'
# os.system('python age.py 2500 0.0025 0.003 0 100 r 1 0 0 0.05')
# print '3 done'
# os.system('python age.py 2500 0.0075 0.003 0 100 sf 1 0 0 0.05')
# print '4 done'
# os.system('python age.py 2500 0.00375 0.003 0 100 sf 1 0 0 0.05')
# print '5 done'
# os.system('python age.py 2500 0.0025 0 0.003 100 sf 1 0 0 0.05')
# print '6 done'
# print 'gamma_0 done'

# Fig 5B - vary gamma_1 - not frail
# os.system('python age.py 10000 0.00625 0.003 0 100 r 0 0 0 0.05')
# print '1 done'
# os.system('python age.py 10000 0.00625 0.006 0 100 r 0 0 0 0.05')
# print '2 done'
# os.system('python age.py 10000 0.00625 0.009 0 100 r 0 0 0 0.05')
# print '3 done'
# os.system('python age.py 10000 0.00625 0.003 0 100 sf 0 0 0 0.05')
# print '4 done'
# os.system('python age.py 10000 0.00625 0.006 0 100 sf 0 0 0 0.05')
# print '5 done'
# os.system('python age.py 10000 0.00625 0.009 0 100 sf 0 0 0 0.05')
# print '6 done'
# print 'gamma_1 done'

# Fig. 5A - vary gamma_0 - not frail
# os.system('python age.py 10000 0.0075 0.003 0 100 r 0 0 0 0.05')
# print '1 done'
# os.system('python age.py 10000 0.00375 0.003 0 100 r 0 0 0 0.05')
# print '2 done'
# os.system('python age.py 10000 0.0025 0.003 0 100 r 0 0 0 0.05')
# print '3 done'
# os.system('python age.py 10000 0.0075 0.003 0 100 sf 0 0 0 0.05')
# print '4 done'
# os.system('python age.py 10000 0.00375 0.003 0 100 sf 0 0 0 0.05')
# print '5 done'
# os.system('python age.py 10000 0.0025 0 0.003 100 sf 0 0 0 0.05')
# print '6 done'
# print 'gamma_0 done'


# RUN 12: mortality curves for this data
# # Fig. 5A - vary gamma_0
# os.system('python age.py 2500 0.0075 0.003 0 100 r 1 0 1 0.05')
# print '1 done'
# os.system('python age.py 2500 0.00375 0.003 0 100 r 1 0 1 0.05')
# print '2 done'
# os.system('python age.py 2500 0.0025 0.003 0 100 r 1 0 1 0.05')
# print '3 done'
# os.system('python age.py 2500 0.0075 0.003 0 100 sf 1 0 1 0.05')
# print '4 done'
# os.system('python age.py 2500 0.00375 0.003 0 100 sf 1 0 1 0.05')
# print '5 done'
# os.system('python age.py 2500 0.0025 0 0.003 100 sf 1 0 1 0.05')
# print '6 done'
# print 'gamma_0 done'

# # Fig 5B - vary gamma_1 - not frail
# os.system('python age.py 10000 0.00625 0.003 0 100 r 0 0 1 0.05')
# print '1 done'
# os.system('python age.py 10000 0.00625 0.006 0 100 r 0 0 1 0.05')
# print '2 done'
# os.system('python age.py 10000 0.00625 0.009 0 100 r 0 0 1 0.05')
# print '3 done'
# os.system('python age.py 10000 0.00625 0.003 0 100 sf 0 0 1 0.05')
# print '4 done'
# os.system('python age.py 10000 0.00625 0.006 0 100 sf 0 0 1 0.05')
# print '5 done'
# os.system('python age.py 10000 0.00625 0.009 0 100 sf 0 0 1 0.05')
# print '6 done'
# print 'gamma_1 done'

# # Fig. 5A - vary gamma_0 - not frail
# os.system('python age.py 10000 0.0075 0.003 0 100 r 0 0 1 0.05')
# print '1 done'
# os.system('python age.py 10000 0.00375 0.003 0 100 r 0 0 1 0.05')
# print '2 done'
# os.system('python age.py 10000 0.0025 0.003 0 100 r 0 0 1 0.05')
# print '3 done'
# os.system('python age.py 10000 0.0075 0.003 0 100 sf 0 0 1 0.05')
# print '4 done'
# os.system('python age.py 10000 0.00375 0.003 0 100 sf 0 0 1 0.05')
# print '5 done'
# os.system('python age.py 10000 0.0025 0 0.003 100 sf 0 0 1 0.05')
# print '6 done'
# print 'gamma_0 done'



