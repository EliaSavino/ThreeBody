'''
Author: Elia Savino
github: github.com/EliaSavino

Happy Hacking!

Descr: plotting file to plot the results of the three body problem simulation

'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#initialise the bodies:
from Classes.body import Body
earth_mass = 5.972e24  # mass of the earth in kg
moon_mass = 7.342e22   # mass of the moon in kg
second_moon_mass = 1e10   # mass of the moon in kg
distance_moon_earth = 384400000   # average distance from Earth to Moon in meters

# Initial Positions
earth_position = np.array([0.0, 0.0])
moon_position = np.array([distance_moon_earth, 0.0])  # Moon starts at x = distance, y = 0
second_moon_position = np.array([-distance_moon_earth * 0.8, 0.9*distance_moon_earth])  # Different initial position

# Velocities for circular orbit calculation
orbital_velocity_magnitude_moon = np.sqrt(Body.g * earth_mass / distance_moon_earth)
moon_velocity = np.array([0.0, orbital_velocity_magnitude_moon])  # Orbiting in positive y-direction

# Second Moon with an elliptical and inclined orbit
# Slightly less than needed for a circular orbit to introduce elliptical properties
orbital_velocity_magnitude_second_moon = np.sqrt(Body.g * earth_mass / (distance_moon_earth * 1.5)) * 0.9
second_moon_velocity = np.array([orbital_velocity_magnitude_second_moon, orbital_velocity_magnitude_second_moon])

# Create bodies
earth = Body(earth_position, [0.0,0.0], earth_mass, 'blue', size=50.0)
moon = Body(moon_position, moon_velocity, moon_mass, 'grey', size=30.0)
second_moon = Body(second_moon_position, second_moon_velocity, second_moon_mass, 'red', size=10.0)
second_earth = Body([-distance_moon_earth, 0.0], [0.0, -orbital_velocity_magnitude_moon], earth_mass, 'green', size=30.0)
# make some random asteroids:
asteroids = [Body(np.random.rand(2)*1e9, np.random.rand(2)*1e3, 1e19, 'black', size=10.0) for _ in range(10)]

sun = Body([0.0, 0.0], [0.0, 0.0], 1.989e30, 'yellow', size=100.0)
bodies = [sun, *asteroids]
#initialise the time step and the time:
dt = 500  # time step in seconds, consider starting small
t_f = 10*3600 * 24 * 30  # simulate for one month (in seconds)
times = np.arange(0, t_f, dt)

#run the simulation:
# for t in times:
#     for body in bodies:
#         body.calculate_force(bodies)
#     for body in bodies:
#         body.update_acceleration()
#         body.update_velocity(dt)
#         body.update_position(dt)
fig, ax = plt.subplots()
ax.set_xlim(-10*distance_moon_earth, 10*distance_moon_earth)
ax.set_ylim(-10*distance_moon_earth, 10*distance_moon_earth)
# Creating a scatter plot for each body
scatters = [ax.scatter(body.position[0], body.position[1], color = body.color, s = body.size) for body in bodies]
lines = [ax.plot([], [], color=body.color)[0] for body in bodies]

def init():
    for scatter,line, body in zip(scatters,lines, bodies):
        scatter.set_offsets([body.position[0], body.position[1]])
        line.set_data([], [])
    return scatters + lines


def update(frame):
    for body in bodies:
        body.calculate_force([b for b in bodies if b != body])
    for body in bodies:
        body.update_acceleration()
        body.update_velocity(dt)  # Assuming dt=1 for simplicity; adjust as needed
        body.update_position(dt)

    # Gather all current positions
    for scatter, line, body in zip(scatters, lines, bodies):
        positions = np.array(body.position_history)
        line.set_data(positions[:, 0], positions[:, 1])
        scatter.set_offsets([body.position[0], body.position[1]])


    return scatters + lines


# Create animation
ani = FuncAnimation(fig, update, frames=np.arange(0, len(times) , 1), init_func=init, blit=True, interval=10)

# Show animation

plt.show()