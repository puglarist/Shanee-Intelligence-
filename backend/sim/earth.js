const debug = require('debug')('omniverse:sim:earth');

/**
 * Earth Simulation - Provides terrain, atmosphere, weather
 */
class EarthSimulation {
  constructor(config) {
    this.config = config;
    this.terrainGenerator = null;
    this.weatherSystem = null;
    this.timeOfDay = 0; // 0-24 hours
    this.dayNightCycle = true;
    this.atmosphericSettings = {
      visibility: 100, // km
      windSpeed: 0,
      windDirection: 0,
      temperature: 15, // Celsius
      humidity: 60 // percent
    };
    
    debug('Earth simulation initialized');
  }

  /**
   * Generate terrain using procedural generation
   */
  generateTerrain(width, height, resolution) {
    const terrain = {
      width,
      height,
      resolution,
      vertices: [],
      faces: [],
      generated: new Date().toISOString()
    };

    const verticesPerSide = Math.ceil(width / resolution) + 1;
    const heightMap = this.generateHeightMap(verticesPerSide, verticesPerSide);

    // Generate vertices
    for (let y = 0; y < verticesPerSide; y++) {
      for (let x = 0; x < verticesPerSide; x++) {
        const xPos = (x / verticesPerSide) * width;
        const yPos = heightMap[y][x];
        const zPos = (y / verticesPerSide) * height;

        terrain.vertices.push({
          x: xPos,
          y: yPos,
          z: zPos,
          normal: { x: 0, y: 1, z: 0 }, // Simplified
          uv: { u: x / verticesPerSide, v: y / verticesPerSide }
        });
      }
    }

    // Generate faces (simplified)
    for (let y = 0; y < verticesPerSide - 1; y++) {
      for (let x = 0; x < verticesPerSide - 1; x++) {
        const a = y * verticesPerSide + x;
        const b = a + 1;
        const c = a + verticesPerSide;
        const d = c + 1;

        terrain.faces.push([a, b, c]);
        terrain.faces.push([b, d, c]);
      }
    }

    debug(`Generated terrain: ${terrain.vertices.length} vertices, ${terrain.faces.length} faces`);
    return terrain;
  }

  /**
   * Generate height map using Perlin noise simulation
   */
  generateHeightMap(width, height) {
    const heightMap = [];
    const scale = 50; // Max height in meters

    for (let y = 0; y < height; y++) {
      heightMap[y] = [];
      for (let x = 0; x < width; x++) {
        // Simplified noise function
        const noise = Math.sin(x * 0.05) * Math.cos(y * 0.05);
        const ridges = Math.abs(noise) * 0.5;
        const mountains = Math.sin(x * 0.01) * Math.cos(y * 0.01) * 0.5;

        heightMap[y][x] = (noise + ridges + mountains) * scale;
      }
    }

    return heightMap;
  }

  /**
   * Update time of day (affects lighting/shadows)
   */
  updateTimeOfDay(deltaTime) {
    if (!this.dayNightCycle) return;

    this.timeOfDay += deltaTime / 3600; // Convert to hours

    // 24-hour cycle
    if (this.timeOfDay >= 24) {
      this.timeOfDay -= 24;
    }

    return this.getEnvironmentalLighting();
  }

  /**
   * Get environmental lighting based on time of day
   */
  getEnvironmentalLighting() {
    const sunAltitude = Math.sin((this.timeOfDay / 24 - 0.25) * Math.PI * 2) * 90;
    const sunAzimuth = (this.timeOfDay / 24) * 360;

    // Sky color based on time
    const isDay = sunAltitude > -6;
    const isDawn = sunAltitude > -12 && sunAltitude <= 0;
    const isDusk = sunAltitude > -6 && sunAltitude <= 6;

    let skyColor = { r: 0, g: 0, b: 0 }; // Night

    if (isDawn) {
      // Reddish dawn
      skyColor = { r: 1, g: 0.4, b: 0.2 };
    } else if (isDay) {
      // Blue daytime
      skyColor = { r: 0.5, g: 0.7, b: 1 };
    } else if (isDusk) {
      // Orange dusk
      skyColor = { r: 1, g: 0.5, b: 0.2 };
    }

    return {
      timeOfDay: this.timeOfDay,
      sunAltitude,
      sunAzimuth,
      skyColor,
      sunIntensity: Math.max(0, Math.sin((this.timeOfDay / 24) * Math.PI)),
      ambientLight: Math.max(0.1, Math.sin((this.timeOfDay / 24) * Math.PI)) * 0.5 + 0.5
    };
  }

  /**
   * Update weather system
   */
  updateWeather(deltaTime) {
    const windVariation = Math.sin(Date.now() / 10000) * 0.1;
    this.atmosphericSettings.windSpeed = Math.max(0, 5 + windVariation);
    this.atmosphericSettings.windDirection = (Date.now() / 100) % 360;

    const tempVariation = Math.sin(this.timeOfDay / 24 * Math.PI) * 10;
    this.atmosphericSettings.temperature = 15 + tempVariation;

    return this.atmosphericSettings;
  }

  /**
   * Get weather data
   */
  getWeatherData() {
    return {
      timestamp: new Date().toISOString(),
      ...this.atmosphericSettings,
      uvIndex: Math.max(0, Math.sin((this.timeOfDay / 24) * Math.PI)) * 11
    };
  }

  /**
   * Get terrain state
   */
  getTerrainState() {
    return {
      timeOfDay: this.timeOfDay,
      weather: this.getWeatherData(),
      lighting: this.getEnvironmentalLighting(),
      atmosphericDensity: 1.0 // Sea level
    };
  }
}

module.exports = EarthSimulation;
