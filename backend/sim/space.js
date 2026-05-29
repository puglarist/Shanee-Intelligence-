const debug = require('debug')('omniverse:sim:space');

/**
 * Space Simulation - Orbital mechanics and celestial bodies
 */
class SpaceSimulation {
  constructor(config) {
    this.config = config;
    this.celestialBodies = this.initializeSolarSystem();
    this.time = 0; // Simulation time in seconds
    this.timeScale = 1; // Simulation speed multiplier
    this.G = 6.674e-11; // Gravitational constant
    
    debug('Space simulation initialized');
  }

  /**
   * Initialize solar system with bodies
   */
  initializeSolarSystem() {
    const AU = 1.496e11; // Astronomical unit in meters

    return {
      sun: {
        id: 'sun',
        name: 'Sun',
        mass: 1.989e30,
        radius: 696000,
        position: { x: 0, y: 0, z: 0 },
        velocity: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        color: { r: 1, g: 1, b: 0 }
      },
      earth: {
        id: 'earth',
        name: 'Earth',
        mass: 5.972e24,
        radius: 6371,
        position: { x: AU, y: 0, z: 0 },
        velocity: { x: 0, y: 29780, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        color: { r: 0.2, g: 0.4, b: 0.8 }
      },
      mars: {
        id: 'mars',
        name: 'Mars',
        mass: 6.417e23,
        radius: 3390,
        position: { x: AU * 1.524, y: 0, z: 0 },
        velocity: { x: 0, y: 24070, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        color: { r: 0.8, g: 0.4, b: 0.2 }
      },
      moon: {
        id: 'moon',
        name: 'Moon',
        mass: 7.342e22,
        radius: 1737,
        position: { x: AU + 384400, y: 0, z: 0 },
        velocity: { x: 0, y: 29780 + 1022, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        color: { r: 0.6, g: 0.6, b: 0.6 }
      }
    };
  }

  /**
   * Calculate gravitational force between two bodies
   */
  calculateGravitationalForce(body1, body2) {
    const dx = body2.position.x - body1.position.x;
    const dy = body2.position.y - body1.position.y;
    const dz = body2.position.z - body1.position.z;

    const distanceSq = dx * dx + dy * dy + dz * dz;
    const distance = Math.sqrt(distanceSq);

    if (distance === 0) return { x: 0, y: 0, z: 0 };

    const forceMagnitude = (this.G * body1.mass * body2.mass) / distanceSq;

    const forceX = (forceMagnitude / distance) * dx;
    const forceY = (forceMagnitude / distance) * dy;
    const forceZ = (forceMagnitude / distance) * dz;

    return { x: forceX, y: forceY, z: forceZ };
  }

  /**
   * Update orbital positions (simplified Euler integration)
   */
  updateOrbits(deltaTime) {
    const scaledDelta = deltaTime * this.timeScale;
    const bodies = Object.values(this.celestialBodies);

    // Calculate accelerations
    const accelerations = {};
    bodies.forEach(body => {
      accelerations[body.id] = { x: 0, y: 0, z: 0 };

      bodies.forEach(other => {
        if (body.id === other.id) return;

        const force = this.calculateGravitationalForce(body, other);
        const ax = force.x / body.mass;
        const ay = force.y / body.mass;
        const az = force.z / body.mass;

        accelerations[body.id].x += ax;
        accelerations[body.id].y += ay;
        accelerations[body.id].z += az;
      });
    });

    // Update velocities and positions
    bodies.forEach(body => {
      const acc = accelerations[body.id];

      body.velocity.x += acc.x * scaledDelta;
      body.velocity.y += acc.y * scaledDelta;
      body.velocity.z += acc.z * scaledDelta;

      body.position.x += body.velocity.x * scaledDelta;
      body.position.y += body.velocity.y * scaledDelta;
      body.position.z += body.velocity.z * scaledDelta;

      // Simple rotation
      body.rotation.x += 0.0001 * scaledDelta;
      body.rotation.y += 0.0001 * scaledDelta;
    });

    this.time += scaledDelta;
  }

  /**
   * Get orbital data
   */
  getOrbitalData() {
    const data = {};

    for (const [key, body] of Object.entries(this.celestialBodies)) {
      const distance = Math.sqrt(
        body.position.x ** 2 + body.position.y ** 2 + body.position.z ** 2
      );
      const speed = Math.sqrt(
        body.velocity.x ** 2 + body.velocity.y ** 2 + body.velocity.z ** 2
      );

      data[body.id] = {
        id: body.id,
        name: body.name,
        position: body.position,
        velocity: body.velocity,
        rotation: body.rotation,
        distance,
        speed,
        color: body.color,
        radius: body.radius
      };
    }

    return {
      timestamp: new Date().toISOString(),
      simulationTime: this.time,
      timeScale: this.timeScale,
      bodies: data
    };
  }

  /**
   * Set simulation time scale
   */
  setTimeScale(scale) {
    this.timeScale = Math.max(0.001, scale);
    debug(`Time scale set to ${this.timeScale}x`);
  }

  /**
   * Reset simulation
   */
  reset() {
    this.time = 0;
    this.celestialBodies = this.initializeSolarSystem();
    debug('Space simulation reset');
  }
}

module.exports = SpaceSimulation;
