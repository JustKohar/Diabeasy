from dataclasses import dataclass
import datetime

@dataclass
class InsulinProfile:
    breakfast: int
    lunch: int
    dinner: int
    base_rate: int
    increase_per: int
    scale_ranges: list
    last_updated: str = datetime.datetime.now().isoformat()

def create_new_profile(breakfast=0, lunch=0, dinner=0, base_rate=150, increase_per=50):
    if increase_per <= 0:
        increase_per = 50
        
    return InsulinProfile(
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        base_rate=base_rate,
        increase_per=increase_per,
        scale_ranges=generate_scale_ranges(base_rate, increase_per)
    )

def generate_scale_ranges(base_rate, increase_per):
    ranges = []
    current = base_rate
    
    if increase_per <= 0 or base_rate <= 0:
        return [{"low": 0, "high": 400, "dose": 1}]
        
    while current < 400 and len(ranges) < 20:
        ranges.append({
            "low": current,
            "high": current + increase_per,
            "dose": len(ranges) + 1
        })
        current += increase_per
        
    return ranges