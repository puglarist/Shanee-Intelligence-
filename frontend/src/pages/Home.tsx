export default function Home() {
  return (
    <div className="space-y-8">
      <section className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold text-white">
          Welcome to <span className="text-cyan-500">Shanee Intelligence</span>
        </h1>
        <p className="text-xl text-gray-400">
          Privacy-focused GPU-accelerated platform for distributed AI orchestration
        </p>
      </section>

      <section className="grid md:grid-cols-3 gap-6 mt-12">
        <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20 hover:border-cyan-500/50 transition">
          <h3 className="text-lg font-semibold text-cyan-400 mb-2">🔐 Privacy First</h3>
          <p className="text-gray-400">
            Built with privacy at the core. Your data stays secure with end-to-end encryption and local processing.
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20 hover:border-cyan-500/50 transition">
          <h3 className="text-lg font-semibold text-cyan-400 mb-2">⚡ GPU Accelerated</h3>
          <p className="text-gray-400">
            Leverage cutting-edge GPU acceleration for high-performance compute workloads and AI inference.
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-cyan-500/20 hover:border-cyan-500/50 transition">
          <h3 className="text-lg font-semibold text-cyan-400 mb-2">🔀 Distributed</h3>
          <p className="text-gray-400">
            Distributed architecture for scalable multi-agent orchestration across multiple nodes.
          </p>
        </div>
      </section>

      <section className="bg-gradient-to-r from-gray-800 to-gray-800 rounded-lg p-8 border border-cyan-500/20">
        <h2 className="text-2xl font-bold text-white mb-4">Getting Started</h2>
        <div className="space-y-3 text-gray-300">
          <p>✓ <span className="font-semibold">View System Status</span> - Check your dashboard for real-time metrics</p>
          <p>✓ <span className="font-semibold">Authentication</span> - Use your credentials to access secure areas</p>
          <p>✓ <span className="font-semibold">API Integration</span> - Connect via REST API at <code className="text-cyan-400 bg-gray-900 px-2 py-1 rounded">/api</code></p>
        </div>
      </section>
    </div>
  )
}
