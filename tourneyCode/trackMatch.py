#Track Match for a particular round in VG Tournament
#Input: 6 IGNS of a particular round.

import getHKDA

stats = getHKDA.getMatchStats("Berand,Eddie12314,AirStriker")

if stats[1] == 'True':
    print ('Winners are', stats[2]['ign'], stats[3]['ign'], stats[4]['ign'])
else:
    print('Winners are', stats[6]['ign'], stats[7]['ign'], stats[8]['ign'])


