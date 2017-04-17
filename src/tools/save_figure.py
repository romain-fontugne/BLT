import sys
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import pickle
import argparse



def load_pickele(pickele_file):
	with open(pickele_file, mode="rb") as f:
	    pfx_data = pickle.load(f)
	f.close
	return pfx_data

def save_figure(pfx_data, x_axis, y_axis):
    y_max = 0
    if x_axis == "prefix":
        result = traffic_vs_prefix(pfx_data, y_axis)
        x = result[0]
        y = result[1]
        x_max = len(x)
        y_max = y[-1]

    else:
        pfx_list = sorted(pfx_data.items(), key=lambda x: x[1][x_axis])

        x=[]
        y=[]

        for pfx in pfx_list:
            x.append(pfx[1][x_axis])
            y.append(pfx[1][y_axis])
            if pfx[1][y_axis] > y_max:
                y_max = pfx[1][y_axis]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(x,y)

    ax.set_title(y_axis + ' vs ' + x_axis)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_xscale("log")
    ax.set_yscale("log")
    #ax.set_xlim(xmin = 0)
    #ax.set_xlim(xmax = x_max*1.1)
    #ax.set_ylim(ymin = 0)
    #ax.set_ylim(ymax = 2500)
    plt.savefig( "../../Data/graphs/" + y_axis + "_vs_"+ x_axis +'.png' )

def traffic_vs_prefix(pfx_list, y_axis):
	volume = []
	for pfx in pfx_list.items():
		volume.append(int(pfx[1][y_axis]))
	
	y = sorted(volume)
	x = range(1,len(volume)+1)
    
        print "len(x): " + str(len(x))
        print "len(y): " + str(len(y))
	return [x,y]

if __name__ =="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-x', '--x_axis')
	parser.add_argument("-y", "--y_axis")
	parser.add_argument("pickele_file")
	args = parser.parse_args()

	pfx_data = load_pickele(args.pickele_file)	 
	save_figure(pfx_data, args.x_axis, args.y_axis)
