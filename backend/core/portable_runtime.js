const path = require('path');
const fs = require('fs');
const os = require('os');
const debug = require('debug')('omniverse:portable');

/**
 * PortableRuntime - Manages paths and assets across different storage mediums
 * Supports: local filesystem, external drives, USB drives, cloud storage
 */
class PortableRuntime {
  constructor(config) {
    this.config = config;
    this.externalDrivePaths = [];
    this.storagePaths = [];
    this.assetCache = new Map();
    
    this.initialize();
  }

  initialize() {
    debug('Initializing PortableRuntime');
    
    // Detect available storage paths
    this.detectStoragePaths();
    
    // Set up fallback paths
    this.setupFallbackPaths();
    
    debug(`Available storage paths: ${this.storagePaths.join(', ')}`);
  }

  /**
   * Detect external drives and mount points
   */
  detectStoragePaths() {
    const platform = os.platform();
    
    // Add configured external drive path
    if (this.config.externalDrive.basePath) {
      this.storagePaths.push(this.config.externalDrive.basePath);
    }

    // Platform-specific detection
    if (platform === 'linux') {
      this.detectLinuxMounts();
    } else if (platform === 'darwin') {
      this.detectMacMounts();
    } else if (platform === 'win32') {
      this.detectWindowsDrives();
    }

    // Add fallback local path
    this.storagePaths.push(this.config.externalDrive.fallbackPath);
  }

  detectLinuxMounts() {
    try {
      const mounts = fs.readFileSync('/proc/mounts', 'utf8').split('\n');
      mounts.forEach(mount => {
        const parts = mount.split(' ');
        const device = parts[0];
        const path = parts[1];
        
        // Look for USB or external drives
        if ((device.includes('sd') || device.includes('nvme')) && 
            (path.includes('media') || path.includes('mnt'))) {
          this.storagePaths.push(path);
        }
      });
    } catch (error) {
      debug('Error detecting Linux mounts:', error.message);
    }
  }

  detectMacMounts() {
    try {
      const mounts = fs.readdirSync('/Volumes');
      mounts.forEach(mount => {
        if (mount !== 'Macintosh HD') {
          this.storagePaths.push(path.join('/Volumes', mount));
        }
      });
    } catch (error) {
      debug('Error detecting macOS mounts:', error.message);
    }
  }

  detectWindowsDrives() {
    // Windows drive letters C, D, E, etc.
    for (let code = 67; code <= 90; code++) {
      const drive = String.fromCharCode(code) + ':';
      const testPath = path.join(drive, 'omniverse');
      try {
        if (fs.existsSync(drive)) {
          this.storagePaths.push(drive);
        }
      } catch (error) {
        // Drive doesn't exist
      }
    }
  }

  setupFallbackPaths() {
    // Ensure fallback path exists
    const fallback = this.config.externalDrive.fallbackPath;
    if (!fs.existsSync(fallback)) {
      fs.mkdirSync(fallback, { recursive: true });
    }
  }

  /**
   * Resolve asset path - checks multiple storage locations
   */
  resolvePath(assetName, assetType = 'default') {
    // Check cache first
    const cacheKey = `${assetType}:${assetName}`;
    if (this.assetCache.has(cacheKey)) {
      const cached = this.assetCache.get(cacheKey);
      if (fs.existsSync(cached)) {
        return cached;
      } else {
        this.assetCache.delete(cacheKey);
      }
    }

    // Build possible paths
    const possiblePaths = [
      path.join(this.config.externalDrive.basePath, assetType, assetName),
      path.join(this.config.externalDrive.fallbackPath, assetType, assetName),
      path.join(__dirname, '../assets', assetType, assetName),
    ];

    // Add detected external drive paths
    for (const storagePath of this.storagePaths) {
      possiblePaths.push(path.join(storagePath, 'omniverse', assetType, assetName));
    }

    // Check each path
    for (const possiblePath of possiblePaths) {
      if (fs.existsSync(possiblePath)) {
        this.assetCache.set(cacheKey, possiblePath);
        debug(`Resolved asset ${assetName} to ${possiblePath}`);
        return possiblePath;
      }
    }

    // Return fallback path (doesn't need to exist yet)
    const fallback = path.join(this.config.externalDrive.fallbackPath, assetType, assetName);
    debug(`Asset ${assetName} not found, using fallback: ${fallback}`);
    return fallback;
  }

  /**
   * Get available storage information
   */
  getStorageInfo() {
    const info = {
      timestamp: new Date().toISOString(),
      paths: [],
      totalSize: 0,
      availableSize: 0
    };

    for (const storagePath of this.storagePaths) {
      try {
        if (fs.existsSync(storagePath)) {
          const stats = fs.statSync(storagePath);
          info.paths.push({
            path: storagePath,
            available: true,
            size: stats.size
          });
          info.totalSize += stats.size;
        } else {
          info.paths.push({
            path: storagePath,
            available: false
          });
        }
      } catch (error) {
        info.paths.push({
          path: storagePath,
          available: false,
          error: error.message
        });
      }
    }

    return info;
  }

  /**
   * Check if asset exists
   */
  assetExists(assetName, assetType = 'default') {
    try {
      const resolvedPath = this.resolvePath(assetName, assetType);
      return fs.existsSync(resolvedPath);
    } catch (error) {
      return false;
    }
  }

  /**
   * List assets of a type
   */
  listAssets(assetType = 'default') {
    const assets = new Set();

    for (const storagePath of this.storagePaths) {
      try {
        const assetDir = path.join(storagePath, assetType);
        if (fs.existsSync(assetDir)) {
          const files = fs.readdirSync(assetDir);
          files.forEach(file => assets.add(file));
        }
      } catch (error) {
        debug(`Error listing assets in ${storagePath}:`, error.message);
      }
    }

    return Array.from(assets);
  }

  /**
   * Save asset to best available storage
   */
  saveAsset(assetName, assetType, data) {
    const targetPath = this.resolvePath(assetName, assetType);
    const targetDir = path.dirname(targetPath);

    try {
      // Create directory if needed
      fs.mkdirSync(targetDir, { recursive: true });

      // Write file
      if (Buffer.isBuffer(data)) {
        fs.writeFileSync(targetPath, data);
      } else if (typeof data === 'string') {
        fs.writeFileSync(targetPath, data);
      } else {
        fs.writeFileSync(targetPath, JSON.stringify(data, null, 2));
      }

      debug(`Asset saved: ${targetPath}`);
      return targetPath;
    } catch (error) {
      debug(`Error saving asset:`, error);
      throw error;
    }
  }

  /**
   * Load asset as Buffer
   */
  loadAsset(assetName, assetType = 'default') {
    const assetPath = this.resolvePath(assetName, assetType);

    try {
      if (!fs.existsSync(assetPath)) {
        throw new Error(`Asset not found: ${assetName}`);
      }

      return fs.readFileSync(assetPath);
    } catch (error) {
      debug(`Error loading asset:`, error);
      throw error;
    }
  }

  /**
   * Clear asset cache
   */
  clearCache() {
    this.assetCache.clear();
    debug('Asset cache cleared');
  }
}

module.exports = PortableRuntime;
