from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.interpolate import LinearNDInterpolator
import sys, os
               
def plot_horn(params, save_to=None):
    
    def line(start, end, colour="blue"):
        x = [start[0], end[0]]
        y = [start[1], end[1]]
        z = [start[2], end[2]]

        ax.plot3D(x, y, z, colour)

    def rect_around_y_axis(x_len, z_len, y_loc, colour="blue"):
        line((-x_len/2, y_loc, -z_len/2), (-x_len/2, y_loc, z_len/2), colour=colour)
        line((-x_len/2, y_loc, z_len/2), (x_len/2, y_loc, z_len/2), colour=colour)
        line((x_len/2, y_loc, z_len/2), (x_len/2, y_loc, -z_len/2), colour=colour)
        line((-x_len/2, y_loc, -z_len/2), (x_len/2, y_loc, -z_len/2), colour=colour)

    def line_parallel_y_axis(x, z, y_start, length, colour="blue"):
        line((x, y_start, z), (x, y_start+length, z))

    def waveguide(_w2, _h2, y_left, y_right):
        rect_around_y_axis(_w2, _h2, y_left, colour="blue")
        rect_around_y_axis(_w2, _h2, y_right, colour="blue")
        for x in [ -_w2/2, _w2/2 ]:
            for z in [ -_h2/2, _h2/2 ]:
                line_parallel_y_axis(x, z, y_left, y_right-y_left, colour="blue")

    def flare(_w1, _h1, _w2, _h2, y_left, y_right):
        rect_around_y_axis(_w1, _h1, y_right, colour="red")
        for x_dir in [ -1, 1]:
            for z_dir in [ -1, 1]:
                line((x_dir*_w2/2, y_left, z_dir*_h2/2), (x_dir*_w1/2, y_right, z_dir*_h1/2), colour="red")

    def feed(_h2, _l2, _f0, _f1, _h3, _y_start):
        # Where is the 0 of the feed?
        # is the feed offset [ x, y ]? or [y, x]?
        # is the feedwidth in the x or y direction? or both?
        # Ignoring feedwidth and assuming offset is x, y and is in centre of l2

        feed_x = _f0
        feed_y = _y_start+_l2/2+_f1
        line((feed_x, feed_y, -_h2/2), (feed_x, feed_y, -_h2/2+_h3), colour="black")
        
        

    # Convert to lengths, widths etc. (l1, w1, ...) on the diagram at 
    # https://uk.mathworks.com/help/antenna/ref/horn.html
    l1 = params["FlareLength"]
    h1 = params["FlareHeight"]
    w1 = params["FlareWidth"]
    l2 = params["Length"]
    h2 = params["Height"]
    w2 = params["Width"]
    h3 = params["FeedHeight"]
    w3 = params["FeedWidth"]
    f0 = params["FeedOffset0"]
    f1 = params["FeedOffset1"]

    # The midpoint of the horn along the y axis is placed at y=0
    # See https://uk.mathworks.com/help/antenna/ref/horn.html for
    # orientation of axes
    y_start = -(l1+l2)/2       
    #print("y start", y_start)


    max_x_offset = max(max(w1/2, w2/2), f0)
    max_y_offset = max(abs(y_start), y_start+l2/2+f1)
    max_z_offset = max(max(h1/2, h2/2), -h2/2+h3)
    
    max_offset = max(max_x_offset, max(max_y_offset, max_z_offset))


    plt.figure(figsize=(12, 12))
    ax = plt.axes(projection='3d')
    ax.set_aspect('equal', adjustable='box')

    #ax.view_init(10, 20)

    waveguide(w2, h2, y_start, y_start+l2)
    flare(w1, h1, w2, h2, y_start+l2, y_start+l2+l1)
    feed(h2, l2, f0, f1, h3, y_start)
    

    # Make the axes all the same. Should be done better. The point is that
    # the axes have to have the same scale. If the horn is 10m long
    # and only 2m high then how to make sure that it LOOKS like that in 3d plot.
    ax.set_xlim(-max_offset, max_offset)
    ax.set_ylim(-max_offset, max_offset)
    ax.set_zlim(-max_offset, max_offset)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    if save_to is not None:
        plt.savefig(save_to)
        
def plot_beam_orig(data_file, az_file, za_file, name, log=True, normalize=False, save_to=None):
    """
    Plot a beam. The plot is the beam projected flat onto the ground when looking from above.
    Colors indicate the beam values.

    Parameters
    ----------
    data_file : matlab beam output za by az
        The beam to plot.
    az_file : matlab az file
    za_file: matlab za file
    save_to: str
        A file name to save the plot to.

    """
       
    
    az = np.deg2rad(np.loadtxt(az_file, delimiter=","))
    za = np.deg2rad(np.loadtxt(za_file, delimiter=","))  
    if za[0] != 0: 
        #print("Warning, za needs to be 0 to 180. Adjusting to HG convention")
        za = np.deg2rad(np.arange(181, dtype=int)) # Trickey going on here, setup by the Tilt so that the first row in the data is za = 0

    data = np.loadtxt(data_file, delimiter=",")
    #data = 10**(data/10)    # dB to power
    
    if normalize: data /= np.max(data)
    
    assert data.shape[0] == za.size and data.shape[1] == az.size
    
    za_coord = np.repeat(za, az.size)
    az_coord = np.tile(az, za.size)
    data = data.ravel()
    
    r = np.sin(za_coord)
    x = r*np.sin(az_coord)
    y = r*np.cos(az_coord)  

    grid_dim = 64

    # convert the x/y points to a grid location. x/y can be -1 to 1
    gi = np.round(np.interp(x, [-1, 1], [0, grid_dim-1])).astype(int)
    gj = np.round(np.interp(y, [-1, 1], [0, grid_dim-1])).astype(int)

    # Insert beam values into grid and weight
    grid = np.zeros((grid_dim, grid_dim), dtype=complex)
    np.add.at(grid, (gi, gj), data)
    weights = np.zeros((grid_dim, grid_dim))
    np.add.at(weights, (gi, gj), 1)

    grid /= weights

    #ax = plt.axes()
    #ax.remove()           # Causes problem in subplots

    plt.clf()
    if log: 
        im=plt.imshow(np.abs(grid), interpolation=None, norm=LogNorm(), cmap="rainbow")
    else:
        im=plt.imshow(np.abs(grid), interpolation="quadric", cmap="rainbow")
    plt.xticks([])
    plt.yticks([])


    if False:
        points = np.arange(0, 2*np.pi, 0.01)
        for deg in [ 30, 45, 60, 75 ]:
            r = np.cos(deg*np.pi/180)
            x = r*np.cos(points)
            y = r*np.sin(points)
            plt.text(r/np.sqrt(2), -r/np.sqrt(2), "    $"+str(deg)+"^\circ$", c="w")
            plt.scatter(x, y, s=0.01, c='w', marker='o')
    

    plt.colorbar(im,fraction=0.04, pad=0.04)
    plt.title(name, fontsize=10)

    for pos in ['right', 'top', 'bottom', 'left']: 
        plt.gca().spines[pos].set_visible(False) 
    # shape.custom3d()
    #show()
    # or just show(h2) replace with image dump

    if save_to is not None:
        plt.savefig(save_to)
        
def plot_beam(data_file, az_file, za_file, name="Beam", grid_only=False, log=True, normalize=False, interpolation="quadric", save_to=None):
    """
    Plot a beam. The plot is the beam projected flat onto the ground when looking from above.
    Colors indicate the beam values.

    Parameters
    ----------
    data_file : matlab beam output za by az
        The beam to plot.
    az_file : matlab az file
    za_file: matlab za file
    save_to: str
        A file name to save the plot to.

    """
    grid_dim = 64
    
    az = np.loadtxt(az_file, delimiter=",", dtype=int)
    za = np.loadtxt(za_file, delimiter=",", dtype=int)  

    data = np.loadtxt(data_file, delimiter=",")

    assert data.shape[0] == za.size and data.shape[1] == az.size

    za_coord = np.repeat(za, az.size)
    az_coord = np.tile(az, za.size)
    data = data.ravel()


    # Cut some things where 360 goes to 0
    data = data[(az_coord<360) & (za_coord<=90)]
    _za_coord = za_coord[(az_coord<360) & (za_coord<=90)]
    az_coord = az_coord[(az_coord<360) & (za_coord<=90)]
    za_coord = _za_coord


    za_coord = np.deg2rad(za_coord)
    az_coord = np.deg2rad(az_coord)
    r = np.sin(za_coord)
    x = r*np.sin(az_coord)
    y = r*np.cos(az_coord)  

    X = np.linspace(-1, 1, num=grid_dim)
    Y = np.linspace(-1, 1, num=grid_dim)

    X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation
    interp = LinearNDInterpolator(list(zip(x, y)), data)

    grid = interp(X, Y).T   

    if normalize: grid /= np.nanmax(grid)

    if grid_only: return grid

    plt.clf()
    if log: 
        im=plt.imshow(grid, interpolation=interpolation, norm=LogNorm(), cmap="rainbow")
    else:
        im=plt.imshow(grid, interpolation=interpolation, cmap="rainbow")
    plt.xticks([])
    plt.yticks([])


    if False:
        points = np.arange(0, 2*np.pi, 0.01)
        for deg in [ 30, 45, 60, 75 ]:
            r = np.cos(deg*np.pi/180)
            x = r*np.cos(points)
            y = r*np.sin(points)
            plt.text(r/np.sqrt(2), -r/np.sqrt(2), "    $"+str(deg)+"^\circ$", c="w")
            plt.scatter(x, y, s=0.01, c='w', marker='o')
    

    plt.colorbar(im,fraction=0.04, pad=0.04)
    plt.title(name, fontsize=10)

    for pos in ['right', 'top', 'bottom', 'left']: 
        plt.gca().spines[pos].set_visible(False) 
    # shape.custom3d()
    #show()
    # or just show(h2) replace with image dump

    if save_to is not None:
        plt.savefig(save_to)

        
def plot_beam_grid(data_file, az_file, za_file, name, log=True, vmin=None, save_to=None):
    """
    az by za
    """
    az = np.loadtxt(az_file, delimiter=",", dtype=int)
    za = np.loadtxt(za_file, delimiter=",", dtype=int)  
    if za[0] != 0: 
        print("Warning, za needs to be 0 to 180. Adjusting to HG convention")
        za = np.arange(181, dtype=int) # Trickey going on here, setup by the Tilt so that the first row in the data is za = 0 regardless of what el says

    data = np.loadtxt(data_file, delimiter=",")
    data = 10**(data/10)    # dB to power
    
    assert data.shape[0] == za.size and data.shape[1] == az.size

    if vmin is not None:
        data = np.where(data<vmin, vmin, data)

    if log:
        plt.imshow(data.T, extent=[np.min(za), np.max(za), np.max(az), np.min(az)], 
                   norm=LogNorm())
    else:
        plt.imshow(data.T, extent=[np.min(za), np.max(za), np.max(az), np.min(az)], 
                   )
    plt.ylabel("az [deg]")
    plt.xlabel("za [deg]")
    plt.title("Power")
    plt.colorbar()

    plt.savefig(name)
        
def plot_beam_cst(pattern_file, name, log=True, save_to=None):
    """
    Plot a beam. The plot is the beam projected flat onto the ground when looking from above.
    Colors indicate the beam values.


    """
    
    cst = np.loadtxt(pattern_file, skiprows=2)
    data = 10**(cst[:, 2]/10)    # from dB
    
    az = cst[:, 0]
    el = cst[:, 1]
    
    data = data[el>0]
    az = az[el>0]
    el = el[el>0]
    
    peak_i = np.argmax(data)
    print("Max at az=", az[peak_i], "el=", el[peak_i])
    min_i = np.argmin(data)
    print("Min at az=", az[min_i], "el=", el[min_i])
    
    az = np.deg2rad(az)
    el = np.deg2rad(el)
    
    r = np.cos(el)
    x = r*np.sin(az)
    y = r*np.cos(az)  

    grid_dim = 64

    # convert the x/y points to a grid location. x/y can be -1 to 1
    gi = np.round(np.interp(x, [-1, 1], [0, grid_dim-1])).astype(int)
    gj = np.round(np.interp(y, [-1, 1], [0, grid_dim-1])).astype(int)

    # Insert beam values into grid and weight
    grid = np.zeros((grid_dim, grid_dim), dtype=complex)
    np.add.at(grid, (gi, gj), data)
    weights = np.zeros((grid_dim, grid_dim))
    np.add.at(weights, (gi, gj), 1)

    grid /= weights

    #ax = plt.axes()
    #ax.remove()           # Causes problem in subplots

    plt.clf()
    if log: 
        im=plt.imshow(np.abs(grid), interpolation="quadric", norm=LogNorm(), cmap="rainbow")
    else:
        im=plt.imshow(np.abs(grid), interpolation="quadric", cmap="rainbow")
    plt.xticks([])
    plt.yticks([])


    if False:
        points = np.arange(0, 2*np.pi, 0.01)
        for deg in [ 30, 45, 60, 75 ]:
            r = np.cos(deg*np.pi/180)
            x = r*np.cos(points)
            y = r*np.sin(points)
            plt.text(r/np.sqrt(2), -r/np.sqrt(2), "    $"+str(deg)+"^\circ$", c="w")
            plt.scatter(x, y, s=0.01, c='w', marker='o')
    

    plt.colorbar(im,fraction=0.04, pad=0.04)
    plt.title(name)

    for pos in ['right', 'top', 'bottom', 'left']: 
        plt.gca().spines[pos].set_visible(False) 
    # shape.custom3d()
    #show()
    # or just show(h2) replace with image dump

    if save_to is not None:
        plt.savefig(save_to)
        
def plot_beam_grid_cst(pattern_file, name, log=True, save_to=None):
    cst = np.loadtxt(pattern_file, skiprows=2)
    data = 10**(cst[:, 2]/10)    # from dB
    
    az = cst[:, 0].astype(int)
    el = cst[:, 1].astype(int)
    
    # az goes from -180 to 179. el goes from -90 to 90 
    
    grid = np.zeros((360, 181))
    for i in range(az.size):
        grid[az[i]+180, el[i]+90] = data[i]
 
    plt.matshow(grid, extent=[-90, 91, -180, 180])
    plt.ylabel("Theta [deg]")
    plt.xlabel("Phi [deg]")
    plt.title("Power")
    plt.savefig(name)

if __name__ == "__main__":
    dat_file = sys.argv[1]
    az_file = dat_file[:-4]+"_az.dat"
    za_file = dat_file[:-4]+"_za.dat"

    plot_file = dat_file.replace("dat_files", "plot_files")[:-4]
    print(plot_file+".png")
    #print(dat_file, az_file, za_file, plot_file)

    plot_beam(dat_file, az_file, za_file, os.path.basename(plot_file), interpolation="None", normalize=True, save_to=plot_file)
    #plot_beam_orig("/users/PAS1960/hughgarsden/matlab_beams/matlab_horn_351MHz_rot.dat", "/users/PAS1960/hughgarsden//matlab_beams/matlab_horn_351MHz_rot_az.dat", "/users/PAS1960/hughgarsden/matlab_beams/matlab_horn_351MHz_rot_za.dat", "test",save_to="x")
     
