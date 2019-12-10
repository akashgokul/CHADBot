import math
import sys
import matplotlib.pyplot as plt

def calc_xy(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) 
        - math.atan2(a[1]-b[1], a[0]-b[0]))
    return -ang

def convertfrom3D(gun, cup):
    """
    gun is (x1, y1, z1)
    cup is (x2, y2, z2)

    returns (height, distance)
    """
    d = math.sqrt((gun[0] - cup[0])**2 + (gun[1] - cup[1])**2)
    h = gun[2] - cup[2]
    return h, d


def projectile(h, d, v = 3.27):
    """
    Rarams:
    h -> vertical height of arm above the target
    d -> horizontal distance to target
    v -> initial velocity of ball

    Return:
    the positive theta (launch angle of the ball)
    """
    gdv = (9.81 * d * d) / (2 * v * v)

    a = gdv
    b = -d
    c = -h + gdv

    x1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
    x2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)

    theta1, theta2 = math.atan(x1), math.atan(x2)
    if theta1 < 0:
        return theta2
    else:
        return theta1
    """
    # Plotting the curve
    i=[]
    j=[]
    for x in range(-100,100,1):
        y=(a*(x**2))+ b*x + c
        i.append(x)
        j.append(y)
    fig= plt.figure()
    axes=fig.add_subplot(111)
    axes.plot(i,j)
    plt.show()
    """


# Use this section to enter height and distance
# h = float(raw_input("Enter height in meters: "))
# d = float(raw_input("Enter distance in meters: "))

# # Use this section to enter points
# x0 = float(raw_input("gun x: "))
# y0 = float(raw_input("gun y: "))
# z0 = float(raw_input("gun z: "))
# print("")
# x1 = float(raw_input("cup x: "))
# y1 = float(raw_input("cup y: "))
# z1 = float(raw_input("cup z: "))
# h, d = convertfrom3D((x0, y0, z0), (x1, y1, z1))
# print("height: " + str(h) + "m, distance: " + "%.4g" % d + "m")

# v = 3.27 # from the spreadsheet in drive
# try:
#     theta = projectile(h, d, v)
#     print("\nLaunch angle:")
#     print("%.4g" % theta + " radians")
#     print("%.4g" % math.degrees(theta) + " degrees")
# except ValueError:
#     print("impossible to shoot the ball that far with our gun")
