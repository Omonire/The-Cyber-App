import re

def analyze_password_strength(password):
    """
    Analyzes the strength of a password and returns a score and feedback.
    """
    score = 0
    feedback = []

    # Length check
    if len(password) >= 12:
        score += 1
    elif len(password) >= 8:
        pass # Baseline
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Uppercase letter check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Lowercase letter check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Number check
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    # Special character check
    if re.search(r'[^A-Za-z0-9]', password):
        score += 1
    else:
        feedback.append("Add at least one special character (e.g., !@#$%).")

    # Determine strength level based on score
    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong",
        5: "Excellent"
    }

    strength = strength_levels.get(score, "Very Weak")

    return {
        "score": score,
        "strength": strength,
        "feedback": feedback
    }