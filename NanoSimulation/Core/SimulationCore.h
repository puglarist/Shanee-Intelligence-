#pragma once

#include "Types.h"
#include <vector>
#include <cstring>

namespace NanoSim {

// ============================================================================
// Voxel Grid - 3D Grid-based Material Representation
// ============================================================================

class VoxelGrid {
public:
    VoxelGrid(uint32_t size);
    ~VoxelGrid();
    
    // Grid access
    MaterialVoxel& GetVoxel(uint32_t x, uint32_t y, uint32_t z);
    const MaterialVoxel& GetVoxel(uint32_t x, uint32_t y, uint32_t z) const;
    MaterialVoxel& GetVoxelByIndex(uint32_t index);
    
    // Grid dimensions
    uint32_t GetSize() const { return gridSize; }
    uint32_t GetTotalVoxels() const { return gridSize * gridSize * gridSize; }
    
    // Queries
    std::vector<MaterialVoxel*> GetNeighbors(uint32_t x, uint32_t y, uint32_t z, uint32_t radius);
    MaterialType GetMaterialAt(uint32_t x, uint32_t y, uint32_t z) const;
    
    // Updates
    void SetMaterial(uint32_t x, uint32_t y, uint32_t z, MaterialType type);
    void UpdateVoxelState(uint32_t x, uint32_t y, uint32_t z, float deltaTime);
    void ApplyEnergy(uint32_t x, uint32_t y, uint32_t z, float energyAmount);
    void SetTemperature(uint32_t x, uint32_t y, uint32_t z, float tempK);
    
    // Bulk operations
    void UpdateAllStates(float deltaTime);
    void ClearGrid();
    void ApplyThermalDamping(float dampingFactor);
    
    // Utility
    uint32_t LinearIndex(uint32_t x, uint32_t y, uint32_t z) const;
    void IndexToCoords(uint32_t index, uint32_t& x, uint32_t& y, uint32_t& z) const;
    bool IsInBounds(uint32_t x, uint32_t y, uint32_t z) const;
    
private:
    uint32_t gridSize;
    std::vector<MaterialVoxel> voxels;
    
    // Bounds checking
    static constexpr uint32_t MAX_COORD_DIFF = 2;  // For neighbor queries
};

// ============================================================================
// Assembly Rules Engine
// ============================================================================

struct AssemblyRule {
    MaterialType sourceMaterial;
    MaterialType targetMaterial;
    float energyRequired;
    float probability;                      // Per timestep
    std::vector<MaterialType> catalysts;
    
    AssemblyRule()
        : sourceMaterial(MaterialType::EMPTY),
          targetMaterial(MaterialType::EMPTY),
          energyRequired(1.0f),
          probability(0.1f) {}
};

class AssemblyEngine {
public:
    AssemblyEngine();
    
    // Rule management
    void AddRule(const AssemblyRule& rule);
    void RemoveRule(uint32_t ruleIndex);
    const std::vector<AssemblyRule>& GetRules() const { return rules; }
    
    // Assembly processing
    void ProcessAssembly(VoxelGrid& grid, float deltaTime);
    void ApplyRule(VoxelGrid& grid, uint32_t x, uint32_t y, uint32_t z, 
                   const AssemblyRule& rule);
    
    // Statistics
    uint32_t GetTransformationCount() const { return transformationCount; }
    void ResetStats() { transformationCount = 0; }
    
private:
    std::vector<AssemblyRule> rules;
    uint32_t transformationCount;
};

// ============================================================================
// Octree - Spatial Partitioning for Agents
// ============================================================================

class OctreeNode {
public:
    OctreeNode(const Vector3& min, const Vector3& max, int depth);
    ~OctreeNode();
    
    // Agent management
    void Insert(NanobotAgent* agent);
    void Remove(NanobotAgent* agent);
    void Update(NanobotAgent* agent);
    
    // Queries
    std::vector<NanobotAgent*> QueryRadius(const Vector3& center, float radius) const;
    std::vector<NanobotAgent*> QueryBox(const Vector3& min, const Vector3& max) const;
    
    // Utility
    bool IsLeaf() const;
    void Clear();
    
private:
    static constexpr int MAX_AGENTS_PER_NODE = 64;
    static constexpr int MAX_DEPTH = 16;
    
    Vector3 boundsMin, boundsMax;
    int depth;
    
    std::vector<NanobotAgent*> agents;      // Empty if internal node
    OctreeNode* children[8];
    
    void Split();
    int GetChildIndex(const Vector3& pos) const;
};

// ============================================================================
// Physics Engine - Force Calculation and Integration
// ============================================================================

class PhysicsEngine {
public:
    PhysicsEngine();
    
    // Configuration
    void SetGravity(float magnitude);
    void SetDamping(float dampingFactor);
    void SetCollisionEnabled(bool enabled);
    
    // Force application
    void ApplyForce(NanobotAgent& agent, const Force& force);
    void ApplyForces(NanobotAgent& agent, const std::vector<Force>& forces);
    
    // Physics update
    void Update(std::vector<NanobotAgent>& agents, float deltaTime);
    void IntegrateVelocity(NanobotAgent& agent, float deltaTime);
    void ApplyDamping(NanobotAgent& agent);
    
    // Collision detection and response
    void DetectCollisions(std::vector<NanobotAgent>& agents, OctreeNode& octree);
    void ResolveCollision(NanobotAgent& agent1, NanobotAgent& agent2);
    
    // Energy management
    void UpdateEnergy(std::vector<NanobotAgent>& agents, float deltaTime);
    float GetTotalSystemEnergy(const std::vector<NanobotAgent>& agents) const;
    
private:
    float gravityMagnitude;
    float dampingFactor;
    bool collisionEnabled;
    
    static constexpr float ENERGY_LOSS_RATE = 0.05f;    // 5% per frame
    static constexpr float MIN_VELOCITY = 0.001f;
};

} // namespace NanoSim

#endif // NANO_SIM_VOXEL_GRID_H
