import numpy as np
import openmdao.api as om


class PropulsionAssembly(om.ExplicitComponent):
    "Connects the different aircraft components"

    def initialize(self):
        self.options.declare('num_nodes', types=int, default = 1)

    def setup(self):
        nn = self.options['num_nodes']


        self.add_input('P_gen1', val=np.ones(nn), desc='power of generator 1', units='kW')
        self.add_input('P_gen2', val=np.ones(nn), desc='power of generator 2', units='kW')
        self.add_input('fuel_rate_gen1', val=np.ones(nn), desc='fuel burn of generator 1', units='kg/s')
        self.add_input('fuel_rate_gen2', val=np.ones(nn), desc='fuel burn of generator 2', units='kg/s')
        

        self.add_output('P_total', val=np.ones(nn), desc='total Power', units='kW')
        self.add_output('fuel_rate_total', val=np.ones(nn), desc='total fuel burnt', units='kg/s')
        

        ar = np.arange(nn)
        
        
        self.declare_partials('P_total', 'P_gen1', rows=ar, cols=ar, val=1.0)
        self.declare_partials('P_total', 'P_gen1', rows=ar, cols=ar, val=1.0)
        self.declare_partials('fuel_rate_total', 'fuel_rate_gen1', rows=ar, cols=ar, val=1.0)
        self.declare_partials('fuel_rate_total', 'fuel_rate_gen1', rows=ar, cols=ar, val=1.0)
        
    def compute(self, inputs, outputs):
    
        outputs['fuel_rate_total'] =  inputs['fuel_rate_gen1'] + inputs['fuel_rate_gen2']
        outputs['P_total'] = inputs['P_gen1'] + inputs['P_gen2']
