import openmdao.api as om

from turboshaft_generator_comp import TurboshaftGenerator
from propulsion_assembly_comp import PropulsionAssembly



class PropulsionGroupODE(om.Group):

    def initialize(self):
        self.options.declare('num_nodes', types=int, default = 1,
                             desc='Number of nodes to be evaluated in the RHS')

    def setup(self):
        nn = self.options['num_nodes']


        
        self.add_subsystem(name='generator2',
                           subsys=TurboshaftGenerator(num_nodes=nn))

        self.add_subsystem(name='generator1',
                           subsys=TurboshaftGenerator(num_nodes=nn))        
        
        
        self.add_subsystem(name='assembly',
                           subsys=PropulsionAssembly(num_nodes=nn))
        
        
        self.connect('generator1.fuel_rate', 'assembly.fuel_rate_gen1')
        self.connect('generator2.fuel_rate', 'assembly.fuel_rate_gen2')