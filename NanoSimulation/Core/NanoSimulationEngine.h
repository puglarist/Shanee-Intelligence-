#pragma once

#include "SimulationCore.h"
#include <map>
#include <memory>

namespace NanoSim {

// ============================================================================
// Nanobot Agent Controller
// ============================================================================

class NanobotController {
public:
    NanobotController(NanobotAgent& agent);
    
    // Behavior control
    void UpdateBehavior(float deltaTime);
    void AssignTask(const Task& task);
    void MoveTo(const Vector3& target, float speed);
    void Work(float duration);
    void Rest(float duration);
    
    // State queries
    AgentState GetState() const { return agent.state; }
    bool IsIdle() const { return agent.state == AgentState::IDLE; }
    bool IsWorking() const { return agent.state == AgentState::WORKING; }
    
    // Energy management
    void ConsumeEnergy(float amount);
    void RestoreEnergy(float amount);
    bool HasEnergy(float required) const;
    
private:
    NanobotAgent& agent;
    Task currentTask;
    float taskProgress;
    float targetSpeed;
    Vector3 targetPosition;
};

// ============================================================================
// Swarm Behavior Manager
// ============================================================================

enum class SwarmPattern : uint8_t {
    DISPERSE = 0,           // Spread out
    CONCENTRATE = 1,        // Form dense cluster
    CONVOY = 2,             // Move in formation
    EMERGENT_SEARCH = 3,    // Stigmergy-based exploration
};

class SwarmBehavior {
public:
    SwarmBehavior();
    
    // Pattern control
    void SetPattern(SwarmPattern pattern);
    SwarmPattern GetPattern() const { return currentPattern; }
    
    // Update swarm
    void Update(std::vector<NanobotAgent>& agents, float deltaTime);
    
    // Individual force calculations
    Vector3 ComputeSeparation(const NanobotAgent& agent, 
                              const std::vector<NanobotAgent*>& neighbors) const;
    Vector3 ComputeAlignment(const NanobotAgent& agent,
                             const std::vector<NanobotAgent*>& neighbors) const;
    Vector3 ComputeCohesion(const NanobotAgent& agent,
                            const std::vector<NanobotAgent*>& neighbors) const;
    Vector3 ComputeTaskAttraction(const NanobotAgent& agent,
                                  const Vector3& taskLocation) const;
    
    // Metrics
    float CalculateCohesion(const std::vector<NanobotAgent>& agents) const;
    Vector3 CalculateCenterOfMass(const std::vector<NanobotAgent>& agents) const;
    
    // Configuration
    void SetWeights(float separation, float alignment, float cohesion, float task);
    
private:
    SwarmPattern currentPattern;
    float w_separation;
    float w_alignment;
    float w_cohesion;
    float w_task;
    
    static constexpr float DEFAULT_SEPARATION_RANGE = 2.0f;
    static constexpr float DEFAULT_COHESION_RANGE = 5.0f;
};

// ============================================================================
// Task Queue & Distribution
// ============================================================================

class TaskQueue {
public:
    TaskQueue();
    
    // Task management
    void AddTask(const Task& task);
    void RemoveTask(uint64_t taskId);
    void MarkTaskComplete(uint64_t taskId);
    
    // Task assignment
    Task* GetNextAvailableTask(const NanobotAgent& agent);
    std::vector<Task*> GetTasksInRadius(const Vector3& location, float radius);
    
    // Queries
    uint32_t GetPendingTaskCount() const;
    uint32_t GetTotalTaskCount() const;
    const std::vector<Task>& GetAllTasks() const { return allTasks; }
    
    // Clearing
    void Clear();
    
private:
    std::vector<Task> allTasks;
    std::vector<uint64_t> completedTasks;
    uint64_t nextTaskId;
};

// ============================================================================
// Main Nano Simulation Engine
// ============================================================================

class NanoSimulationEngine {
public:
    NanoSimulationEngine(const SimulationConfig& config);
    ~NanoSimulationEngine();
    
    // Initialization and cleanup
    bool Initialize();
    void Shutdown();
    
    // Main simulation loop
    void Update(float deltaTime);
    void Render();
    
    // Agent management
    NanobotAgent* CreateAgent(AgentType type, const Vector3& position);
    void DestroyAgent(uint64_t agentId);
    NanobotAgent* GetAgent(uint64_t agentId);
    const std::vector<NanobotAgent>& GetAllAgents() const { return agents; }
    uint32_t GetAgentCount() const { return agents.size(); }
    
    // Task management
    void AddTask(const Task& task);
    void DistributeTasks();
    
    // Grid access
    VoxelGrid& GetGrid() { return *voxelGrid; }
    
    // Statistics and metrics
    SwarmMetrics GetMetrics() const;
    float GetSimulationTime() const { return simulationTime; }
    uint32_t GetSimulationStep() const { return simulationStep; }
    
    // Speed control
    void SetSimulationSpeed(float speed);
    float GetSimulationSpeed() const { return config.simulationSpeed; }
    
    // Configuration access
    const SimulationConfig& GetConfig() const { return config; }
    
private:
    // Configuration
    SimulationConfig config;
    
    // Core systems
    std::unique_ptr<VoxelGrid> voxelGrid;
    std::unique_ptr<OctreeNode> spatialIndex;
    std::unique_ptr<PhysicsEngine> physicsEngine;
    std::unique_ptr<AssemblyEngine> assemblyEngine;
    std::unique_ptr<SwarmBehavior> swarmBehavior;
    std::unique_ptr<TaskQueue> taskQueue;
    
    // Agent management
    std::vector<NanobotAgent> agents;
    std::map<uint64_t, NanobotController*> agentControllers;
    uint64_t nextAgentId;
    
    // Simulation state
    float simulationTime;
    uint32_t simulationStep;
    float accumulatedTime;
    
    // Private methods
    void UpdateAgents(float deltaTime);
    void UpdateMaterials(float deltaTime);
    void RebuildSpatialIndex();
    void ComputeAgentMetrics();
    void ApplyBehaviors(float deltaTime);
};

} // namespace NanoSim

#endif // NANO_SIM_ENGINE_H
