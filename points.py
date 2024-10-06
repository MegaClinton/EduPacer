def assign_points(correct_answers):
    # Points per correct answer
    points_per_answer = 10
    
    # Calculate total points
    total_points = correct_answers * points_per_answer
    
    return total_points

# Function to assign tokens based on points
def assign_tokens(points):
    # Token value is 0.01 of the total points
    tokens = points * 0.01
    return tokens

# Example usage
correct_answers = 7
points = assign_points(correct_answers)
tokens = assign_tokens(points)

print(f"User has earned {points} points and {tokens:.2f} tokens.")