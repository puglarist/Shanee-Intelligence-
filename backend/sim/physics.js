const debug = require('debug')('omniverse:sim:physics');

/**
 * Physics Engine - Handles rigid body dynamics and collisions
 */
class PhysicsEngine {
  constructor(config) {
    this.config = config;
    this.bodies = new Map();
    this.gravity = { x: 0, y: -9.81, z: 0 };
    this.timeStep = 1 / (config.simulation?.physicsFPS || 60);
    this.substeps = 4;
    this.debug = {};
    
    debug('Physics engine initialized');
  }

  /**
   * Create a rigid body
   */
  createBody(id, options = {}) {
    const body = {
      id,
      mass: options.mass || 1,
      position: options.position || { x: 0, y: 0, z: 0 },
      velocity: options.velocity || { x: 0, y: 0, z: 0 },
      acceleration: { x: 0, y: 0, z: 0 },
      rotation: options.rotation || { x: 0, y: 0, z: 0 },
      angularVelocity: { x: 0, y: 0, z: 0 },
      shape: options.shape || 'sphere',
      radius: options.radius || 1,
      friction: options.friction || 0.3,
      restitution: options.restitution || 0.5,
      linearDamping: options.linearDamping || 0.01,
      angularDamping: options.angularDamping || 0.01,
      isStatic: options.isStatic || false,
      isAwake: true,
      forces: [],
      torques: []
    };

    this.bodies.set(id, body);
    debug(`Created body: ${id}`);
    return body;
  }

  /**
   * Remove a body
   */
  removeBody(id) {
    this.bodies.delete(id);
    debug(`Removed body: ${id}`);
  }

  /**
   * Add force to a body
   */
  addForce(bodyId, force) {
    const body = this.bodies.get(bodyId);
    if (body) {
      body.forces.push(force);
    }
  }

  /**
   * Add torque to a body
   */
  addTorque(bodyId, torque) {
    const body = this.bodies.get(bodyId);
    if (body) {
      body.torques.push(torque);
    }
  }

  /**
   * Update physics simulation
   */
  update(deltaTime) {
    const fixedTimeStep = this.timeStep / this.substeps;

    for (let i = 0; i < this.substeps; i++) {
      this.updateForces();
      this.integrateVelocity(fixedTimeStep);
      this.updateCollisions();
      this.integratePosition(fixedTimeStep);
    }
  }

  /**
   * Calculate forces on all bodies
   */
  updateForces() {
    for (const body of this.bodies.values()) {
      if (body.isStatic) continue;

      // Reset acceleration
      body.acceleration = { x: 0, y: 0, z: 0 };

      // Apply gravity
      if (!body.isStatic) {
        body.acceleration.x += this.gravity.x;
        body.acceleration.y += this.gravity.y;
        body.acceleration.z += this.gravity.z;
      }

      // Apply accumulated forces
      let totalForce = { x: 0, y: 0, z: 0 };
      for (const force of body.forces) {
        totalForce.x += force.x;
        totalForce.y += force.y;
        totalForce.z += force.z;
      }

      body.acceleration.x += totalForce.x / body.mass;
      body.acceleration.y += totalForce.y / body.mass;
      body.acceleration.z += totalForce.z / body.mass;

      body.forces = [];
    }
  }

  /**
   * Integrate velocities
   */
  integrateVelocity(deltaTime) {
    for (const body of this.bodies.values()) {
      if (body.isStatic) continue;

      body.velocity.x += body.acceleration.x * deltaTime;
      body.velocity.y += body.acceleration.y * deltaTime;
      body.velocity.z += body.acceleration.z * deltaTime;

      // Apply damping
      body.velocity.x *= (1 - body.linearDamping);
      body.velocity.y *= (1 - body.linearDamping);
      body.velocity.z *= (1 - body.linearDamping);

      body.angularVelocity.x *= (1 - body.angularDamping);
      body.angularVelocity.y *= (1 - body.angularDamping);
      body.angularVelocity.z *= (1 - body.angularDamping);
    }
  }

  /**
   * Integrate positions
   */
  integratePosition(deltaTime) {
    for (const body of this.bodies.values()) {
      if (body.isStatic) continue;

      body.position.x += body.velocity.x * deltaTime;
      body.position.y += body.velocity.y * deltaTime;
      body.position.z += body.velocity.z * deltaTime;

      body.rotation.x += body.angularVelocity.x * deltaTime;
      body.rotation.y += body.angularVelocity.y * deltaTime;
      body.rotation.z += body.angularVelocity.z * deltaTime;
    }
  }

  /**
   * Simple sphere-sphere collision detection and response
   */
  updateCollisions() {
    const bodies = Array.from(this.bodies.values());

    for (let i = 0; i < bodies.length; i++) {
      for (let j = i + 1; j < bodies.length; j++) {
        const body1 = bodies[i];
        const body2 = bodies[j];

        if (body1.isStatic && body2.isStatic) continue;

        const dx = body2.position.x - body1.position.x;
        const dy = body2.position.y - body1.position.y;
        const dz = body2.position.z - body1.position.z;

        const distanceSq = dx * dx + dy * dy + dz * dz;
        const minDistance = body1.radius + body2.radius;

        if (distanceSq < minDistance * minDistance) {
          this.resolveCollision(body1, body2);
        }
      }
    }
  }

  /**
   * Resolve collision between two bodies
   */
  resolveCollision(body1, body2) {
    const dx = body2.position.x - body1.position.x;
    const dy = body2.position.y - body1.position.y;
    const dz = body2.position.z - body1.position.z;

    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    const overlap = (body1.radius + body2.radius) - distance;

    if (distance === 0) return;

    // Separate bodies
    const nx = dx / distance;
    const ny = dy / distance;
    const nz = dz / distance;

    const separation = (overlap / 2) + 0.001;

    if (!body1.isStatic) {
      body1.position.x -= nx * separation;
      body1.position.y -= ny * separation;
      body1.position.z -= nz * separation;
    }

    if (!body2.isStatic) {
      body2.position.x += nx * separation;
      body2.position.y += ny * separation;
      body2.position.z += nz * separation;
    }

    // Calculate relative velocity
    const dvx = body2.velocity.x - body1.velocity.x;
    const dvy = body2.velocity.y - body1.velocity.y;
    const dvz = body2.velocity.z - body1.velocity.z;

    const relativeVelocity = dvx * nx + dvy * ny + dvz * nz;

    if (relativeVelocity >= 0) return;

    const restitution = (body1.restitution + body2.restitution) / 2;
    const impulse = -(1 + restitution) * relativeVelocity;

    const mass1 = body1.isStatic ? Infinity : body1.mass;
    const mass2 = body2.isStatic ? Infinity : body2.mass;
    const totalMass = mass1 + mass2;

    const impulseX = (impulse / totalMass) * nx;
    const impulseY = (impulse / totalMass) * ny;
    const impulseZ = (impulse / totalMass) * nz;

    if (!body1.isStatic) {
      body1.velocity.x -= impulseX / body1.mass;
      body1.velocity.y -= impulseY / body1.mass;
      body1.velocity.z -= impulseZ / body1.mass;
    }

    if (!body2.isStatic) {
      body2.velocity.x += impulseX / body2.mass;
      body2.velocity.y += impulseY / body2.mass;
      body2.velocity.z += impulseZ / body2.mass;
    }
  }

  /**
   * Get all bodies state
   */
  getState() {
    const bodiesState = [];

    for (const body of this.bodies.values()) {
      bodiesState.push({
        id: body.id,
        position: body.position,
        velocity: body.velocity,
        rotation: body.rotation,
        shape: body.shape,
        radius: body.radius
      });
    }

    return {
      timestamp: new Date().toISOString(),
      bodies: bodiesState,
      gravity: this.gravity
    };
  }
}

module.exports = PhysicsEngine;
