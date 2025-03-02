from dataclasses import dataclass  # Import dataclass decorator for easy class creation
import datetime  # Import datetime for timestamping


@dataclass  # Define a class that will automatically create init, repr, and other methods
class InsulinProfile:
    breakfast: int  # Insulin dosage for breakfast
    lunch: int  # Insulin dosage for lunch
    dinner: int  # Insulin dosage for dinner
    base_rate: int  # The base insulin rate
    increase_per: int  # The increase in insulin rate per step
    scale_ranges: list  # A list of insulin dosage ranges
    last_updated: str = datetime.datetime.now().isoformat()  # Timestamp for the last update (defaults to current time)


# Function to create a new insulin profile with optional custom parameters
def create_new_profile(breakfast=0, lunch=0, dinner=0, base_rate=150, increase_per=50):
    # Ensure increase_per is positive, defaulting to 50 if not
    if increase_per <= 0:
        increase_per = 50

    # Create and return a new InsulinProfile object with the given or default values
    return InsulinProfile(
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        base_rate=base_rate,
        increase_per=increase_per,
        scale_ranges=generate_scale_ranges(base_rate, increase_per)
        # Generate scale ranges based on base_rate and increase_per
    )


# Function to generate insulin dosage ranges based on base rate and increase per step
def generate_scale_ranges(base_rate, increase_per):
    ranges = []  # List to store the dosage ranges
    current = base_rate  # Start at the base rate

    # If either increase_per or base_rate is invalid, return a default range
    if increase_per <= 0 or base_rate <= 0:
        return [{"low": 0, "high": 400, "dose": 1}]

    # Generate ranges until the maximum range (400) is reached or 20 ranges are created
    while current < 400 and len(ranges) < 20:
        ranges.append({
            "low": current,  # The lower bound of the range
            "high": current + increase_per,  # The upper bound of the range
            "dose": len(ranges) + 1  # The dose number based on the range's position
        })
        current += increase_per  # Increase the current range by the increase_per

    return ranges  # Return the generated list of ranges
