import numpy as np
import flapjack
from flapjack import Flapjack
import sys

class Simulator:
    def __init__(
        self,
        study_name='',
        assay_name='', 
        study_description='',
        assay_description='',
        dna_name='',
        ):
        self.assay_name = assay_name
        self.assay_description = assay_description
        self.study_name = study_name
        self.study_description = study_description
        self.dna_name = dna_name

    def create_meta_objects(self, fj):
        # Create a new study or re-use existing study
        self.study = fj.get('study', name=self.study_name)
        if len(self.study)==0:
            self.study = fj.create('study', 
                                name=self.study_name, 
                                description=self.study_description
                                )

        # Get or create a media and strain
        self.media = fj.get('media', name='Simulated media')
        if len(self.media)==0:
            self.media = fj.create('media', name='Simulated media', description='Gompertz growth model')
        self.strain = fj.get('strain', name='Simulated strain')
        if len(self.strain)==0:
            self.strain = fj.create('strain', name='Simulated strain', description='Gompertz growth model')

        # Get or create the DNA and vector
        self.dna = fj.get('dna', name=self.dna_name)
        if len(self.dna)==0:
            self.dna = fj.create('dna', name=self.dna_name)
        self.vector = fj.get('vector', name=self.dna_name)
        if len(self.vector)==0:
            self.vector = fj.create('vector', name=self.dna_name, dnas=[self.dna.id[0]])

        # Get or create the signals
        self.signal = fj.get('signal', name='SFP')
        if len(self.signal)==0:
            self.signal = fj.create('signal', name='SFP', color='green', description='Simulated signal')
        self.od = fj.get('signal', name='SOD')
        if len(self.od)==0:
            self.od = fj.create('signal', name='SOD', color='black', description='Simulated OD')

        # Get or create the chemical and supplement
        self.chemical = fj.get('chemical', name='A')
        if len(self.chemical)==0:
            self.chemical = fj.create('chemical', name='A', description='Simulated inducer')

    def create_data(self, fj, step, n_samples, nt, dt):
        # Add a new assay
        self.assay = fj.create('assay', 
                            name=self.assay_name,
                            description=self.assay_description,
                            machine='Simulator',
                            temperature=0,
                            study=self.study.id[0]
                            )

        # Create the samples
        for j in range(n_samples):
            for i in range(12):
                # Inducer concentration
                conc = 10**(i/2-3)
                # See if a supplement already exists
                supplement = fj.get('supplement', chemical=self.chemical.id[0], concentration=conc)
                if len(supplement)==0:
                    supp_name = self.chemical.name[0] + f' {conc}'
                    supplement = fj.create('supplement', name=supp_name, chemical=self.chemical.id[0], concentration=conc)
                # Create a new sample
                sample = fj.create('sample',
                                row=j, col=i,
                                media=self.media.id[0],
                                strain=self.strain.id[0],
                                vector=self.vector.id[0],
                                assay=self.assay.id[0],
                                )
                fj.patch('sample', sample.id[0], supplements=[supplement.id[0]])
                # Create the measurements for this sample
                p = 0
                for t in range(nt):
                    growth_rate = flapjack.gompertz_growth_rate(t*dt, 0.01, 1, 1, 4)
                    odval = flapjack.gompertz(t*dt, 0.01, 1, 1, 4)
                    measurement = fj.create('measurement', 
                                            signal=self.signal.id[0], 
                                            time=t * dt, 
                                            value=p * odval, 
                                            sample=sample.id[0])
                    od_measurement = fj.create('measurement',
                                            signal=self.od.id[0], 
                                            time=t*dt, 
                                            value=odval, 
                                            sample=sample.id[0])
                    p = step(p, conc, growth_rate, dt)