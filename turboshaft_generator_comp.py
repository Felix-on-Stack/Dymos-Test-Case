import numpy as np
import openmdao.api as om


class TurboshaftGenerator(om.ExplicitComponent):
    "Models the fuel consumption of a turbine generator"
    fc_poly = np.poly1d([3.5, -14, 21, -14, 4.5, 0])

    def initialize(self):
        self.options.declare('num_nodes', types=int, default = 1)

    def setup(self):
        nn = self.options['num_nodes']


        self.add_input('P_req', val=np.ones(nn), desc='required power', units='kW')
        
        
        self.add_output('fuel_rate', val=np.ones(nn), desc='Fuel Burnt', units='kg/s')
    
    
        ar = np.arange(nn)
        self.declare_partials('fuel_rate', 'P_req', rows=ar, cols=ar)        


    def compute(self, inputs, outputs):
        P_req = inputs['P_req'] 

        outputs['fuel_rate'] =  self.fc_poly(P_req)
        
        

    def compute_partials(self, inputs, partials):
        P_req = inputs['P_req'] 
        fc_polyder = np.polyder(self.fc_poly)


        partials['fuel_rate', 'P_req'] = fc_polyder(P_req)


        
