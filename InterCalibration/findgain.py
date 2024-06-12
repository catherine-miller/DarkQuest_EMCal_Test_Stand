#################################################################
# Title: FindGain
# Description: Find Janus gain settings to align energy peaks
#              for several uncalibrated channels
# Author: Catherine Miller, cmiller6@bu.edu
# Date: 6 June 2024
#################################################################

def gauss(x,a,b,d):
        f = b*np.exp(-d*(x-a)**2)
        return f


def find_nearest(array, value): #returns index of first component in array that is higher than "value"
    i = 0
    #print(array[i])
    #print(value)
    while array[i] < value:
        i += 1
    return i

#function to find gain setting
def find_gain(gf, gs, gs_initial, MPV_f, MPV_i):
    target = MPV_f/MPV_i #target change factor
    #plt.style.use(hep.style.ROOT)
    init = gf[np.where(gs == gs_initial)[0]] #initial gain factor
    target_gf = target*gf[np.where(gs == gs_initial)[0]] #target gain factor
    '''if target_gf < 1:
        print("Error: gain factor cannot be less than 1")
        return 1'''
    i = find_nearest(gf, target_gf)
    slope = (gf[i]-gf[i-1])/(gs[i]-gs[i-1])
    x = (target_gf - gf[i])/slope
    closest_gs = gs[i] + np.round(x)
    print("The closest gain setting is "+str(closest_gs))
    print("This will give an estimated MPV of "+str(np.round((slope*np.round(x)+gf[i])/init*MPV_i,0)))
    '''
    plt.figure()
    plt.title("Gain Factor vs. DT5202 Gain Setting")
    plt.ylabel("Gain Factor (MPV/MPV$_{GS=1}$)")
    plt.xlabel("Gain Setting")
    plt.errorbar(gs, gf,yerr=gf*.06,fmt='o',markersize=3,label="experimental gain factor (linear interpolation)",linestyle="dotted", color='red')
    plt.plot(gs,np.repeat(target_gf,len(gs)),label="target gain factor = "+str(np.round(target_gf,3)[0]),color='green')
    plt.plot(gs,np.repeat(init,len(gs)),label="initial gain factor = "+str(np.round(init,3)[0]),color='blue')
    plt.legend()
    plt.savefig("gaincalib.png")
    '''
    return closest_gs

def calibrate(HG):
    if HG == True:
        df = pandas.read_csv(homedir+"DataFiles/gainscan_scaled.csv", names = ["gain","gainfactor","gferr","res","reserr"])
        gs = np.array(df['gain'])
        gf = np.array(df['gainfactor'])
    else:
        gs = np.array([1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,35,40,45,50])
        gf = np.array([1411,1424,1447,1484.8,1506.4,1539.4,1557.3,1585.8,1613.5,1645.1,1711.1,1777.6,1854.1,1927.7,2023.9,2284,2612,3129.5,3720,4646,6216])/1411
