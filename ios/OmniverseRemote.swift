import SwiftUI
import CoreBluetooth

// MARK: - Main App Entry Point
@main
struct OmniverseRemoteApp: App {
    @StateObject private var bluetoothManager = BluetoothManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(bluetoothManager)
        }
    }
}

// MARK: - Main Content View
struct ContentView: View {
    @EnvironmentObject var bluetoothManager: BluetoothManager
    @State private var showSettings = false
    
    var body: some View {
        NavigationStack {
            VStack {
                // Connected Device Status
                HStack {
                    Image(systemName: bluetoothManager.isConnected ? "bluetooth.circle.fill" : "bluetooth.circle")
                        .foregroundColor(bluetoothManager.isConnected ? .blue : .gray)
                    
                    VStack(alignment: .leading) {
                        Text("Omniverse Engine")
                            .font(.headline)
                        Text(bluetoothManager.isConnected ? "Connected" : "Disconnected")
                            .font(.caption)
                            .foregroundColor(bluetoothManager.isConnected ? .green : .red)
                    }
                    
                    Spacer()
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(8)
                
                if bluetoothManager.isConnected {
                    ConnectedControlView()
                        .environmentObject(bluetoothManager)
                } else {
                    DeviceDiscoveryView()
                        .environmentObject(bluetoothManager)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("Omniverse Remote")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showSettings = true }) {
                        Image(systemName: "gear")
                    }
                }
            }
            .sheet(isPresented: $showSettings) {
                SettingsView()
                    .environmentObject(bluetoothManager)
            }
        }
    }
}

// MARK: - Device Discovery View
struct DeviceDiscoveryView: View {
    @EnvironmentObject var bluetoothManager: BluetoothManager
    @State private var isScanning = false
    
    var body: some View {
        VStack {
            if isScanning {
                ProgressView("Searching for devices...")
            } else {
                Button(action: startScan) {
                    Label("Scan for Devices", systemImage: "magnifyingglass")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
            
            if !bluetoothManager.discoveredDevices.isEmpty {
                List {
                    ForEach(bluetoothManager.discoveredDevices, id: \.uuid) { device in
                        Button(action: { connect(to: device) }) {
                            VStack(alignment: .leading) {
                                Text(device.name)
                                    .font(.headline)
                                Text("RSSI: \(device.rssi)")
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                        }
                    }
                }
            } else if !isScanning {
                VStack {
                    Image(systemName: "bluetooth")
                        .font(.largeTitle)
                        .foregroundColor(.gray)
                    Text("No devices found")
                        .foregroundColor(.gray)
                }
            }
        }
    }
    
    func startScan() {
        isScanning = true
        bluetoothManager.startDiscovery()
        DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
            isScanning = false
        }
    }
    
    func connect(to device: DiscoveredDevice) {
        bluetoothManager.connect(to: device)
    }
}

// MARK: - Connected Control View
struct ConnectedControlView: View {
    @EnvironmentObject var bluetoothManager: BluetoothManager
    
    var body: some View {
        VStack(spacing: 16) {
            // Simulation Controls
            GroupBox(label: Label("Simulation", systemImage: "play.fill")) {
                VStack(spacing: 12) {
                    HStack {
                        Button(action: { bluetoothManager.sendCommand("PAUSE") }) {
                            Label("Pause", systemImage: "pause.fill")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                        
                        Button(action: { bluetoothManager.sendCommand("PLAY") }) {
                            Label("Play", systemImage: "play.fill")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                    }
                    
                    HStack {
                        Button(action: { bluetoothManager.sendCommand("RESET") }) {
                            Label("Reset", systemImage: "arrow.counterclockwise")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                    }
                }
            }
            
            // View Controls
            GroupBox(label: Label("Camera", systemImage: "video")) {
                VStack(spacing: 12) {
                    HStack(spacing: 8) {
                        Button(action: { bluetoothManager.sendCommand("CAMERA_EARTH") }) {
                            Text("Earth")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                        
                        Button(action: { bluetoothManager.sendCommand("CAMERA_SPACE") }) {
                            Text("Space")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                        
                        Button(action: { bluetoothManager.sendCommand("CAMERA_FREE") }) {
                            Text("Free")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                    }
                }
            }
            
            // State Display
            GroupBox(label: Label("State", systemImage: "info.circle")) {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Text("Command Queue:")
                        Spacer()
                        Text("\(bluetoothManager.commandQueue.count)")
                            .fontWeight(.semibold)
                    }
                    
                    HStack {
                        Text("Last Update:")
                        Spacer()
                        Text(bluetoothManager.lastUpdate ?? "N/A")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                }
                .font(.caption)
            }
            
            Spacer()
        }
    }
}

// MARK: - Settings View
struct SettingsView: View {
    @EnvironmentObject var bluetoothManager: BluetoothManager
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationStack {
            VStack {
                Form {
                    Section("Bluetooth") {
                        Toggle("Auto-Connect", isOn: $bluetoothManager.autoConnectEnabled)
                        Toggle("Show RSSI", isOn: $bluetoothManager.showRSSI)
                    }
                    
                    Section("Simulation") {
                        Text("Speed: 1x")
                        Text("Quality: High")
                    }
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - Preview
#Preview {
    ContentView()
        .environmentObject(BluetoothManager())
}
