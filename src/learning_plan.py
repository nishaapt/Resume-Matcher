def generate_learning_plan(missing_skills, resources_dict, total_days=30):
    """Spread missing skills across a day-by-day plan."""
    if not missing_skills:
        return []

    days_per_skill = max(total_days // len(missing_skills), 3)
    plan = []
    day_counter = 1

    for skill in missing_skills:
        info = resources_dict.get(skill, {"resources": [], "tip": "Practice this skill with a small project."})
        resources = info["resources"]
        tip = info["tip"]

        for i in range(days_per_skill):
            if day_counter > total_days:
                break

            if i == 0:
                task = f"Start learning {skill.title()} — read/watch: {resources[0] if resources else 'a beginner resource'}"
            elif i == days_per_skill - 1:
                task = f"Apply {skill.title()}: {tip}"
            else:
                remaining = resources[1:] if len(resources) > 1 else resources
                res = remaining[(i - 1) % len(remaining)] if remaining else "Practice and review notes"
                task = f"Continue {skill.title()}: {res}"

            plan.append({"day": day_counter, "skill": skill.title(), "task": task})
            day_counter += 1

    return plan