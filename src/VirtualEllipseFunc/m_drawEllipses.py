import numpy as np 
import matplotlib.pyplot as plt
from math import atan2, pi
from matplotlib.patches import Ellipse
from scipy.spatial import distance


def drawEllipses (e_posi, posi, ka, kb, crowding_cons, newWindowSize, loop_number, direction = 'radial', ellipseColor_r = 'orangered', ellipseColor_t = 'lime', ellipsetransp = 0.5):
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)
    eccentricities2 = []
    for i in range(len(posi)):
        eccentricities0 = distance.euclidean(posi[i], (0,0))
        eccentricities2.append(eccentricities0)
    #radial
    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi
        angle_deg.append(angle_deg0)
    angle_deg3 = []
    for ang in range(len(posi)):
        angle_rad0s = atan2(posi[ang][1],posi[ang][0])
        angle_deg0s = angle_rad0s*180/pi
        angle_deg3.append(angle_deg0s)
    # #tangential
    # angle_deg2 = []
    # for ang in range(len(e_posi)):
    #     angle_rad0_2 = atan2(e_posi[ang][1],e_posi[ang][0])
    #     angle_deg0_2 = angle_rad0_2*180/pi + 90
    #     angle_deg2.append(angle_deg0_2)
        
    my_e = [Ellipse(xy=posi[j], width=eccentricities2[j]*ka*2, height=eccentricities2[j]*kb*2, angle = angle_deg3[j])
            for j in range(len(posi))]
    my_e2 = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j]+90)
            for j in range(len(e_posi))]

    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    if direction == 'radial':
        for e in my_e:
            ax.add_artist(e)
            #random color?
            e.set_clip_box(ax.bbox)
            # e.set_alpha(np.random.rand())
            e.set_alpha(ellipsetransp)
            # e.set_facecolor(np.random.rand(3))
            #change face color here
            e.set_facecolor(ellipseColor_r)
            # e.set_facecolor('lime')

    elif direction == 'tangential':
        for e in my_e2:
            ax.add_artist(e)
            #random color?
            e.set_clip_box(ax.bbox)
            # e.set_alpha(np.random.rand())
            e.set_alpha(ellipsetransp)
            #change face color here
            e.set_facecolor(ellipseColor_t)
    else:
        for e in my_e:
            ax.add_artist(e)
            #random color?
            e.set_clip_box(ax.bbox)
            # e.set_alpha(np.random.rand())
            e.set_alpha(ellipsetransp)
            e.set_facecolor(np.random.rand(3))
            #change face color here
            e.set_facecolor(ellipseColor_r)
            # e.set_facecolor('lime')

        for e in my_e2:
            ax.add_artist(e)
            #random color?
            e.set_clip_box(ax.bbox)
            # e.set_alpha(np.random.rand())
            e.set_alpha(ellipsetransp)
            e.set_facecolor(np.random.rand(3))
            #change face color here
            e.set_facecolor(ellipseColor_t)

    ax.set_xlim([-800, 800]) #TODO
    ax.set_ylim([-500, 500]) #TODO
    # ax.set_title('c_%s_wS_%s_eS_%s_%s_E.png' %(crowding_cons,newWindowSize,ka,kb))

    #边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    #坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_c_%s_wS_%s_eS_%s_%s_%s_E.png' %(loop_number,crowding_cons,newWindowSize,ka,kb,len(e_posi)))


def drawEllipse (e_posi, ka, kb, crowding_cons, newWindowSize, loop_number): 
    """
    This function allows to draw more than one ellipse. The parameter is 
    a list of coordinate (must contain at least two coordinates)
    The direction of ellipses are only radial direction,
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)

    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi
        angle_deg.append(angle_deg0)
#    https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.patches.Ellipse.html
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j],color='red',fill=None)#color='red',fill=None
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        # e.set_alpha(np.random.rand())
        # e.set_facecolor(np.random.rand(3))
    # ax.set_xlim([-800, 800])
    # ax.set_ylim([-500, 500])
    ax.set_xlim([-400, 400])
    ax.set_ylim([-250, 250])
    # ax.set_title('c_%s_wS_%s_eS_%s_%s_E_%s.png' %(crowding_cons,newWindowSize,ka,kb,len(e_posi)))
    
    #边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    #坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_c_%s_wS_%s_eS_%s_%s_E_%s.png' %(loop_number,crowding_cons,newWindowSize,ka,kb,len(e_posi)))

# # call the function
# eposi = [(-90.0, -60.0), (140.0, 110.0), (-110.0, 150.0), (-140.0, -160.0), (130.0, -20.0), (200.0, 10.0), (200.0, -100.0), (120.0, 180.0), (-230.0, -50.0), (-200.0, 50.0), (-40.0, -140.0), (-220.0, 170.0), (-190.0, 0.0), (140.0, -130.0), (10.0, 120.0), (-100.0, 90.0), (60.0, 160.0), (30.0, 100.0), (-110.0, -10.0), (70.0, -160.0), (220.0, -50.0), (-160.0, -80.0), (250.0, -180.0), (-60.0, 170.0), (70.0, -80.0), (210.0, 110.0), (0.0, -120.0), (-90.0, -170.0), (-20.0, 130.0), (130.0, 50.0), (-160.0, 90.0), (100.0, -60.0), (-70.0, -80.0), (120.0, 10.0), (100.0, -140.0), (-240.0, -180.0), (50.0, 90.0), (80.0, 70.0), (30.0, -140.0), (-100.0, 40.0), (-110.0, -40.0), (-40.0, 100.0), (220.0, 60.0), (-50.0, -90.0), (-120.0, 20.0), (-60.0, 80.0), (50.0, -90.0)]
# drawEllipse(e_posi = eposi, ka = 0.25, kb = 0.1, crowding_cons = 0, newWindowSize= 0.5, loop_number=1)
# for posi in eposi:
#     plt.plot(posi[0],posi[1],'ko')
# ex = plt.gca()
# ex.set_xlim([-400, 400])
# ex.set_ylim([-250, 250])

# # 边框不可见
# ex.spines['top'].set_visible(False)
# ex.spines['right'].set_visible(False)
# ex.spines['bottom'].set_visible(False)
# ex.spines['left'].set_visible(False)
# #坐标不可见
# ex.axes.get_yaxis().set_visible(False)
# ex.axes.get_xaxis().set_visible(False)

# # plt.show()
# # plt.savefig('dots.png')
# # call the function
# eposi = [(-90.0, -60.0), (140.0, 110.0), (-110.0, 150.0), (-140.0, -160.0)]

def drawProcess(e_posi, ka, kb, crowding_cons, newWindowSize, loop_number):
    curr_eposi = []
    for i_eposi in eposi:
        curr_eposi.append(i_eposi)
        drawEllipse(e_posi = curr_eposi, ka = 0.25, kb = 0.1, crowding_cons = 0, newWindowSize= 0.5, loop_number=1)

# drawProcess(e_posi = eposi, ka = 0.25, kb = 0.1, crowding_cons = 0, newWindowSize= 0.5, loop_number=1)

def drawEllipseT (e_posi, ka, kb, crowding_cons, newWindowSize, loop_number): 
    """
    This function allows to draw more than one ellipse. The parameter is 
    a list of coordinate (must contain at least two coordinates)
    The direction of ellipses are only radial direction,
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)

    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi + 90
        angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j]+90)
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
    ax.set_xlim([-800, 800]) #TODO
    ax.set_ylim([-500, 500]) #TODO
    ax.set_title('c_%s_wS_%s_eS_%s_%s_E.png' %(crowding_cons,newWindowSize,ka,kb))
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_c_%s_wS_%s_eS_%s_%s_E.png' %(loop_number,crowding_cons,newWindowSize,ka,kb))

def drawEllipse_full(e_posi, extra_posi, ka, kb):
        """
        This function allows to draw more than one ellipse. The parameter is 
        a list of coordinate (must contain at least two coordinates)
        The radial and tangential ellipses for the same coordinates are drawn.
        """
        eccentricities = []
        for i in range(len(e_posi)):
            eccentricities0 = distance.euclidean(e_posi[i], (0,0))
            eccentricities.append(eccentricities0)
        #radial
        angle_deg = []
        for ang in range(len(e_posi)):
            angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
            angle_deg0 = angle_rad0*180/pi
            angle_deg.append(angle_deg0)
        my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j])
                for j in range(len(e_posi))]
        
        #tangential
        angle_deg2 = []
        for ang in range(len(e_posi)):
            angle_rad0_2 = atan2(e_posi[ang][1],e_posi[ang][0])
            angle_deg0_2 = angle_rad0_2*180/pi + 90
            angle_deg2.append(angle_deg0_2)
        my_e2 = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j]+90)
                for j in range(len(e_posi))]
        
        fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
        for e in my_e:
            ax.add_artist(e)
            e.set_clip_box(ax.bbox)
            e.set_alpha(np.random.rand())
            e.set_facecolor(np.random.rand(3))
        for e2 in my_e2:
            ax.add_artist(e2)
            e2.set_clip_box(ax.bbox)
            e2.set_alpha(np.random.rand())
            e2.set_facecolor(np.random.rand(3))
        
        #show the discs on the ellipses-flower
        for dot in e_posi:
            plt.plot(dot[0],dot[1], color = 'k', marker ='o')
        # plt.show()
        for dot1 in extra_posi:
            plt.plot(dot1[0],dot1[1],color = 'r', marker = 'o')
        # plt.show()
        # ax.set_xlim([-800, 800])
        # ax.set_ylim([-500, 500])
        ax.set_xlim([-400, 400])
        ax.set_ylim([-260, 260])
        # ax.set_title('wS_%s_eS_%s_%s_E.png' %(newWindowSize,ka,kb))
        
        #边框不可见
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        #坐标不可见
        ax.axes.get_yaxis().set_visible(False)
        ax.axes.get_xaxis().set_visible(False)
        plt.show()
        
        try:
            loop_number
        except NameError:
            var_exists = False
        else:
            var_exists = True
            # plt.savefig('%s_wS_%s_eS_%s_%s_E.png' %(loop_number,newWindowSize,ka,kb))
