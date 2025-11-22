import { useState, useEffect } from 'react';

const INITIAL_COMPANIES = [
    { name: "NVIDIA", hype: 95, cost: 110, growth: 0.9 },
    { name: "OpenAI", hype: 98, cost: 115, growth: 0.95 },
    { name: "Oracle", hype: 40, cost: 36, growth: 0.2 },
    { name: "IBM", hype: 30, cost: 27, growth: 0.1 },
    { name: "HotNewStartup.ai", hype: 60, cost: 55, growth: 0.8 }
];

export default function MarketTicker() {
    const [companies, setCompanies] = useState(INITIAL_COMPANIES);

    useEffect(() => {
        const interval = setInterval(() => {
            setCompanies(prev => prev.map(company => {
                // Simulate market fluctuation
                const change = (Math.random() - 0.3) * 5 * company.growth; // Bias slightly up
                const newHype = Math.max(10, Math.min(100, company.hype + change));

                // Cost formula: Base(10) + (Hype^1.5 / 10)
                const newCost = Math.floor(10 + (Math.pow(newHype, 1.5) / 10));

                return { ...company, hype: newHype, cost: newCost };
            }));
        }, 1500); // Update every 1.5s

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="glass-card mb-8">
            <h2 className="text-2xl text-neon-blue mb-4 font-semibold">📈 Live Talent Market</h2>
            <div className="flex flex-wrap justify-around gap-4">
                {companies.map((company) => (
                    <div key={company.name} className="text-left min-w-[150px] transition-all duration-500">
                        <div className="text-sm opacity-80">{company.name}</div>
                        <div className="text-2xl font-bold flex items-center gap-2">
                            {company.cost}
                            <span className="text-xs opacity-60 font-normal">TOKENS</span>
                        </div>
                        <div className={`text-xs ${company.hype > 80 ? 'text-sunrise' : 'text-neon-blue'}`}>
                            Hype: {Math.round(company.hype)}%
                        </div>
                    </div>
                ))}
            </div>
            <div className="mt-4 text-xs opacity-50">
                * Prices update in real-time based on company growth & hype.
            </div>
        </div>
    );
}
