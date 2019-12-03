import sys
import time
import multiprocessing as mp
import numpy as np
import pickle
#Add the src directory with OTR Sim Modules to path:
sys.path.append('Modules/')
sys.path.append('include/')
#OTR Simulation Modules in src:
import Foil, Mirror, Camera, Log, Ray
from GetRay import GetRay
#OTR components, i.e. beam, mirrors, foil, etc...
import config
from config import VERBOSE, nrays

if __name__ == "__main__":
    #Set the log file if VERBOSE
    log = Log.LogFile(VERBOSE)
    #if VERBOSE: log = open(VERBOSE, 'w')
    #else: log = None
    log.Log('Starting pyOTR', True)
    nCPUs = mp.cpu_count()

    #Configure the OTR System:
    log.Log('\nSetting OTR Configuration:', True)

    #Set the Beam Properties:   
    beam = config.beam
    log.Log('Beam at {0} {1}'.format(beam['x'], beam['y']))

    #Set the Light Properties:          
    light = config.light_source
    log.Log('Light Source: {0} = {1}'.format(light, config.light[light]) )

    #Set the OTR Foil in the Foil Disk:                          
    foil = Foil.Foil(ID=config.foil['ID'], normal=config.foil['normal'], diam=config.foil['diam'])
    log.Log('Foil ID: {0} = {1}'.format(foil.GetID(), foil.GetType()))
    calib = Foil.CalibrationFoil(normal=config.foil['normal'], diam=config.foil['diam'])    

    nrays = 100000
    nbins = 45
    xmin, xmax = -27., 27.

    t0 = time.time()
    rays = []
    vs = []
    rays_through = []
    for i in range(nrays):
        #x = np.random.normal(0., 3.)
        #y = np.random.normal(0., 3.)
        x = xmax*np.random.uniform(-1., 1.)
        y = xmax*np.random.uniform(-1., 1.)
        z = -1.
        iray = Ray.Ray(X=np.array([x, y, z]), V=np.array([0., 0., 1.]))
        calib.RayTransport(iray)
        x = iray.GetPosition()
        v = iray.GetDirection()
        rays.append(x)
        vs.append(v)

    rays = np.array(rays)
    vs = np.array(vs)
    #rays_through = np.array(rays_through)

    print('time for {}: {:.2f} s'.format(nrays, time.time() - t0))

    from ROOT import TCanvas, TH2F, gStyle
    img = TH2F('img', '', nbins, xmin, xmax, nbins, xmin, xmax)
    img2 = TH2F('img2', '', nbins, xmin, xmax, nbins, xmin, xmax)
    img3 = TH2F('img3', '', nbins, xmin, xmax, nbins, xmin, xmax)
    for iray, iv in zip(rays, vs):
        img.Fill(iray[0], iray[1])
        if iv[2] > 0: img2.Fill(iray[0], iray[1]) 
        else: img3.Fill(iray[0], iray[1])
    #for iray in rays_through: img3.Fill(iray[0], iray[1])
    c0 = TCanvas('c1', 'c1', 700, 800)
    gStyle.SetOptStat(0)
    img.Draw('colz')
    c0.SaveAs('img.png')
    img2.Draw('colz')
    c0.SaveAs('img2.png')
    img3.Draw('colz')
    c0.SaveAs('img3.png')

    '''
    start_time = time.time()     
    queue = mp.Queue() 
    #procs = [mp.Process(target=GetRay, args=(queue, beam, light, otr_components,)) for x in xrange(nrays)]
    procs = [mp.Process(target=GetRay, args=(queue, calib)) for x in range(nrays)]
    for p in procs: p.start()                                             
    for p in procs: p.join()                                                                          
    rays = np.array([queue.get() for p in procs]) 
    print('parallel time for {}: {:.2f} s'.format(nrays, time.time() - start_time))
    
    img = TH2F('img3', '', 30, -15., 15, 30, -15., 15.)
    img2 = TH2F('img4', '', 30, -15., 15, 30, -15., 15.)
    for iray in rays:
        img.Fill(iray[0], iray[1])
        if iray[2] > 0: img2.Fill(iray[0], iray[1])
    c0 = TCanvas('c0', 'c0', 700, 800)
    img.Draw('colz')
    c0.SaveAs('img3.png')
    img2.Draw('colz')
    c0.SaveAs('img4.png')
    '''
    '''
    #Set the Configuration of the Mirrors:
    use_mirrors = config.mirrors
    mirrors = [Mirror.Mirror(x=imirror['x'], y=imirror['y'], fdist=imirror['f']) for imirror in use_mirrors]
    log.Log('Number of mirrors: {0}'.format(len(mirrors)))
    m_message = '{0} cm with focal length = {1}'
    for imirror in mirrors: log.Log(m_message.format(imirror.GetPosition(), imirror.GetDistance()) )

    #Set the OTR Camera Design:
    camera = Camera.Camera(npxlX=config.camera['npxlX'],
                           npxlY=config.camera['npxlY'],
                           fdist=config.camera['focal distance'])
    cam_message = 'Camera size: {0} pixels at {1} cm from mirror.'
    log.Log(cam_message.format(camera.GetPixels(), camera.GetDistance()))
    
    #Add all the components to pass to the main function
    log.Log('\nPreparing OTR components.')
    otr_components = [foil, mirrors, camera]

    otr_components = [foil] 

    #Run the main function called 'GetRay' for each light ray.
    log.Log('\nUsing {0} CPUs to parallelize ray tracing.'.format(nCPUs), True)
    start_time = time.time()
    queue = mp.Queue()
    procs = [mp.Process(target=GetRay, args=(queue, beam, light, otr_components,)) for x in xrange(nrays)]
    for p in procs: p.start()
    for p in procs: p.join()
    rays = np.array([queue.get() for p in procs])
    log.Log('Time to trace {0} rays = {1:.2f} s'.format(nrays, (time.time() - start_time)), True)

    #Save the light rays list to a pickle file that can be read in the script 'macro/PickleToROOT.py'
    pickle.dump( rays, open( 'outputs/rays.p', 'wb') )

    log.Log('\nExiting pyOTR.', True)
    '''
