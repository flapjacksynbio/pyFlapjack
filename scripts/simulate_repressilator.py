import numpy as np
import flapjack
from flapjack import Flapjack
import sys

alpha = 1e2
gamma = 2

def step(p, growth_rate, dt):
    '''
    Update protein levels p according to signal
    '''
    p1,p2,p3 = p
    dp1dt = alpha / (1 + p3*p3) - gamma * p1 - growth_rate * p1
    dp2dt = alpha / (1 + p1*p1) - gamma * p2 - growth_rate * p2
    dp3dt = alpha / (1 + p2*p2) - gamma * p3 - growth_rate * p3
    p[0] += dp1dt * dt
    p[1] += dp2dt * dt
    p[2] += dp3dt * dt
    return p

def main(argv):
    if len(argv)<3:
        print('''
        Usage:
            python simulate.py "<Assay name>" "<Description>"
        ''')
        return
    assay_name = argv[1]
    assay_description = argv[2]

    # Make connection to Flapjack
    fj = Flapjack(url_base='localhost:8000')
    fj.log_in(username='tim', password='chicken')

    # Create a new study or re-use existing study
    study_name = 'Repressilator simulation'
    study = fj.get('study', name=study_name)
    if len(study)==0:
        study = fj.create('study', 
                            name=study_name, 
                            description='Simulation of repressilator'
                            )

    # Add a new assay
    assay = fj.create('assay', 
                        name=assay_name,
                        description=assay_description,
                        machine='Simulator',
                        temperature=37,
                        study=study.id[0]
                        )

    # Get or create a media and strain
    media = fj.get('media', name='Simulated media')
    if len(media)==0:
        media = fj.create('media', name='Simulated media', description='Gompertz growth model')
    strain = fj.get('strain', name='Simulated strain')
    if len(strain)==0:
        strain = fj.create('strain', name='Simulated strain', description='Gompertz growth model')

    # Get or create the DNA and vector
    dna = fj.get('dna', name='pSREP')
    if len(dna)==0:
        dna = fj.create('dna', name='pREP1')
    vector = fj.get('vector', name='pREP1')
    if len(vector)==0:
        vector = fj.create('vector', name='pREP1', dnas=[dna.id[0]])

    # Get or create the signals
    signal1 = fj.get('signal', name='SFP1')
    if len(signal1)==0:
        signal1 = fj.create('signal', name='SFP1', color='red', description='Simulated fluorescent protein')
    signal2 = fj.get('signal', name='SFP2')
    if len(signal2)==0:
        signal2 = fj.create('signal', name='SFP2', color='green', description='Simulated fluorescent protein')
    signal3 = fj.get('signal', name='SFP3')
    if len(signal3)==0:
        signal3 = fj.create('signal', name='SFP3', color='blue', description='Simulated fluorescent protein')
    od = fj.get('signal', name='SOD')
    if len(od)==0:
        od = fj.create('signal', name='SOD', color='black', description='Simulated OD')

    # Create the samples
    for i in range(1):
        # Create a new sample
        sample = fj.create('sample',
                        row=1, col=i,
                        media=media.id[0],
                        strain=strain.id[0],
                        vector=vector.id[0],
                        assay=assay.id[0],
                        )
        # Create the measurements for this sample
        dt = 24/100
        p = np.array([0, 5, 0])
        for t in range(100):
            growth_rate = flapjack.gompertz_growth_rate(t*dt, 0.01, 1, 1, 4)
            odval = flapjack.gompertz(t*dt, 0.01, 1, 1, 4)
            measurement = fj.create('measurement', 
                                    signal=signal1.id[0], 
                                    time=t * dt, 
                                    value=p[0] * odval, 
                                    sample=sample.id[0])
            measurement = fj.create('measurement', 
                                    signal=signal2.id[0], 
                                    time=t * dt, 
                                    value=p[1] * odval, 
                                    sample=sample.id[0])
            measurement = fj.create('measurement', 
                                    signal=signal3.id[0], 
                                    time=t * dt, 
                                    value=p[2] * odval, 
                                    sample=sample.id[0])
            od_measurement = fj.create('measurement',
                                    signal=od.id[0], 
                                    time=t*dt, 
                                    value=odval, 
                                    sample=sample.id[0])
            p = step(p, growth_rate, dt)

if __name__=='__main__':
    main(sys.argv)