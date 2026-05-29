# Swift Modules Architecture & Specifications

## Module Ecosystem Overview

The Omniverse Engine Swift ecosystem consists of 8 core frameworks plus companion apps, organized in a layered dependency structure.

```
┌─────────────────────────────────────────────────────────────┐
│              iOS/macOS/visionOS Applications                 │
│  (Control Center, Creator Console, Spatial UI)               │
└────┬────────────────────┬─────────────────────┬──────────────┘
     │                    │                     │
     ▼                    ▼                     ▼
┌──────────────────┐ ┌──────────────┐ ┌────────────────────┐
│  Core Frameworks │ │ UI Frameworks│ │ Specialized Modules│
├──────────────────┤ ├──────────────┤ ├────────────────────┤
│OmniverseMobile   │ │VisionSpatial │ │AppleSecurityLayer  │
│Core              │ │UI            │ ├────────────────────┤
├──────────────────┤ ├──────────────┤ │OmniverseSyncFrame  │
│StrongholdControl │ │              │ ├────────────────────┤
│Center            │ │              │ │PortableWorldMgr   │
├──────────────────┤ ├──────────────┤ ├────────────────────┤
│SpatialSimulation │ │              │ │AIWorldConsole      │
│Viewer            │ │              │ └────────────────────┘
└────┬─────────────┘ └──────┬───────┘
     │                      │
     └──────────┬───────────┘
                ▼
     ┌──────────────────────┐
     │ Foundation Packages  │
     ├──────────────────────┤
     │ Unreal Bridge APIs   │
     │ HTTP Client Layer    │
     │ WebSocket Manager    │
     │ Data Models          │
     │ Error Handling       │
     └──────────────────────┘
```

---

## Module 1: OmniverseMobileCore

**Purpose**: Foundation framework containing core APIs, data models, and communication infrastructure.

**Package Dependencies**:
- Foundation
- Combine
- Network

**Exports**:
```swift
// Core Models
public struct OmniverseWorld { }
public struct SimulationState { }
public struct AIGenerationRequest { }
public struct NPC { }
public struct Avatar { }

// API Clients
public class OmniverseAPIClient { }
public class SimulationService { }
public class AIService { }
public class WorldService { }

// Networking
public class WebSocketManager { }
public protocol APIEndpoint { }

// Data Access
public class WorldRepository { }
public class SaveStateRepository { }
public class LocalDataManager { }

// Error Handling
public enum OmniverseError: Error { }

// Utilities
public class OmniverseLogger { }
public struct PerformanceMetrics { }
```

**Submodules**:
- `OmniverseMobileCore.Models` - Data structures
- `OmniverseMobileCore.API` - Network communication
- `OmniverseMobileCore.Storage` - Local persistence
- `OmniverseMobileCore.Networking` - WebSocket & HTTP
- `OmniverseMobileCore.Logging` - Telemetry

**Key Classes & Structs**:

### OmniverseAPIClient
```swift
public actor OmniverseAPIClient: Sendable {
    public init(baseURL: URL, sessionConfig: URLSessionConfiguration)
    
    public func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T
    public func stream<T: Decodable>(_ endpoint: APIEndpoint) -> AsyncThrowingStream<T, Error>
    
    public var isConnected: Bool { get }
    public var lastError: Error? { get }
}
```

### WebSocketManager
```swift
public class WebSocketManager: NSObject, URLSessionWebSocketDelegate, ObservableObject {
    @Published public var isConnected: Bool
    
    public init(url: URL)
    public func connect() async throws
    public func disconnect()
    public func send<T: Encodable>(_ message: T) async throws
    public func receive<T: Decodable>(as type: T.Type) -> AsyncThrowingStream<T, Error>
}
```

**Testing Strategy**:
- Mock API responses with URLProtocol
- Test error handling and retry logic
- Validate model serialization/deserialization
- Performance benchmarks for concurrent requests

**Documentation**:
- DocC documentation for all public APIs
- Code examples for common patterns
- Migration guide for future versions

---

## Module 2: StrongholdControlCenter

**Purpose**: iOS/iPadOS app for managing Stronghold access, universe switching, and security.

**Target Platforms**: iOS 16.0+, iPadOS 16.0+

**Key Features**:
- Biometric authentication
- Universe/Stronghold selector
- Access control management
- Security audit logging
- Account settings

**App Architecture**:
```
StrongholdControlCenter (App)
├── Authentication View
│   ├── BiometricPrompt
│   ├── CredentialEntry
│   └── SessionManagement
├── Stronghold View
│   ├── UniverseSelector
│   ├── AccessPanel
│   ├── AuditLog
│   └── Settings
└── AppDelegate
    ├── App Lifecycle
    ├── Deep Linking
    └── Background Tasks
```

**SwiftUI Views**:
```swift
struct AuthenticationView: View { }
struct StrongholdSelectorView: View { }
struct AccessControlView: View { }
struct AuditLogView: View { }
struct SettingsView: View { }
```

**Core Classes**:

### AuthenticationManager
```swift
@MainActor
public class AuthenticationManager: ObservableObject {
    @Published public var isAuthenticated: Bool
    @Published public var currentUser: User?
    
    public func authenticateWithBiometric() async throws -> AuthToken
    public func logout() async throws
    public func refreshToken() async throws
}
```

### StrongholdManager
```swift
@MainActor
public class StrongholdManager: ObservableObject {
    @Published public var currentStronghold: Stronghold?
    @Published public var availableUniverses: [Universe]
    
    public func switchUniverse(_ universe: Universe) async throws
    public func getAccessRules(for stronghold: Stronghold) async throws -> [AccessRule]
    public func updateAccessRule(_ rule: AccessRule) async throws
}
```

**Data Models**:
```swift
public struct Stronghold: Identifiable, Codable {
    public let id: UUID
    public let name: String
    public let createdAt: Date
    public var accessLevel: AccessLevel
}

public enum AccessLevel: String, Codable {
    case owner, admin, moderator, user, guest
}

public struct AccessRule: Identifiable, Codable {
    public let id: UUID
    public let userId: UUID
    public let accessLevel: AccessLevel
    public let grantedAt: Date
    public var expiresAt: Date?
}
```

**Security**:
- BiometricAuthentication + LAContext
- Keychain for token storage
- Local authentication caching (15min)
- Network security with TLS pinning

**Persistence**:
- UserDefaults for preferences
- Keychain for credentials
- Core Data for audit logs
- CloudKit for cloud backup

---

## Module 3: SpatialSimulationViewer

**Purpose**: Real-time 3D/AR viewer for simulation streaming and cinematic playback.

**Target Platforms**: iOS 16.0+, visionOS 1.0+

**Key Features**:
- HLS stream playback
- Cinematic viewer with controls
- AR overlay of simulation data
- Performance metrics display
- Screen recording

**Architecture**:
```swift
public struct SimulationViewerConfig {
    public var streamURL: URL
    public var qualityPreference: StreamQuality
    public var arOverlayEnabled: Bool
    public var performanceMonitoring: Bool
}

public class SimulationViewerController: UIViewController {
    public func startStreaming() async throws
    public func pauseStreaming()
    public func changeQuality(_ quality: StreamQuality) async
    public func recordSession() -> URL
}
```

**SwiftUI Integration**:
```swift
struct SimulationViewerView: UIViewControllerRepresentable {
    var config: SimulationViewerConfig
    
    func makeUIViewController(context: Context) -> SimulationViewerController
    func updateUIViewController(_ uiViewController: SimulationViewerController, context: Context)
}
```

**Streaming Protocol**:
- **Primary**: HLS (HTTP Live Streaming)
- **Fallback**: RTMP with transcoding
- **Bitrates**: 720p@30fps → 4K@60fps adaptive
- **Latency**: < 2 seconds end-to-end

**AR Overlay System**:
- RealityKit for spatial anchors
- ARKit for device tracking
- Metal shaders for custom rendering
- World-space UI placement

**Performance**:
- 60 FPS on iPhone 12+
- 90 FPS on Vision Pro
- < 500MB RAM footprint
- Battery: 4+ hours continuous playback

---

## Module 4: AIWorldConsole

**Purpose**: Swift service layer for AI model orchestration and monitoring.

**Platforms**: iOS, macOS, visionOS

**Core Services**:

### AIModelManager
```swift
public actor AIModelManager {
    public func loadModel(_ identifier: String) async throws -> MLModel
    public func listAvailableModels() async throws -> [ModelInfo]
    public func downloadModel(_ identifier: String) -> AsyncThrowingStream<Progress, Error>
    public func cacheModel(_ model: MLModel, ttl: TimeInterval)
    public func getModelMetrics() -> ModelPerformanceMetrics
}
```

### InferenceService
```swift
public actor InferenceService {
    public func runInference<Input, Output>(
        model: MLModel,
        input: Input
    ) async throws -> Output
    
    public func batchInference<Input, Output>(
        model: MLModel,
        inputs: [Input]
    ) async throws -> [Output]
    
    public var metrics: InferenceMetrics { get }
}
```

### HuggingFaceClient
```swift
public class HuggingFaceClient: APIClient {
    public func searchModels(query: String) async throws -> [HFModelInfo]
    public func downloadModel(_ modelId: String) async throws -> URL
    public func runInference(modelId: String, input: String) async throws -> String
    public func listLocalModels() -> [String]
}
```

**Features**:
- Local CoreML inference with Neural Engine
- Remote inference via Hugging Face API
- Intelligent routing (local vs cloud)
- Caching and versioning
- Performance monitoring
- Cost tracking

**Monitoring Dashboard**:
```swift
struct AIMonitoringDashboard: View {
    @StateObject var monitor = AIMonitor()
    
    var body: some View {
        VStack {
            ModelPerformanceChart(metrics: monitor.metrics)
            LatencyDistribution(samples: monitor.latencySamples)
            ResourceUtilizationView(cpu: monitor.cpuUsage, memory: monitor.memoryUsage)
            InferenceHistoryList(history: monitor.history)
        }
    }
}
```

---

## Module 5: PortableWorldManager

**Purpose**: File-based world archive management and synchronization.

**Platforms**: iOS, macOS, visionOS

**Core Classes**:

### WorldArchive
```swift
public struct WorldArchive {
    public let id: UUID
    public let name: String
    public let version: String
    public let size: Int64
    public let createdAt: Date
    public let lastModifiedAt: Date
    public var metadata: ArchiveMetadata
}

public class WorldArchiveManager {
    public func createArchive(from world: OmniverseWorld) async throws -> URL
    public func extractArchive(at path: URL) async throws -> OmniverseWorld
    public func compressArchive(at path: URL) -> AsyncThrowingStream<Progress, Error>
    public func validateArchive(at path: URL) async throws -> ValidationResult
}
```

### ExternalStorageManager
```swift
public class ExternalStorageManager: NSObject, ObservableObject {
    @Published public var detectedDevices: [ExternalStorageDevice]
    @Published public var transferProgress: Progress?
    
    public func scanForExternalStorage() async throws
    public func transferWorld(_ world: OmniverseWorld, to device: ExternalStorageDevice) -> AsyncThrowingStream<Progress, Error>
    public func restoreWorld(from device: ExternalStorageDevice) async throws -> OmniverseWorld
}
```

### IncrementalSyncEngine
```swift
public class IncrementalSyncEngine {
    public func computeDelta(from: OmniverseWorld, to: OmniverseWorld) -> WorldDelta
    public func applyDelta(_ delta: WorldDelta, to world: OmniverseWorld) throws -> OmniverseWorld
    public func createBackup(of world: OmniverseWorld) async throws -> URL
    public func scheduleIncrementalBackup() -> AsyncThrowingStream<BackupEvent, Error>
}
```

**Archive Format**:
```
.omniverse (CBOR-encoded directory structure)
├── metadata.json
├── world/
│   ├── state.cbor
│   ├── entities.cbor
│   ├── terrain.bin
│   └── assets/
└── checksums.sha256
```

**Performance**:
- Compression: LZ4 for speed, ZSTD for ratio
- USB 3.0 transfer: 50GB in < 30 minutes
- Incremental sync: Only 5-10% of world size
- Verification: Parallel SHA256 checksums

---

## Module 6: OmniverseSyncFramework

**Purpose**: Cross-device synchronization with conflict resolution.

**Platforms**: iOS, macOS, visionOS

**Core Protocols**:

### SyncEngine
```swift
public protocol SyncEngine: Actor {
    associatedtype State: Codable
    
    func sync(_ state: State) async throws
    func subscribe(to changes: StateChange) -> AsyncStream<State>
    func getConflictResolution(strategy: ConflictResolutionStrategy) -> ConflictResolver
}
```

### CloudKitSyncManager
```swift
public actor CloudKitSyncManager: SyncEngine {
    public typealias State = OmniverseWorld
    
    public func sync(_ state: OmniverseWorld) async throws
    public func subscribe(to changes: StateChange) -> AsyncStream<OmniverseWorld>
    public func getConflictResolution(strategy: ConflictResolutionStrategy) -> ConflictResolver
}
```

### MultipeerConnectivityManager
```swift
public class MultipeerConnectivityManager: NSObject, ObservableObject {
    @Published public var connectedPeers: [MCPeerID]
    @Published public var isAdvertising: Bool
    
    public func startAdvertising() throws
    public func stopAdvertising()
    public func sendToNearbyPeers<T: Encodable>(_ data: T) throws
    public func receiveFromPeers<T: Decodable>(as type: T.Type) -> AsyncThrowingStream<(T, MCPeerID), Error>
}
```

**Sync Strategies**:
- **CloudKit**: Primary cloud sync with automatic conflict resolution
- **MultipeerConnectivity**: Local device network sync
- **Offline-first**: Queue-based sync with eventual consistency
- **Last-write-wins**: Simple timestamp-based resolution
- **Custom**: User-defined conflict resolution logic

**Conflict Resolution**:
```swift
public protocol ConflictResolver {
    func resolve(local: OmniverseWorld, remote: OmniverseWorld, base: OmniverseWorld) -> OmniverseWorld
}

public struct LastWriteWinsResolver: ConflictResolver {
    public func resolve(local: OmniverseWorld, remote: OmniverseWorld, base: OmniverseWorld) -> OmniverseWorld {
        remote.lastModifiedAt > local.lastModifiedAt ? remote : local
    }
}
```

---

## Module 7: VisionSpatialUI

**Purpose**: visionOS-native spatial user interface framework.

**Target Platform**: visionOS 1.0+

**Core Components**:

### SpatialWindow
```swift
public struct SpatialWindow: View {
    public var title: String
    public var content: AnyView
    public var size: SIMD3<Float>
    public var position: SIMD3<Float>
    
    var body: some View {
        // RealityKit spatial container
    }
}
```

### GestureInteractor
```swift
public class GestureInteractor: NSObject, ObservableObject {
    @Published public var detectedGestures: [SpatialGesture]
    
    public func recognizeHandGestures() -> AsyncStream<HandGestureEvent>
    public func recognizeEyeGaze() -> AsyncStream<GazePoint>
    public func listenForVoiceCommands(vocabulary: [String]) -> AsyncThrowingStream<VoiceCommand, Error>
}
```

### SpatialMetricsView
```swift
struct SpatialMetricsView: View {
    var metrics: SimulationMetrics
    
    var body: some View {
        RealityView { content in
            // Render 3D metrics visualization
        }
    }
}
```

**Input Methods**:
- Hand gesture recognition (pinch, grab, rotate)
- Eye-gaze tracking and dwell interaction
- Voice commands with NLU
- Haptic feedback for confirmation

**Performance**:
- 90 FPS motion-to-photon
- < 15ms latency for gestures
- < 100ms voice recognition latency
- Battery: 3+ hours continuous use

---

## Module 8: AppleSecurityLayer

**Purpose**: Unified security, authentication, and encryption framework.

**Platforms**: iOS, macOS, visionOS

**Core Components**:

### BiometricAuthentication
```swift
public class BiometricAuthenticator {
    public func authenticate() async throws -> LAContext
    public func evaluatePolicy(_ policy: LAPolicy) async throws -> Bool
    public var availableBiometrics: [BiometricType] { get }
}
```

### KeychainManager
```swift
public class KeychainManager {
    public func store<T: Codable>(_ value: T, forKey key: String, accessibility: KeychainAccessibility) throws
    public func retrieve<T: Codable>(as type: T.Type, forKey key: String) throws -> T?
    public func delete(key: String) throws
    public func update<T: Codable>(_ value: T, forKey key: String) throws
}
```

### SecureEnclaveIntegration
```swift
public class SecureEnclaveManager {
    public func generateKeyPair() throws -> SecureEnclaveKey
    public func sign(_ data: Data, with key: SecureEnclaveKey) throws -> Data
    public func verify(_ signature: Data, for data: Data, with key: SecureEnclaveKey) throws -> Bool
}
```

### EncryptionManager
```swift
public class EncryptionManager {
    public func encrypt(_ data: Data, with key: SymmetricKey) throws -> Data
    public func decrypt(_ encryptedData: Data, with key: SymmetricKey) throws -> Data
    public func generateSymmetricKey(algorithm: SymmetricKeyAlgorithm) -> SymmetricKey
}
```

**Security Features**:
- Face ID / Touch ID authentication
- Secure Enclave key generation and signing
- Keychain credential storage
- AES-256 encryption for sensitive data
- TLS certificate pinning
- Secure random number generation

**Compliance**:
- OWASP Top 10 mitigations
- NIST cryptographic standards
- HIPAA/GDPR privacy requirements
- iOS App Store security review

---

## Companion Applications

### iOS Control Center App
- Integrates all 8 frameworks
- Primary user-facing interface
- Real-time dashboard
- Simulation monitoring
- Creator tools

### macOS Creator Suite
- Advanced world editor
- Portable world management
- Team collaboration
- Batch operations
- Developer console

### visionOS Spatial App
- Immersive spatial UI (Module 7)
- Hand and eye interaction
- Holographic visualization
- Voice-controlled commands

---

## Module Dependencies Summary

```
AppleSecurityLayer (Bottom)
    ↑
OmniverseMobileCore
    ↑ ↑ ↑ ↑ ↑
    │ │ │ │ └─ VisionSpatialUI
    │ │ │ └───── PortableWorldManager
    │ │ └─────── OmniverseSyncFramework
    │ └───────── AIWorldConsole
    └─────────── StrongholdControlCenter
                 └─ SpatialSimulationViewer
                    ↓
            iOS/macOS/visionOS Apps
```

## Development Guidelines

### Code Style
- Swift Naming Conventions (API Design Guidelines)
- SwiftLint for automated checks
- 80-char line limit for readability
- MARK comments for logical sections

### Testing Requirements
- 80%+ code coverage per module
- Unit tests with XCTest
- Integration tests with mock APIs
- UI tests with XCUITest for apps
- Performance tests with Measure

### Documentation
- DocC documentation for all public APIs
- Code comments for complex logic
- Examples and tutorials
- Changelog entries for releases

### Version Strategy
- Semantic Versioning (Major.Minor.Patch)
- Compatibility with multiple OS versions
- Deprecation warnings for API changes
- Regular minor releases (quarterly)

---

**Last Updated**: 2026-05-29  
**Next Review**: 2026-06-30
