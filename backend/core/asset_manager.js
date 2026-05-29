const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const debug = require('debug')('omniverse:assets');
const PortableRuntime = require('./portable_runtime');

/**
 * AssetManager - Manages asset discovery, streaming, and caching
 */
class AssetManager {
  constructor(config) {
    this.config = config;
    this.portable = new PortableRuntime(config);
    this.assetMetadata = new Map();
    this.streamSessions = new Map();
    
    this.initialize();
  }

  initialize() {
    debug('Initializing AssetManager');
    
    // Create cache directory
    if (!fs.existsSync(this.config.assets.cacheDir)) {
      fs.mkdirSync(this.config.assets.cacheDir, { recursive: true });
    }
  }

  /**
   * Calculate file hash for integrity checking
   */
  calculateHash(filePath) {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);

    return new Promise((resolve, reject) => {
      stream.on('data', data => hash.update(data));
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', reject);
    });
  }

  /**
   * Register an asset in the database
   */
  async registerAsset(name, type, filePath) {
    try {
      const stats = fs.statSync(filePath);
      const hash = await this.calculateHash(filePath);

      const metadata = {
        name,
        type,
        path: filePath,
        size: stats.size,
        hash,
        registered: new Date().toISOString(),
        cached: false
      };

      this.assetMetadata.set(name, metadata);
      debug(`Asset registered: ${name} (${stats.size} bytes)`);

      return metadata;
    } catch (error) {
      debug(`Error registering asset:`, error);
      throw error;
    }
  }

  /**
   * Stream asset in chunks
   */
  streamAsset(assetName, res) {
    try {
      const metadata = this.assetMetadata.get(assetName);
      if (!metadata) {
        throw new Error(`Asset not found: ${assetName}`);
      }

      const filePath = metadata.path;
      const fileSize = metadata.size;
      const chunkSize = this.config.assets.chunkSize;

      // Set response headers
      res.setHeader('Content-Type', 'application/octet-stream');
      res.setHeader('Content-Length', fileSize);
      res.setHeader('X-Asset-Hash', metadata.hash);
      res.setHeader('X-Asset-Size', fileSize);

      // Stream file in chunks
      let position = 0;
      const readStream = fs.createReadStream(filePath, {
        highWaterMark: chunkSize
      });

      readStream.on('data', chunk => {
        res.write(chunk);
        position += chunk.length;
        
        // Emit progress
        const progress = Math.round((position / fileSize) * 100);
        debug(`Streaming ${assetName}: ${progress}%`);
      });

      readStream.on('end', () => {
        res.end();
        debug(`Streaming complete: ${assetName}`);
      });

      readStream.on('error', error => {
        debug(`Stream error:`, error);
        res.status(500).json({ error: error.message });
      });
    } catch (error) {
      debug(`Error streaming asset:`, error);
      res.status(404).json({ error: error.message });
    }
  }

  /**
   * Get asset metadata
   */
  getAssetMetadata(assetName) {
    const metadata = this.assetMetadata.get(assetName);
    if (!metadata) {
      return null;
    }

    return {
      ...metadata,
      exists: fs.existsSync(metadata.path)
    };
  }

  /**
   * List all registered assets
   */
  listAssets(type = null) {
    const assets = [];

    for (const [name, metadata] of this.assetMetadata) {
      if (type === null || metadata.type === type) {
        assets.push({
          name,
          type: metadata.type,
          size: metadata.size,
          hash: metadata.hash,
          registered: metadata.registered
        });
      }
    }

    return assets;
  }

  /**
   * Cache asset locally
   */
  cacheAsset(assetName) {
    try {
      const metadata = this.assetMetadata.get(assetName);
      if (!metadata) {
        throw new Error(`Asset not found: ${assetName}`);
      }

      if (!fs.existsSync(metadata.path)) {
        throw new Error(`Asset file not found: ${metadata.path}`);
      }

      const cachePath = path.join(this.config.assets.cacheDir, assetName);
      const cacheDir = path.dirname(cachePath);

      // Create cache directory
      if (!fs.existsSync(cacheDir)) {
        fs.mkdirSync(cacheDir, { recursive: true });
      }

      // Copy file to cache
      fs.copyFileSync(metadata.path, cachePath);

      // Update metadata
      metadata.cached = true;
      metadata.cachedAt = new Date().toISOString();

      debug(`Asset cached: ${assetName}`);
      return cachePath;
    } catch (error) {
      debug(`Error caching asset:`, error);
      throw error;
    }
  }

  /**
   * Get asset from cache or disk
   */
  getAsset(assetName) {
    try {
      const metadata = this.assetMetadata.get(assetName);
      if (!metadata) {
        throw new Error(`Asset not found: ${assetName}`);
      }

      // Return from cache if available
      if (metadata.cached) {
        const cachePath = path.join(this.config.assets.cacheDir, assetName);
        if (fs.existsSync(cachePath)) {
          return fs.readFileSync(cachePath);
        }
      }

      // Return from original path
      if (fs.existsSync(metadata.path)) {
        return fs.readFileSync(metadata.path);
      }

      throw new Error(`Asset file not found: ${assetName}`);
    } catch (error) {
      debug(`Error getting asset:`, error);
      throw error;
    }
  }

  /**
   * Clear cache
   */
  clearCache(assetName = null) {
    try {
      if (assetName) {
        const cachePath = path.join(this.config.assets.cacheDir, assetName);
        if (fs.existsSync(cachePath)) {
          fs.unlinkSync(cachePath);
          const metadata = this.assetMetadata.get(assetName);
          if (metadata) {
            metadata.cached = false;
          }
        }
      } else {
        // Clear entire cache
        const cacheFiles = fs.readdirSync(this.config.assets.cacheDir);
        cacheFiles.forEach(file => {
          const filePath = path.join(this.config.assets.cacheDir, file);
          fs.unlinkSync(filePath);
        });

        // Reset all metadata cache flags
        for (const metadata of this.assetMetadata.values()) {
          metadata.cached = false;
        }
      }

      debug(`Cache cleared${assetName ? ': ' + assetName : ''}`);
    } catch (error) {
      debug(`Error clearing cache:`, error);
      throw error;
    }
  }

  /**
   * Discover assets from external drives
   */
  discoverAssets(assetType) {
    const discovered = [];

    try {
      const assets = this.portable.listAssets(assetType);
      assets.forEach(assetName => {
        const assetPath = this.portable.resolvePath(assetName, assetType);
        if (fs.existsSync(assetPath)) {
          discovered.push({
            name: assetName,
            type: assetType,
            path: assetPath,
            discovered: true
          });
        }
      });

      debug(`Discovered ${discovered.length} assets of type ${assetType}`);
    } catch (error) {
      debug(`Error discovering assets:`, error);
    }

    return discovered;
  }
}

module.exports = AssetManager;
