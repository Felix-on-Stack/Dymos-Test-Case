import matplotlib.pyplot as plt
import openmdao.api as om
import dymos as dm
from dymos.examples.plotting import plot_results
from propulsion_group import PropulsionGroupODE


# Initialize the Problem and the optimization driver
p = om.Problem(model=om.Group())
p.driver = om.ScipyOptimizeDriver()


# Create a trajectory and add a phase to it
traj = p.model.add_subsystem('traj', dm.Trajectory())

phase = traj.add_phase('phase0',
                       dm.Phase(ode_class=PropulsionGroupODE,
                                transcription=dm.GaussLobatto(num_segments=3)))
                                # transcription=dm.Radau(num_segments=3)))
                                # transcription=dm.RungeKutta(num_segments=3)))
                                                              


# Set the variables
phase.set_time_options(initial_bounds=(0, 0), duration_bounds=(3600, 3600))

phase.add_state('fuel_burnt', units='kg', #defect_ref=1,# fix_initial=True,
                rate_source='assembly.fuel_rate_total', lower=0)

phase.add_control('P_gen2', units='kW', opt=True, lower=-0.001, upper=1.001, 
                  targets=['generator2.P_req', 'assembly.P_gen2'])

phase.add_control('P_gen1', units='kW', opt=True, lower=-0.001, upper=1.001, 
                  targets=['generator1.P_req', 'assembly.P_gen1'])


p_set = 1.4
phase.add_path_constraint('assembly.P_total', lower=p_set, upper=p_set+0.01, units='kW')


# Set Objective
phase.add_objective('fuel_burnt', loc='final')


# Setup the Problem
p.model.linear_solver = om.DirectSolver()
p.setup()


# Set the initial values
p['traj.phase0.states:fuel_burnt'][:] = 0 
p['traj.phase0.controls:P_gen1'][:] = 1
p['traj.phase0.controls:P_gen2'][:] = 1


# Solve for the optimal trajectory
dm.run_problem(p)


# Test the results
print(p.get_val('traj.phase0.timeseries.states:fuel_burnt')[-1])

# # generate the explicitly simulated trajectory
exp_out = traj.simulate()

fig,axs = plot_results([('traj.phase0.timeseries.time', 'traj.phase0.timeseries.controls:P_gen1',
                'time (s)', 'P1 (kW)'),
              ('traj.phase0.timeseries.time', 'traj.phase0.timeseries.controls:P_gen2',
                'time (s)', 'P2 (kW)'),
              ('traj.phase0.timeseries.time', 'traj.phase0.timeseries.states:fuel_burnt',
                'time (s)', 'fuel burnt (kg)')],
              title='Twin Turboelectric Test Case',
              p_sol=p, p_sim=exp_out)

axs[0].set_ylim(0, 1.1)
axs[1].set_ylim(0, 1.1)
plt.show()

print(p.get_val('traj.phase0.timeseries.states:fuel_burnt')[-1])
