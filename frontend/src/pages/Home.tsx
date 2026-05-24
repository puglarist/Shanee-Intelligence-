import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-16">
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
          Shanee Intelligence
        </h1>
        <p className="text-xl text-slate-300 mb-8">
          A privacy-focused, GPU-accelerated platform for secure computing and intelligence operations
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/dashboard"
            className="px-8 py-3 bg-cyan-500 hover:bg-cyan-600 rounded-lg font-semibold transition"
          >
            Go to Dashboard
          </Link>
          <Link
            to="/secure"
            className="px-8 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition"
          >
            Secure Area
          </Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mt-16">
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold text-cyan-400 mb-2">🔐 Security</h3>
          <p className="text-slate-300">End-to-end encrypted communications and secure compute isolation</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold text-cyan-400 mb-2">⚡ GPU Compute</h3>
          <p className="text-slate-300">Harness GPU power via Runpod and edge devices for AI/ML workloads</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h3 className="text-lg font-semibold text-cyan-400 mb-2">🌐 Decentralized</h3>
          <p className="text-slate-300">Multi-backend storage with GitHub, cloud, and distributed options</p>
        </div>
      </div>

      <div className="mt-16 bg-slate-800 p-8 rounded-lg border border-slate-700">
        <h2 className="text-2xl font-semibold mb-4">Project Status</h2>
        <p className="text-slate-300 mb-4">
          Shanee Intelligence is in early development (Phase 1: MVP). Core infrastructure is being established.
        </p>
        <ul className="list-disc list-inside text-slate-300 space-y-2">
          <li>React + TypeScript frontend (responsive, iOS-friendly)</li>
          <li>Python FastAPI backend with GPU integration</li>
          <li>Docker Compose for local development</li>
          <li>Authentication foundation (JWT)</li>
          <li>Multi-backend storage support</li>
        </ul>
      </div>
    </div>
  )
}
