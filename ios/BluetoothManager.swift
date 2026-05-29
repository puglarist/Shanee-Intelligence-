import Foundation
import CoreBluetooth
import Combine
import os.log

// MARK: - Models
struct DiscoveredDevice: Identifiable {
    var id: String { uuid }
    let uuid: String
    let name: String
    let rssi: Int
    let timestamp: Date
}

// MARK: - Bluetooth Manager
@MainActor
class BluetoothManager: NSObject, ObservableObject, CBCentralManagerDelegate, CBPeripheralDelegate {
    @Published var isConnected = false
    @Published var isScanning = false
    @Published var discoveredDevices: [DiscoveredDevice] = []
    @Published var commandQueue: [String] = []
    @Published var lastUpdate: String?
    @Published var autoConnectEnabled = true
    @Published var showRSSI = true
    
    private var centralManager: CBCentralManager!
    private var connectedPeripheral: CBPeripheral?
    private var commandCharacteristic: CBCharacteristic?
    private var stateCharacteristic: CBCharacteristic?
    
    private let logger = Logger(subsystem: "com.omniverse.remote", category: "Bluetooth")
    
    // MARK: - Initialization
    override init() {
        super.init()
        self.centralManager = CBCentralManager(delegate: self, queue: .main)
    }
    
    // MARK: - Public Methods
    func startDiscovery() {
        guard centralManager.state == .poweredOn else {
            logger.warning("Bluetooth is not powered on")
            return
        }
        
        isScanning = true
        discoveredDevices.removeAll()
        
        // Scan for Omniverse services
        let omniverseServiceUUID = CBUUID(string: "OmniverseService")
        centralManager.scanForPeripherals(withServices: [omniverseServiceUUID], options: nil)
        
        // Stop scanning after 30 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 30) {
            self.stopDiscovery()
        }
    }
    
    func stopDiscovery() {
        centralManager.stopScan()
        isScanning = false
    }
    
    func connect(to device: DiscoveredDevice) {
        guard let peripheral = discoveredDevices.first(where: { $0.uuid == device.uuid }) else {
            logger.error("Device not found: \(device.uuid)")
            return
        }
        
        // Create a CBPeripheral from the discovered device
        // In real implementation, store the actual peripheral during discovery
        logger.info("Attempting to connect to \(device.name)")
    }
    
    func disconnect() {
        guard let peripheral = connectedPeripheral else { return }
        centralManager.cancelPeripheralConnection(peripheral)
    }
    
    func sendCommand(_ command: String) {
        guard let characteristic = commandCharacteristic,
              let peripheral = connectedPeripheral else {
            commandQueue.append(command)
            logger.warning("Queued command (no connection): \(command)")
            return
        }
        
        let commandData = command.data(using: .utf8) ?? Data()
        peripheral.writeValue(commandData, for: characteristic, type: .withResponse)
        lastUpdate = ISO8601DateFormatter().string(from: Date())
        
        logger.info("Sent command: \(command)")
    }
    
    // MARK: - CBCentralManagerDelegate
    nonisolated func centralManagerDidUpdateState(_ central: CBCentralManager) {
        DispatchQueue.main.async {
            switch central.state {
            case .poweredOn:
                self.logger.info("Bluetooth powered on")
                if self.autoConnectEnabled {
                    self.startDiscovery()
                }
            case .poweredOff:
                self.logger.warning("Bluetooth powered off")
                self.isConnected = false
            case .unsupported:
                self.logger.error("Bluetooth not supported")
            case .unauthorized:
                self.logger.error("Bluetooth authorization denied")
            case .resetting:
                self.logger.info("Bluetooth resetting")
            case .unknown:
                self.logger.warning("Bluetooth state unknown")
            @unknown default:
                self.logger.warning("Unknown Bluetooth state")
            }
        }
    }
    
    nonisolated func centralManager(_ central: CBCentralManager,
                                   didDiscover peripheral: CBPeripheral,
                                   advertisementData: [String: Any],
                                   rssi RSSI: NSNumber) {
        DispatchQueue.main.async {
            let device = DiscoveredDevice(
                uuid: peripheral.identifier.uuidString,
                name: peripheral.name ?? "Unknown",
                rssi: RSSI.intValue,
                timestamp: Date()
            )
            
            if !self.discoveredDevices.contains(where: { $0.uuid == device.uuid }) {
                self.discoveredDevices.append(device)
                self.logger.info("Discovered device: \(device.name)")
            }
        }
    }
    
    nonisolated func centralManager(_ central: CBCentralManager,
                                   didConnect peripheral: CBPeripheral) {
        DispatchQueue.main.async {
            self.logger.info("Connected to \(peripheral.name ?? "Unknown")")
            self.isConnected = true
            self.connectedPeripheral = peripheral
            peripheral.delegate = self
            peripheral.discoverServices([CBUUID(string: "OmniverseService")])
            self.lastUpdate = ISO8601DateFormatter().string(from: Date())
        }
    }
    
    nonisolated func centralManager(_ central: CBCentralManager,
                                   didFailToConnect peripheral: CBPeripheral,
                                   error: Error?) {
        DispatchQueue.main.async {
            self.logger.error("Failed to connect: \(error?.localizedDescription ?? "Unknown error")")
            self.isConnected = false
        }
    }
    
    nonisolated func centralManager(_ central: CBCentralManager,
                                   didDisconnectPeripheral peripheral: CBPeripheral,
                                   error: Error?) {
        DispatchQueue.main.async {
            self.logger.warning("Disconnected from \(peripheral.name ?? "Unknown")")
            self.isConnected = false
            self.connectedPeripheral = nil
            self.commandQueue.removeAll()
        }
    }
    
    // MARK: - CBPeripheralDelegate
    nonisolated func peripheral(_ peripheral: CBPeripheral,
                              didDiscoverServices error: Error?) {
        guard let services = peripheral.services else { return }
        
        DispatchQueue.main.async {
            for service in services {
                if service.uuid.uuidString == "OmniverseService" {
                    peripheral.discoverCharacteristics(
                        [
                            CBUUID(string: "OmniverseCommand"),
                            CBUUID(string: "OmniverseState")
                        ],
                        for: service
                    )
                }
            }
        }
    }
    
    nonisolated func peripheral(_ peripheral: CBPeripheral,
                              didDiscoverCharacteristicsFor service: CBService,
                              error: Error?) {
        guard let characteristics = service.characteristics else { return }
        
        DispatchQueue.main.async {
            for characteristic in characteristics {
                if characteristic.uuid.uuidString == "OmniverseCommand" {
                    self.commandCharacteristic = characteristic
                    self.logger.info("Found command characteristic")
                }
                
                if characteristic.uuid.uuidString == "OmniverseState" {
                    self.stateCharacteristic = characteristic
                    if characteristic.properties.contains(.notify) {
                        peripheral.setNotifyValue(true, for: characteristic)
                    }
                    self.logger.info("Found state characteristic")
                }
            }
        }
    }
    
    nonisolated func peripheral(_ peripheral: CBPeripheral,
                              didUpdateValueFor characteristic: CBCharacteristic,
                              error: Error?) {
        guard let data = characteristic.value else { return }
        
        DispatchQueue.main.async {
            if let state = String(data: data, encoding: .utf8) {
                self.logger.debug("Received state: \(state)")
                self.lastUpdate = ISO8601DateFormatter().string(from: Date())
            }
        }
    }
}
