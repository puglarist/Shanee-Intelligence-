#pragma once

#include "NanoSimulationEngine.h"
#include <vector>

namespace NanoSim {

// ============================================================================
// Experiment Framework
// ============================================================================

class ExperimentFramework {
public:
    ExperimentFramework();
    
    // Experiment execution
    ExperimentResult RunExperiment(const ExperimentConfig& config);
    
    // Batch execution
    std::vector<ExperimentResult> RunParameterSweep(const ExperimentConfig& baseConfig,
                                                    const std::vector<ParameterRange>& ranges);
    
    // Results management
    void SaveResult(const ExperimentResult& result);
    std::vector<ExperimentResult> GetResults() const { return results; }
    
    // Analysis
    ExperimentResult GetBestResult() const;
    float CalculateSuccessRate() const;
    void PrintResultsSummary() const;
    
private:
    std::vector<ExperimentResult> results;
    NanoSimulationEngine* experimentEngine;
    
    void SetupExperiment(NanoSimulationEngine& engine, const ExperimentConfig& config);
    ExperimentResult CollectResults(NanoSimulationEngine& engine, const ExperimentConfig& config);
};

// ============================================================================
// R&D Hypothesis Database
// ============================================================================

struct Hypothesis {
    uint64_t id;
    const char* description;
    uint64_t createdAt;
    uint64_t testedAt;
    ExperimentResult result;
    bool isVerified;
    float confidenceScore;  // 0.0 - 1.0
};

class HypothesisDatabase {
public:
    HypothesisDatabase();
    
    // Hypothesis management
    uint64_t CreateHypothesis(const char* description);
    void RecordTest(uint64_t hypothesisId, const ExperimentResult& result);
    const Hypothesis* GetHypothesis(uint64_t id) const;
    
    // Queries
    std::vector<Hypothesis> GetVerifiedHypotheses() const;
    std::vector<Hypothesis> GetUntestedHypotheses() const;
    uint32_t GetTotalHypotheses() const { return hypotheses.size(); }
    
    // Statistics
    float GetAverageConfidence() const;
    uint32_t GetVerificationRate() const;
    
private:
    std::vector<Hypothesis> hypotheses;
    uint64_t nextHypothesisId;
};

// ============================================================================
// Results Analyzer
// ============================================================================

struct AnalysisReport {
    float successRate;
    float averageMetric;
    float variance;
    const char* topFinding;
    std::vector<const char*> recommendations;
};

class ResultsAnalyzer {
public:
    ResultsAnalyzer();
    
    // Analysis
    AnalysisReport AnalyzeResults(const std::vector<ExperimentResult>& results);
    AnalysisReport AnalyzeTrend(const std::vector<ExperimentResult>& results);
    
    // Single result analysis
    bool IsResultSignificant(const ExperimentResult& result, float threshold = 0.75f) const;
    float CalculateConfidence(const ExperimentResult& result) const;
    
    // Reporting
    void GenerateReport(const std::vector<ExperimentResult>& results);
    
private:
    static constexpr float SIGNIFICANCE_THRESHOLD = 0.75f;
};

// ============================================================================
// Material Discovery System
// ============================================================================

struct DiscoveredMaterial {
    uint64_t discoveryId;
    MaterialProperties properties;
    uint64_t discoveredAt;
    ExperimentResult originExperiment;
    bool isPatented;
};

class MaterialDiscoverySystem {
public:
    MaterialDiscoverySystem();
    
    // Discovery tracking
    void RecordDiscovery(const MaterialProperties& properties, 
                        const ExperimentResult& originExperiment);
    
    // Queries
    const DiscoveredMaterial* GetDiscovery(uint64_t discoveryId) const;
    std::vector<DiscoveredMaterial> GetDiscoveriesSince(uint64_t timestamp) const;
    uint32_t GetTotalDiscoveries() const { return discoveries.size(); }
    
    // Material library
    void AddToLibrary(const MaterialProperties& props);
    const std::vector<MaterialProperties>& GetMaterialLibrary() const { return materialLibrary; }
    
private:
    std::vector<DiscoveredMaterial> discoveries;
    std::vector<MaterialProperties> materialLibrary;
    uint64_t nextDiscoveryId;
};

// ============================================================================
// Integration with Stronghold Sandbox
// ============================================================================

class StrongholdSandbox {
public:
    StrongholdSandbox();
    ~StrongholdSandbox();
    
    // Sandbox management
    void CreateIsolatedSimulation(const SimulationConfig& config);
    void DestroyIsolatedSimulation();
    
    // Experiment execution
    ExperimentResult ExecuteExperiment(const ExperimentConfig& config);
    std::vector<ExperimentResult> ExecuteExperimentBatch(
        const std::vector<ExperimentConfig>& configs);
    
    // Resource limits
    void SetMemoryLimit(uint64_t limitBytes);
    void SetTimeLimit(uint32_t limitSeconds);
    void SetStepLimit(uint32_t steps);
    
    // State management
    bool IsRunning() const { return isRunning; }
    float GetProgress() const { return executionProgress; }
    
private:
    std::unique_ptr<NanoSimulationEngine> sandboxEngine;
    bool isRunning;
    float executionProgress;
    
    uint64_t memoryLimitBytes;
    uint32_t timeLimitSeconds;
    uint32_t stepLimit;
};

// ============================================================================
// World Engine Integration
// ============================================================================

class WorldEngineIntegration {
public:
    WorldEngineIntegration();
    
    // Material propagation to world
    void PropagateMaterialDiscovery(const DiscoveredMaterial& discovery);
    void PropagateEnergyInnovation(float energyDensity);
    void PropagateWeaponTechnology(const MaterialProperties& props);
    
    // World event triggers
    void TriggerTechAdvanceEvent(const char* materialName);
    void UpdateResourceAvailability(const char* resourceName, float availability);
    
private:
    // Would connect to actual world engine
    // For now, placeholder for integration points
};

} // namespace NanoSim

#endif // NANO_SIM_RND_FRAMEWORK_H
