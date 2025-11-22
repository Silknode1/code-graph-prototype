import { useState } from 'react'
import MarketTicker from './components/MarketTicker'
import ScoreCard from './components/ScoreCard'

function App() {
    const [isSignedIn, setIsSignedIn] = useState(false)

    return (
        <div className="min-h-screen flex flex-col items-center">
            <header className="mb-12">
                <div className="text-sm tracking-[2px] text-electric font-bold mb-2">
                    THE CODE GRAPH
                </div>
                <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-sunrise to-electric bg-clip-text text-transparent leading-tight">
                    Unbundle Your <span className="text-sunrise">Talent</span>.
                </h1>
                <p className="max-w-xl mx-auto opacity-70 text-lg">
                    The first merit-based talent marketplace.
                    Trade your skills for tokens. Apply to hype companies.
                </p>
            </header>

            <main className="w-full max-w-4xl">
                {/* 1. The Live Market */}
                <MarketTicker />

                {/* 2. The User's Profile (Locked initially) */}
                <ScoreCard onUnlock={() => setIsSignedIn(true)} />

                {/* 3. "More Companies" Teaser (Only visible if not signed in) */}
                {!isSignedIn && (
                    <div className="mt-12 opacity-50 blur-[2px]">
                        <div className="flex gap-4 justify-center">
                            <div className="glass-card w-40 h-24"></div>
                            <div className="glass-card w-40 h-24"></div>
                            <div className="glass-card w-40 h-24"></div>
                        </div>
                        <p className="mt-4 text-sm">Sign up to view 500+ more companies</p>
                    </div>
                )}
            </main>
        </div>
    )
}

export default App
