import numpy as np
import flapjack
from flapjack import Flapjack
import sys

def step(p, signal1, signal2, growth_rate, dt):
    '''
    Update protein levels p according to signal
    '''
    phi1 = growth_rate * signal1**2 / (1 + signal1**2)
    phi2 = growth_rate * signal2**2 / (1 + signal2**2)
    dpdt = phi1 + phi2 - growth_rate * p
    return p + dpdt*dt

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
    study_name = 'Inducible promoter simulation'
    study = fj.get('study', name=study_name)
    if len(study)==0:
        study = fj.create('study', 
                            name=study_name, 
                            description='Simulation of inducible gene expression'
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
    dna = fj.get('dna', name='pSIM1')
    if len(dna)==0:
        dna = fj.create('dna', name='pSIM1')
    vector = fj.get('vector', name='pSIM1')
    if len(vector)==0:
        vector = fj.create('vector', name='pSIM1', dnas=[dna.id[0]])

    # Get or create the chemicals
    chemical1 = fj.get('chemical', name='A')
    if len(chemical1)==0:
        chemical1 = fj.create('chemical', name='A', description='Simulated inducer')
    chemical2 = fj.get('chemical', name='B')
    if len(chemical2)==0:
        chemical2 = fj.create('chemical', name='B', description='Simulated inducer')

    # Get or create the signals
    signal = fj.get('signal', name='SFP')
    if len(signal)==0:
        signal = fj.create('signal', name='SFP', color='green', description='Simulated fluorescent protein')
    od = fj.get('signal', name='SOD')
    if len(od)==0:
        od = fj.create('signal', name='SOD', color='black', description='Simulated OD')

    # Create the samples
    # Loop over inducer 1
    for i in range(12):
        # Inducer A concentration
        conc1 = 10**(i/2-3)
        # Create supplement for inducer A
        supplement1 = fj.get('supplement', chemical=chemical1.id[0], concentration=conc1)
        if len(supplement1)==0:
            supp_name = chemical1.name[0] + f' {conc1}'
            supplement1 = fj.create('supplement', name=supp_name, chemical=chemical1.id[0], concentration=conc1)
        # Loop over inducer 2
        for j in range(12):
            # Inducer B concentration
            conc2 = 10**(j/2-3)
            # See if a supplement already exists
            supplement2 = fj.get('supplement', chemical=chemical2.id[0], concentration=conc2)
            if len(supplement2)==0:
                supp_name = chemical2.name[0] + f' {conc2}'
                supplement2 = fj.create('supplement', name=supp_name, chemical=chemical2.id[0], concentration=conc2)
            # Create a new sample
            supplements = [supplement1.id[0], supplement2.id[0]]
            sample = fj.create('sample',
                            row=i, col=j,
                            media=media.id[0],
                            strain=strain.id[0],
                            vector=vector.id[0],
                            assay=assay.id[0],
                            )
            # Add the supplements to the sample
            fj.patch('sample', sample.id[0], supplements=supplements)
            # Create the measurements for this sample
            dt = 24/100
            p = 0
            for t in range(100):
                growth_rate = flapjack.gompertz_growth_rate(t*dt, 0.01, 1, 1, 4)
                odval = flapjack.gompertz(t*dt, 0.01, 1, 1, 4)
                measurement = fj.create('measurement', 
                                        signal=signal.id[0], 
                                        time=t * dt, 
                                        value=p * odval, 
                                        sample=sample.id[0])
                od_measurement = fj.create('measurement',
                                        signal=od.id[0], 
                                        time=t*dt, 
                                        value=odval, 
                                        sample=sample.id[0])
                p = step(p, conc1, conc2, growth_rate, dt)
        
if __name__=='__main__':
    main(sys.argv)