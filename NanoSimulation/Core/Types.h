#pragma once

#include <vector>
#include <cstdint>
#include <map>
#include <memory>
#include <queue>

namespace NanoSim {

// ============================================================================
// Vector Math Types
// ============================================================================

struct Vector3 {
    float x, y, z;
    
    Vector3() : x(0), y(0), z(0) {}
    Vector3(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}
    
    Vector3 operator+(const Vector3& other) const {
        return Vector3(x + other.x, y + other.y, z + other.z);
    }
    
    Vector3 operator-(const Vector3& other) const {
        return Vector3(x - other.x, y - other.y, z - other.z);
    }
    
    Vector3 operator*(float scalar) const {
        return Vector3(x * scalar, y * scalar, z * scalar);
    }
    
    float dot(const Vector3& other) const {
        return x * other.x + y * other.y + z * other.z;
    }
    
    float length() const;
    Vector3 normalized() const;
};

// ============================================================================
// Enumeration Types
// ============================================================================

enum class AgentType : uint8_t {
    WORKER = 0,
    TRANSPORT = 1,
    SENSOR = 2,
    COMMANDER = 3,
    REPAIR = 4,
};

enum class AgentState : uint8_t {
    IDLE = 0,
    MOVING = 1,
    WORKING = 2,
    CHARGING = 3,
    DAMAGED = 4,
    DESTROYED = 5,
};

enum class MaterialType : uint8_t {
    EMPTY = 0,
    COPPER = 1,
    SILICON = 2,
    GOLD = 3,
    TITANIUM = 4,
    CUSTOM_A = 5,
    CUSTOM_B = 6,
    CUSTOM_C = 7,
};

enum class TaskType : uint8_t {
    GATHER = 0,
    BUILD = 1,
    TRANSPORT = 2,
    REPAIR = 3,
    SCAN = 4,
};

// ============================================================================
// Material Properties
// ============================================================================

struct MaterialProperties {
    uint8_t id;
    const char* name;
    
    // Physical properties
    float density;                          // g/cm³
    float hardness;                         // Mohs scale (0-10)
    float thermalConductivity;              // W/(m·K)
    float electricalConductivity;           // S/m
    float elasticModulus;                   // GPa
    
    // Chemical properties
    float reactivityScore;                  // 0.0 (inert) - 1.0 (reactive)
    
    // Nano-specific
    bool isSelfAssembling;
    float assemblyEnergyPerVoxel;
    bool isProgrammable;                    // Metamaterial capable
    
    // Optical
    float refractionIndex;
    float transparency;                     // 0.0 (opaque) - 1.0 (transparent)
};

// ============================================================================
// Agent Structures
// ============================================================================

struct NanobotAgent {
    // Identity
    uint64_t id;
    AgentType type;
    
    // Physics state
    Vector3 position;
    Vector3 velocity;
    float mass;
    float radius;
    
    // Energy state
    float energyLevel;                      // 0.0 - 1.0
    float maxEnergy;
    
    // Agent state
    AgentState state;
    float damageFactor;                     // 0.0 (destroyed) - 1.0 (perfect)
    
    // Sensors
    float sensorRange;
    
    // Neighbor tracking
    std::vector<uint64_t> neighbors;        // IDs of nearby agents
    
    NanobotAgent() 
        : id(0), type(AgentType::WORKER),
          mass(1.0f), radius(0.5f),
          energyLevel(1.0f), maxEnergy(1.0f),
          state(AgentState::IDLE),
          damageFactor(1.0f),
          sensorRange(5.0f) {}
};

// ============================================================================
// Material Voxel
// ============================================================================

struct MaterialVoxel {
    MaterialType materialType;
    float energyState;                      // 0.0 - 1.0 (excitation)
    float temperatureK;                     // Kelvin
    uint8_t occupancyCount;                 // Agent count
    bool structurallyConnected;             // Part of structure?
    uint32_t lastModifiedStep;
    uint8_t assemblyProgress;               // 0-100
    
    MaterialVoxel() 
        : materialType(MaterialType::EMPTY),
          energyState(0.0f),
          temperatureK(300.0f),
          occupancyCount(0),
          structurallyConnected(false),
          lastModifiedStep(0),
          assemblyProgress(0) {}
};

// ============================================================================
// Simulation Configuration
// ============================================================================

struct SimulationConfig {
    uint32_t gridSize;                      // 256, 512, 1024
    float timestep;                         // 0.001 - 0.01 seconds
    float simulationSpeed;                  // 1.0 = real-time
    uint32_t maxAgents;
    bool enablePhysics;
    bool enableVisualization;
    bool enableSerialization;
    
    SimulationConfig()
        : gridSize(256),
          timestep(0.005f),
          simulationSpeed(1.0f),
          maxAgents(50000),
          enablePhysics(true),
          enableVisualization(true),
          enableSerialization(true) {}
};

// ============================================================================
// Task Definition
// ============================================================================

struct Task {
    uint64_t id;
    Vector3 location;
    TaskType type;
    float estimatedDuration;
    float priority;                         // 0.0 - 1.0
    int minAgentsRequired;
    bool isComplete;
    
    Task()
        : id(0), type(TaskType::GATHER),
          estimatedDuration(0.0f), priority(0.5f),
          minAgentsRequired(1), isComplete(false) {}
};

// ============================================================================
// Experiment Framework
// ============================================================================

struct ParameterRange {
    const char* name;
    float minValue;
    float maxValue;
    float step;
};

struct ExperimentConfig {
    const char* hypothesis;
    std::vector<ParameterRange> parameterRanges;
    uint32_t durationSteps;
    float timestepSize;
    uint32_t trialsPerConfiguration;
    
    ExperimentConfig()
        : hypothesis(""),
          durationSteps(10000),
          timestepSize(0.005f),
          trialsPerConfiguration(1) {}
};

struct ExperimentResult {
    ExperimentConfig config;
    std::vector<float> parameterValues;
    std::vector<float> metrics;
    float successScore;                     // 0.0 - 1.0
    const char* observations;
    uint64_t executionTimeMs;
    
    ExperimentResult()
        : successScore(0.0f), observations(""),
          executionTimeMs(0) {}
};

// ============================================================================
// Force Definition
// ============================================================================

enum class ForceType : uint8_t {
    GRAVITY = 0,
    MAGNETIC = 1,
    CHEMICAL_BOND = 2,
    DRAG = 3,
    ELECTROSTATIC = 4,
    CUSTOM = 5,
};

struct Force {
    ForceType type;
    Vector3 direction;
    float magnitude;
    float range;
    float decay;                            // Attenuation factor
    
    Force()
        : type(ForceType::CUSTOM),
          magnitude(0.0f), range(10.0f),
          decay(1.0f) {}
};

// ============================================================================
// Swarm Metrics
// ============================================================================

struct SwarmMetrics {
    uint32_t agentCount;
    float averageEnergy;
    float energyVariance;
    float averageTemperature;
    float swarmCohesion;                    // 0.0 - 1.0
    float averageVelocity;
    uint32_t activeAgents;
    uint32_t damagedAgents;
    
    SwarmMetrics()
        : agentCount(0), averageEnergy(0.0f),
          energyVariance(0.0f), averageTemperature(300.0f),
          swarmCohesion(0.0f), averageVelocity(0.0f),
          activeAgents(0), damagedAgents(0) {}
};

} // namespace NanoSim

#endif // NANO_SIM_TYPES_H
