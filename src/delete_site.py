import os
import shutil
import json
from src.HTML_generators.update_main_html import update_main_html

def delete_site(site_name):
    if os.path.exists(f"static/sites/{site_name}"):
        shutil.rmtree(f"static/sites/{site_name}")

    with open("static/sites.json", "r", encoding="utf-8") as f:
        sites = json.load(f)
        if site_name in sites:
            del sites[site_name]
            
    with open("static/sites.json", "w", encoding="utf-8") as f:
        sites = json.dumps(sites, ensure_ascii=False, indent=4)
        f.write(sites)
    
    update_main_html(path="static")