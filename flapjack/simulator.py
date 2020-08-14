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

class Simulator:
    def __init__(
        self,
        study_name='',
        assay_name='', 
        study_description='',
        assay_description='',
        dna_name='',
        signal_names=[],
        signal_colors=[]
        ):
        self.assay_name = assay_name
        self.assay_description = assay_description
        self.study_name = study_name
        self.study_description = study_description
        self.dna_name = dna_name,
        self.signal_names = signal_names
        self.signal_colors = signal_colors

    def create_meta_objects(self, fj):
        # Create a new study or re-use existing study
        self.study = fj.get('study', name=self.study_name)
        if len(study)==0:
            self.study = fj.create('study', 
                                name=self.study_name, 
                                description=self.study_description
                                )

        # Add a new assay
        self.assay = fj.create('assay', 
                            name=self.assay_name,
                            description=self.assay_description,
                            machine='Simulator',
                            temperature=0,
                            study=self.study.id[0]
                            )

        # Get or create a media and strain
        self.media = fj.get('media', name='Simulated media')
        if len(self.media)==0:
            self.media = fj.create('media', name='Simulated media', description='Gompertz growth model')
        self.strain = fj.get('strain', name='Simulated strain')
        if len(self.strain)==0:
            self.strain = fj.create('strain', name='Simulated strain', description='Gompertz growth model')

        # Get or create the DNA and vector
        self.dna = fj.get('dna', self.dna_name)
        if len(self.dna)==0:
            self.dna = fj.create('dna', name=self.dna_name)
        self.vector = fj.get('vector', name=self.dna_name)
        if len(self.vector)==0:
            self.vector = fj.create('vector', name=self.dna_name, dnas=[dna.id[0]])

        # Get or create the signals
        self.signals = []
        for s,name in enumerate(signal_names):
            self.signal[s] = fj.get('signal', name=self.signal_names[s])
            if len(self.signal[s])==0:
                self.signals[s] = fj.create('signal', name=self.signal_names[s], color=self.signal_colors[s], description='Simulated signal')
        self.od = fj.get('signal', name='SOD')
        if len(self.od)==0:
            self.od = fj.create('signal', name='SOD', color='black', description='Simulated OD')

    def create_data(self, step, n_samples, nt, dt):
        # Create the samples
        for i in range(n_samples):
            # Create a new sample
            sample = fj.create('sample',
                            row=1, col=i,
                            media=self.media.id[0],
                            strain=self.strain.id[0],
                            vector=self.vector.id[0],
                            assay=self.assay.id[0],
                            )
            # Create the measurements for this sample
            p = self.init_proteins
            for t in range(nt):
                growth_rate = flapjack.gompertz_growth_rate(t*dt, 0.01, 1, 1, 4)
                odval = flapjack.gompertz(t*dt, 0.01, 1, 1, 4)
                measurement = fj.create('measurement', 
                                        signal=signal1.id[0], 
                                        time=t * dt, 
                                        value=p[0] * odval + np.random.normal(scale=5/3), 
                                        sample=sample.id[0])
                measurement = fj.create('measurement', 
                                        signal=signal2.id[0], 
                                        time=t * dt, 
                                        value=p[1] * odval + np.random.normal(scale=5/3), 
                                        sample=sample.id[0])
                measurement = fj.create('measurement', 
                                        signal=signal3.id[0], 
                                        time=t * dt, 
                                        value=p[2] * odval + np.random.normal(scale=5/3), 
                                        sample=sample.id[0])
                od_measurement = fj.create('measurement',
                                        signal=od.id[0], 
                                        time=t*dt, 
                                        value=odval + np.random.normal(scale=0.05), 
                                        sample=sample.id[0])
                p = step(p, growth_rate, dt)
