from src.patterns import Patterns


def generate_html(city_name: str, selected_objects: list, site_name: str) -> str:
    """Сгенерировать страницу локаций

    Args:
        city_name (str): Название города
        selected_objects (list): Набор локаций
        site_name (str): Имя сайта

    Returns:
        str: Сгенерированная страница
    """
    html = Patterns.get_site_header(city_name=city_name, site_name=site_name)
    
    max_visit = -1
    for object in selected_objects:
        max_visit_curr = max([i for i in object.visits.values()])
        if max_visit_curr > max_visit:
            max_visit = max_visit_curr
    
    for object in selected_objects:
        html += Patterns.get_site_location_header(object=object)
        
        for review, rate, date in object.reviews:
            html += Patterns.get_site_location_review(rate=rate, date=date, review=review)
            
        html += Patterns.get_site_location_visits(object=object, max_visit=max_visit)
        
    html += Patterns.site_location_footer
    
    return html