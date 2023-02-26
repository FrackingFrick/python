"""
2D-motion on screen, includes collisions with no friction nor rotation
"""

# Import the necessary libraries
import pygame
import numpy as np


# A class representing the particles in the simulation
class Particle:
    def __init__(self, mass=1, pos=[0.0, 0.0], vel=[0.0, 0.0], colour=pygame.Color("orange"), radius=0.5):
        # Properties of the particle
        self.mass = mass
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array([0.0, 0.0])
        self.colour = colour
        self.radius = radius

        # These are needed in order to rewind the simulation
        self.pos_new = self.pos
        self.vel_new = self.vel
        self.acc_new = self.acc

    # Draws the particle to the screen (which is a property of the environmet)

    def draw(self, env):
        # First change between the coordinate systems of the simulation and the screen
        centre = env.env_to_screen(*self.pos.tolist())
        size = self.radius * env.scale
        pygame.draw.circle(env.screen, self.colour, centre, size)

    # Updates the position and the velocity to the new values

    def update(self):
        self.pos = self.pos_new
        self.vel = self.vel_new


# A class representing the environment (where the particles move)
class Environment:
    def __init__(self, screen):
        # The window where stuff is drawn on
        self.screen = screen

        # Size of the screen in both screen coordinates and simulation coordinates
        self.width_pixels = self.screen.get_width()
        self.height_pixels = self.screen.get_height()
        self.width = 10
        self.scale = self.width_pixels / self.width
        self.height = self.height_pixels / self.scale

        # Gravitational constant
        self.g = np.array([0.0, -10.0])*0
        # All the particles
        self.particles = []
        # Time step of the simulation
        self.dt = 0.01
        # Simulation method, currently either Euler or Verlet (recommended)
        self.integration_method = "Verlet"

        # Tolerances related to collision detection
        self.collision_tolerance = 1e-3
        self.collision_velocity_tolerance = 1e-3

    # Euler's method for general time step dt

    def euler(self, dt):
        for p in self.particles:
            p.acc = self.g
            p.pos_new = p.pos + dt * p.vel
            p.vel_new = p.vel + dt * p.acc

    # Verlet method for general time step dt

    def verlet(self, dt):
        for p in self.particles:
            p.acc = self.g
            p.pos_new = p.pos + dt * p.vel + 0.5 * dt**2 * p.acc
            p.vel_new = p.vel + dt * p.acc
            p.acc_new = self.g
            p.vel_new = p.vel + dt * (p.acc + p.acc_new) / 2

    # Chosen simulation method for general time step dt (not including collisions)

    def integrate(self, dt):
        if self.integration_method == "Euler":
            self.euler(dt)
        else:
            self.verlet(dt)

    # Simulate the system in time either for the time step dt or until next collision occurs (responds to collisions)

    def step(self, dt):
        # Take a tentative step forward
        self.integrate(dt)
        # Get a list of particles colliding to the walls
        boundary_collisions = self.check_boundary_collisions()
        # Get a list of particles colliding to each other
        particle_collisions = self.check_particle_collisions()

        # Count the collisions
        collisions = len(boundary_collisions) + len(particle_collisions)

        # In the case there are no collisions, we can update the positions and velocities
        if not collisions:
            for p in self.particles:
                p.update()
            return dt
        # If there are collisions, we decrease the time step to half of the original value and do the same things as above
        # We allow this halving of the time step to be done a maximum of five times
        # This way we obtain a better estimate for the actual collision time and the simulation will be more accurate
        # This is known as the bisection method
        else:
            # At time t_a, there are no collisions while at time t_b there are
            t_a = 0
            t_b = dt
            for _ in range(5):
                # Calculate the time step and the current time
                dt = (t_b - t_a) / 2
                t_c = (t_a + t_b) / 2
                # Take a tentative step forward
                self.integrate(dt)
                # Get a list of particles colliding to the walls or to each other
                boundary_collisions_new = self.check_boundary_collisions()
                particle_collisions_new = self.check_particle_collisions()
                # Count the collisions
                collisions_new = len(boundary_collisions_new) + \
                    len(particle_collisions_new)

                # If there are no collisions, update the time t_a to correspond to the current time
                # Also update the positions and momenta
                if not collisions_new:
                    t_a = t_c
                    for p in self.particles:
                        p.update()
                # If there are collisions, update the time t_b to correspond to the current time
                else:
                    t_b = t_c

                    # Update the list of colliding particles to the most recent one
                    boundary_collisions = boundary_collisions_new
                    particle_collisions = particle_collisions_new

            # Respond to collisions to the walls
            self.resolve_boundary_collisions(boundary_collisions)
            self.resolve_particle_collisions(particle_collisions)

            # Update the positions and velocities
            for p in self.particles:
                p.update()

            # Return the amount of time we went forward
            return t_b

    # Simulate the whole system forward in time by the amount determined by the time step of the environment (self.dt)

    def update(self):
        # Simulate in steps until we have reached the full self.dt
        # Multiple steps may be needed if there are collisions during the full time step
        t = 0
        while t < self.dt:
            t += self.step(self.dt - t)

    # Check whether any of the particles collide with the walls of the screen

    def check_boundary_collisions(self):
        colliding_particles = []

        for p in self.particles:
            # Calculate the distance from the right edge
            # If dist_right >= 0, the object has penetrated into the wall
            dist_right = p.pos_new[0] + p.radius - self.width / 2
            # Do the same for all the other walls
            dist_left = -p.pos_new[0] + p.radius - self.width / 2
            dist_top = p.pos_new[1] + p.radius - self.height / 2
            dist_bottom = -p.pos_new[1] + p.radius - self.height / 2

            # If there is enough penetration and the particle is further inside the wall, we have a collision event
            # In this case we add to our list the particle, the surface normal, and the distance to the wall
            if dist_right > self.collision_tolerance and p.vel_new[0] > self.collision_velocity_tolerance:
                colliding_particles.append(
                    (p, np.array([1.0, 0.0]), dist_right))

            if dist_left > self.collision_tolerance and p.vel_new[0] < -self.collision_velocity_tolerance:
                colliding_particles.append(
                    (p, np.array([-1.0, 0.0]), dist_left))
            if dist_top > self.collision_tolerance and p.vel_new[1] > self.collision_velocity_tolerance:
                colliding_particles.append((p, np.array([0.0, 1.0]), dist_top))
            if dist_bottom > self.collision_tolerance and p.vel_new[1] < -self.collision_velocity_tolerance:
                colliding_particles.append(
                    (p, np.array([0.0, -1.0]), dist_bottom))

        return colliding_particles

    # Respond to the collisions to the walls

    def resolve_boundary_collisions(self, colliding_particles):
        # The coefficient of restitution defined here should be moved somewhere else
        coeff_of_rest = 0.8
        for p, n, d in colliding_particles:
            vel_rel = np.dot(p.vel_new, n)
            # Try to react also to resting contacts
            if abs(vel_rel) < self.collision_velocity_tolerance:
                p.vel_new -= vel_rel * n
                p.pos_new -= d * n
            else:
                p.vel_new -= (1 + coeff_of_rest) * vel_rel * n

    # Check whether any of the particles collide with each other

    def check_particle_collisions(self):
        colliding_particles = []

        num_particles = len(self.particles)

        # Loop over all the pairs of particles
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                p_1 = self.particles[i]
                p_2 = self.particles[j]

                # Calculate the relative position between the particles
                # And using this, also the distance and the surface normal
                rel_pos = p_2.pos_new - p_1.pos_new
                dist = np.linalg.norm(rel_pos)
                normal = rel_pos / dist

                # Subtract from the distance the radii of the particles
                # If dist <= 0, collision occurs
                dist -= p_1.radius + p_2.radius
                rel_vel = np.dot(p_2.vel_new - p_1.vel_new, normal)

                if dist < - self.collision_tolerance and rel_vel < -self.collision_velocity_tolerance:
                    colliding_particles.append((p_1, p_2, normal))

        return colliding_particles

    # Respond to the collisions between the particles

    def resolve_particle_collisions(self, colliding_particles):
        # The coefficient of restitution defined here should be moved somewhere else
        coeff_of_rest = 0.8
        for p_1, p_2, normal in colliding_particles:
            rel_vel = np.dot(p_2.vel_new - p_1.vel_new, normal)

            p_1.vel_new += (1 + coeff_of_rest) * rel_vel / \
                (1 + p_1.mass / p_2.mass) * normal
            p_2.vel_new -= (1 + coeff_of_rest) * rel_vel / \
                (1 + p_2.mass / p_1.mass) * normal

    # Draw everything in the environment to the screen

    def draw(self):
        self.screen.fill(pygame.Color("white"))
        for p in self.particles:
            p.draw(self)

    # Coordinate transformation from the simulation coordinates to the screen coordinates

    def env_to_screen(self, x, y):
        x_screen = self.scale * x + self.width_pixels / 2
        y_screen = -self.scale * y + self.height_pixels / 2

        return x_screen, y_screen

    # Coordinate transformation from the screen coordinates to the simulation coordinates

    def screen_to_env(self, x_screen, y_screen):
        x = (x_screen - self.width_pixels / 2) / self.scale
        y = -(y_screen - self.height_pixels / 2) / self.scale

        return x, y

    # Add a particle with given position, velocity, and mass

    def add_particle(self, pos, vel=[0.0, 0.0], mass=1, radius=0.5):
        # check that self.particles is not empty
        print(pos)
        collision = 0
        if self.particles:
            for p in self.particles:
                rel_pos = p.pos_new - pos
                dist = np.linalg.norm(rel_pos)
                dist -= p.radius + radius
                if (dist <= 0):
                    collision = 1

        # Calculate the distance from the right edge
        # If dist_right >= 0, the object has penetrated into the wall
        dist_right = pos[0] + radius - self.width / 2
        # Do the same for all the other walls
        dist_left = -pos[0] + radius - self.width / 2
        dist_top = pos[1] + radius - self.height / 2
        dist_bottom = -pos[1] + radius - self.height / 2
        print(dist_right, dist_left, dist_top, dist_bottom)
        if (dist_right >= 0 or dist_left >= 0 or dist_top >= 0 or dist_bottom >= 0):
            collision = 1
        if collision != 1:
            self.particles.append(Particle(mass=mass, pos=pos, vel=vel, radius=radius))
        else:
            return


# Initialise Pygame
pygame.init()

# Screen size
width, height = 1200, 800

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collision simulation v0")

# Create a clock
FPS = 60
clock = pygame.time.Clock()

# Create the environment
env = Environment(screen)

# Game loop
running = True
while running:
    # Handle all the events
    for event in pygame.event.get():
        # Exit the game loop if one presses the window's "X" button
        if event.type == pygame.QUIT:
            running = False

        # Create a particle with mouse (left click == 1)
        # The position is determined by where the left mouse button was pressed down
        # The velocity is determined by where the left mouse button was released
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            x_screen_start, y_screen_start = event.pos
        if event.type == pygame.MOUSEBUTTONUP and (event.button == 1 or event.button == 3):
            x_screen_end, y_screen_end = event.pos
            v_x = (x_screen_start - x_screen_end) * 0.03
            v_y = -(y_screen_start - y_screen_end) * 0.03
            x, y = env.screen_to_env(x_screen_start, y_screen_start)
            # env.add_particle([x, y], [v_x, v_y])
            if event.button == 1:
                env.add_particle([x, y], [v_x, v_y], radius=0.5)
            if event.button == 3:
                env.add_particle([x, y], [v_x, v_y], radius=0.25, mass=0.125)

    # Check how much time has passed since the last iteration, adjust the simulation time step accordingly
    dt = clock.tick(FPS)
    env.dt = dt / 1000