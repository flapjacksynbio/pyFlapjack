import numpy as np
import flapjack
from flapjack import Flapjack
import sys

def step(p, signal, dt):
    '''
    Update protein levels p according to signal
    '''
    dpdt = signal**2 / (1 + signal**2) - p
    return p + dpdt*dt

if __name__=='__main__':
    if len(sys.argv)<2:
        return
    assay_name = sys.argv[1]

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
                        description='First replicate for testing',
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
        dna = fj.create('dna', name='pSIM1', assays=[assay.id[0]])
    vector = fj.get('vector', name='pSIM1')
    if len(vector)==0:
        vector = fj.create('vector', name='pSIM1', dnas=[dna.id[0]])

    # Get or create the chemical and supplement
    chemical = fj.get('chemical', name='A')
    if len(chemical)==0:
        chemical = fj.create('chemical', name='A', description='Simulated inducer')

    # Get or create the signals
    signal = fj.get('signal', name='SFP')
    if len(signal)==0:
        signal = fj.create('signal', name='SFP', color='green', description='Simulated fluorescent protein')
    od = fj.get('signal', name='SOD')
    if len(od)==0:
        od = fj.create('signal', name='SOD', color='black', description='Simulated OD')

    # Create the samples
    for i in range(12):
        # Inducer concentration
        conc = 10**(i/2-3)
        # See if a supplement already exists
        supplement = fj.get('supplement', chemical=chemical.id[0], concentration=conc)
        if len(supplement)==0:
            supp_name = chemical.name[0] + f' {conc}'
            supplement = fj.create('supplement', name=supp_name, chemical=chemical.id[0], concentration=conc)
        # Create a new sample
        sample = fj.create('sample',
                        row='A', col=1,
                        media=media.id[0],
                        strain=media.id[0],
                        vector=media.id[0],
                        assay=assay.id[0],
                        supplements=[supplement.id[0]]
                        )
        # Create the measurements for this sample
        dt = 25/100
        p = 0
        for t in range(100):
            p = step(p, conc, dt)
            measurement = fj.create('measurement', signal=signal.id[0], time=t*dt, value=p, sample=sample.id[0])
            odval = flapjack.gompertz(t, 0.01, 1, 1, 4)
            od_measurement = fj.create('measurement', signal=od.id[0], time=t*dt, value=odval, sample=sample.id[0])
        