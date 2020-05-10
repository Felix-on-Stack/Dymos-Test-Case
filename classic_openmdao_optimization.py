import openmdao.api as om
from turboshaft_generator_comp import TurboshaftGenerator
from propulsion_assembly_comp import PropulsionAssembly


# build the model
prob = om.Problem()
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
indeps.add_output('gen1', 0, units='kW')
indeps.add_output('gen2', 0, units='kW')

nn = 1

prob.model.add_subsystem(name='generator2',
                         subsys=TurboshaftGenerator(num_nodes=nn))
prob.model.add_subsystem(name='generator1',
                         subsys=TurboshaftGenerator(num_nodes=nn))        
        
        
prob.model.add_subsystem(name='assembly',
                         subsys=PropulsionAssembly(num_nodes=nn))
        
        
prob.model.connect('generator1.fuel_rate', 'assembly.fuel_rate_gen1')
prob.model.connect('generator2.fuel_rate', 'assembly.fuel_rate_gen2')

prob.model.connect('indeps.gen1', ['generator1.P_req', 'assembly.P_gen1'])
prob.model.connect('indeps.gen2', ['generator2.P_req', 'assembly.P_gen2'])

# setup the optimization
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'#'COBYLA'

# prob.driver = om.pyOptSparseDriver()
# prob.driver.options['optimizer'] = 'NOMAD'#'NSGA2'#"ALPSO"


prob.model.add_design_var('indeps.gen1', lower=0, upper=1)
prob.model.add_design_var('indeps.gen2', lower=0, upper=1)
prob.model.add_objective('assembly.fuel_rate_total')

# constraint
pwr_const = 1.8
prob.model.add_constraint('assembly.P_total', lower=pwr_const-0.0001, upper=pwr_const+0.0001)

prob.setup()
prob.run_driver()


print('Fuel consumption rate: {}'.format(prob['assembly.fuel_rate_total']))
print('P_gen1: {}'.format(prob['indeps.gen1']))
print('P_gen2: {}'.format(prob['indeps.gen2']))