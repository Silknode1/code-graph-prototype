import random
import time

class Company:
    def __init__(self, name, base_hype, growth_rate):
        self.name = name
        self.base_hype = base_hype # 0-100
        self.growth_rate = growth_rate # 0.0 - 1.0
        self.current_hype = base_hype

    def update_market_conditions(self):
        """Simulate market fluctuations."""
        # Random fluctuation based on growth rate
        change = random.uniform(-5, 10) * self.growth_rate
        self.current_hype = max(10, min(100, self.current_hype + change))

    def get_token_cost(self):
        """
        Calculate the cost to apply in Tokens.
        Formula: Base Cost + (Hype^1.5 / 10)
        """
        base_cost = 10
        hype_premium = (self.current_hype ** 1.5) / 10
        return int(base_cost + hype_premium)

def simulate_market():
    companies = [
        Company("NVIDIA", base_hype=95, growth_rate=0.9),
        Company("OpenAI", base_hype=98, growth_rate=0.95),
        Company("Oracle", base_hype=40, growth_rate=0.2),
        Company("IBM", base_hype=30, growth_rate=0.1),
        Company("HotNewStartup.ai", base_hype=60, growth_rate=0.8)
    ]

    print("📈  OPENING MARKET: The Talent Exchange")
    print("=======================================")
    
    # Simulate 3 "Weeks" of market movement
    for week in range(1, 4):
        print(f"\n🗓  Week {week} Trading Update:")
        print(f"{'COMPANY':<20} | {'HYPE':<6} | {'COST (Tokens)':<15}")
        print("-" * 50)
        
        for company in companies:
            company.update_market_conditions()
            cost = company.get_token_cost()
            
            # Visual indicator of high cost
            indicator = "🔥" if cost > 100 else "  "
            if cost < 30: indicator = "❄️"
            
            print(f"{company.name:<20} | {int(company.current_hype):<6} | {cost:<5} {indicator}")
            
        time.sleep(0.5) # Pause for effect

if __name__ == "__main__":
    simulate_market()
