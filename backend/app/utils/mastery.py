
def update_mastery_from_diagnostic_performance(prior_mastery, success=True, learning_rate=0.3, slip=0.1, guess=0.2):
    if success:
        mastery_probability = (prior_mastery * (1 - slip)) / (prior_mastery * (1 - slip) + (1 - prior_mastery) * guess)
    else:
        mastery_probability = (prior_mastery * slip) / (prior_mastery * slip + (1 - prior_mastery) * (1 - guess))
    
    new_mastery = mastery_probability + (1 - mastery_probability) * learning_rate
    return min(1.0, max(0.0, new_mastery))

def adjust_mastery_from_feedback(prior_mastery, feedback_category):
    if feedback_category == 0:
        return max(0.0, prior_mastery * 0.5)
    elif feedback_category == 0.5:
        return prior_mastery
    elif feedback_category == 1:
        return min(1.0, prior_mastery + 0.2) 
    
    return prior_mastery 