import json
from src.patterns import Patterns

def update_main_html(path: str):
    """Обновление главной страницы

    Args:
        path (str): Путь до сайта

    Raises:
        Exception: _description_
    """
    html = Patterns.main_form_header
    
    with open("static/sites.json", 'r', encoding='utf-8') as f:
        try:
            sites = json.load(f)

        except Exception as ex:
            raise Exception(str(ex))
        
        for site, city in sites.items():
            html += Patterns.get_main_li_elem(site=site, city=city)
            
    html += Patterns.main_form_footer
    
    with open(f"{path}/main_page.html", 'w', encoding="utf-8") as f:
        f.write(html)
    