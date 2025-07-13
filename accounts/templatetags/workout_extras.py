from django import template

register = template.Library()

@register.filter
def get_workout_sets(workout_data, workout_id):
    try:
        return workout_data.get(str(workout_id), 0)
    except (AttributeError, TypeError):
        return 0