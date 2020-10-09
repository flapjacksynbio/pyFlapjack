import numpy as np
import flapjack
from flapjack import Flapjack
import pandas as pd

colors = ['red', 'green', 'blue']

class Simulator:
    def __init__(
        self,
        study_name='',
        assay_name='', 
        study_description='',
        assay_description='',
        dna_name='',
        init_proteins=[0],
        concentrations=[0],
        n_signals=1,
        fluo_noise=0.01,
        od_noise=0.01
        ):
        self.assay_name = assay_name
        self.assay_description = assay_description
        self.study_name = study_name
        self.study_description = study_description
        self.dna_name = dna_name
        self.init_proteins = np.array(init_proteins)
        self.concentrations = concentrations
        self.n_signals = n_signals
        self.signals = []
        self.fluo_noise = fluo_noise
        self.od_noise = od_noise

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
        for i in range(self.n_signals):
            signal = fj.get('signal', name=f'SFP{i}')
            if len(signal)==0:
                signal = fj.create('signal', name=f'SFP{i}', color=colors[i], description='Simulated signal')
            self.signals.append(signal)
        self.od = fj.get('signal', name='SOD')
        if len(self.od)==0:
            self.od = fj.create('signal', name='SOD', color='black', description='Simulated OD')

        if len(self.concentrations) > 1:
            # Get or create the chemical and supplement
            self.chemical = fj.get('chemical', name='A', description='Simulated inducer')
            if len(self.chemical)==0:
                print('Creating chemical A')
                self.chemical = fj.create('chemical', name='A', description='Simulated inducer')

    def create_data(self, fj, step, n_samples, nt, dt, sim_steps):
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
            print(f'Uploading dataset {j+1} of {n_samples}')
            for i, conc in enumerate(self.concentrations):
                # Create a new sample
                sample = fj.create('sample',
                                row=j, col=i,
                                media=self.media.id[0],
                                strain=self.strain.id[0],
                                vector=self.vector.id[0],
                                assay=self.assay.id[0],
                                )
                if conc > 0:
                    # See if a supplement already exists
                    supplement = fj.get('supplement', chemical=self.chemical.id[0], concentration=conc)
                    if len(supplement)==0:
                        supp_name = self.chemical.name[0] + f' {conc}'
                        supplement = fj.create('supplement', name=supp_name, chemical=self.chemical.id[0], concentration=conc)
                    fj.patch('sample', sample.id[0], supplements=[supplement.id[0]])
                # Create the measurements for this sample
                p = list(self.init_proteins)
                fp = np.zeros((nt, self.n_signals))
                od = np.zeros((nt,)) 
                for t in range(nt):
                    # Update sim by sub-timesteps
                    for tt in range(sim_steps):
                        growth_rate = flapjack.gompertz_growth_rate((t + tt / sim_steps) * dt, 0.01, 1, 1, 4)
                        p = step(p, conc, growth_rate, dt/sim_steps)
                    odval = flapjack.gompertz((t + tt/sim_steps)*dt, 0.01, 1, 1, 4)
                    for s in range(self.n_signals):
                        fp[t,s] = p[s] * odval
                    od[t] = odval
                times = np.arange(nt) * dt
                for s in range(self.n_signals):
                    fp_meas = pd.DataFrame()
                    fp_meas['Time'] = times
                    sigma = fp[:,s] / np.sqrt(self.fluo_noise)
                    fp_meas['Measurement'] = fp[:,s] + sigma * np.random.normal(size=fp.shape[:1])
                    fj.upload_measurements(fp_meas, signal=[self.signals[s].id[0]], sample=[sample.id[0]])
                od_meas = pd.DataFrame()
                od_meas['Time'] = times
                sigma = od / np.sqrt(self.od_noise)
                od_meas['Measurement'] = od + sigma * np.random.normal(size=od.shape)
                fj.upload_measurements(od_meas, signal=[self.od.id[0]], sample=[sample.id[0]])