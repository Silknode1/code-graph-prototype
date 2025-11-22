import { useState } from 'react';

export default function ScoreCard({ onUnlock }) {
    const [isUnlocked, setIsUnlocked] = useState(false);

    const handleUnlock = () => {
        setIsUnlocked(true);
        if (onUnlock) onUnlock();
    };

    if (!isUnlocked) {
        return (
            <div className="glass-card text-center py-12">
                <h2 className="text-2xl text-neon-blue mb-4">🔒 Unlock Your Talent Profile</h2>
                <p className="opacity-70 mb-8">
                    Connect your GitHub to reveal your <b>True Skill Graph</b>.
                    <br />
                    No resumes. Just code.
                </p>
                <button
                    onClick={handleUnlock}
                    className="btn-primary text-lg animate-pulse"
                >
                    Analyze My GitHub
                </button>
            </div>
        );
    }

    return (
        <div className="glass-card">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl text-neon-blue">🚀 Your Code Graph</h2>
                <div className="bg-sunrise px-3 py-1 rounded-xl text-xs font-bold text-white">
                    TOP 1% LOGIC
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
                {/* Left: The Stats */}
                <div>
                    <SkillBar label="Algorithmic Logic" score={98} color="bg-sunrise" />
                    <SkillBar label="System Architecture" score={85} color="bg-electric" />
                    <SkillBar label="Code Consistency" score={92} color="bg-neon-blue" />
                    <SkillBar label="Community Impact" score={74} color="bg-emerald-500" />

                    <div className="mt-8 p-4 bg-white/5 rounded-lg">
                        <div className="text-xs opacity-60 mb-2">VERIFIED STACK</div>
                        <div className="flex gap-2">
                            <Badge>Rust</Badge>
                            <Badge>C++</Badge>
                            <Badge>Distributed Systems</Badge>
                        </div>
                    </div>
                </div>

                {/* Right: The "Radar" Visual (Simulated) */}
                <div className="flex items-center justify-center relative">
                    {/* Simple CSS Circle Visual */}
                    <div className="w-48 h-48 rounded-full border-2 border-dashed border-white/20 flex items-center justify-center bg-radial-gradient from-electric/20 to-transparent">
                        <div className="text-5xl font-bold">94</div>
                    </div>
                    <div className="absolute bottom-2 text-xs opacity-60">
                        GLOBAL RANK
                    </div>
                </div>
            </div>
        </div>
    );
}

function SkillBar({ label, score, color }) {
    return (
        <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
                <span>{label}</span>
                <span>{score}</span>
            </div>
            <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                <div
                    className={`h-full ${color} transition-all duration-1000 ease-out`}
                    style={{ width: `${score}%` }}
                ></div>
            </div>
        </div>
    );
}

function Badge({ children }) {
    return (
        <span className="px-2 py-1 bg-white/10 rounded text-xs">
            {children}
        </span>
    );
}
