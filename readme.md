# Примеры сгенерированных сайтов
https://jartix.github.io/Synthetic-sites/docs/sites_preview/site6/index.html

https://jartix.github.io/Synthetic-sites/docs/sites_preview/site7/index.html

https://jartix.github.io/Synthetic-sites/docs/sites_preview/site8/index.html


# Примечание
Для того, чтобы приложение корректно работало, необходимо создать файл keys.py в корне проекта и добавить туда 3 ключа: секретный ключ и API ключ для Кандинского и API ключ для Gemini.

![Ключи](/docs/keys_view.png)

Из-за блокировки Gemini на территории России, чтобы он работал необходим DNS или VPN.

Большую информацию по проекту можно посмотреть в директории docs

# Структура проекта
```txt
.
├── docs
├── instance
├── models
├── src
│   ├── AI
│   ├── auth_scripts
│   ├── HTML_generators
├── static
│   ├── css
│   │   ├── auth_form_styles
│   │   └── main_page_styles
│   ├── descriptions
│   ├── fonts
│   ├── imgs
│   │   └── main_page_images
│   ├── reviews
│   ├── scripts
│   │   ├── main_page
│   │   │   ├── revolution
│   │   │   │   ├── assets
│   │   │   │   ├── css
│   │   │   │   ├── fonts
│   │   │   │   └── js
│   └── sites
├── templates
```
# Развернутая структура проекта
```txt
.
├── docs/
│   ├── API_documentation.md
│   ├── BD_structure.md
│   ├── scheme.png
│   └── server_functions.md
├── instance/
│   └── site.db
├── models/
│   ├── location_model.py
│   └── user_model.py
├── src/
│   ├── AI/
│   │   ├── image_generator.py
│   │   └── text_generator.py
│   │   └── gemini.text_gen.py
│   ├── auth_scripts/
│   │   ├── create_user.py
│   │   ├── forms.py
│   │   ├── init_db.py
│   │   └── make_admin.py
│   ├── HTML_generators/
│   │   ├── generate_html.py
│   │   ├── generate_interactive_map.py
│   │   └── update_main_html.py
│   ├── rate_limiter.py
│   ├── delete_site.py
│   └── generate_site.py
├── static/
│   ├── css/
│   │   ├── auth_form_styles
│   │   └── main_page_styles
│   ├── descriptions
│   ├── fonts
│   ├── imgs/
│   │   └── main_page_images
│   ├── reviews
│   ├── scripts/
│   │   ├── main_page/
│   │   │   ├── revolution/
│   │   │   │   ├── assets
│   │   │   │   ├── css
│   │   │   │   ├── fonts
│   │   │   │   └── js
│   │   │   ├── bootstrap.bundle.js
│   │   │   ├── bootstrap.bundle.js.map
│   │   │   ├── bootstrap.bundle.min.js
│   │   │   ├── bootstrap.bundle.min.js.map
│   │   │   ├── bootstrap.js
│   │   │   ├── bootstrap.js.map
│   │   │   ├── bootstrap.min.js
│   │   │   ├── bootstrap.min.js.map
│   │   │   ├── custom.js
│   │   │   ├── jQ_slider.js
│   │   │   ├── jquery-3.0.0.min.js
│   │   │   ├── jQuery-v3.7.1.js
│   │   │   ├── jquery.mCustomScrollbar.concat.min.js
│   │   │   ├── jquery.min.js
│   │   │   ├── jquery.validate.js
│   │   │   ├── modernizer.js
│   │   │   ├── plugin.js
│   │   │   ├── popper.min.js
│   │   │   ├── script.js
│   │   │   └── slider-setting.js
│   │   ├── admin_panel.js    
│   │   ├── back_button.js
│   │   ├── interactive_map_scripts.js
│   │   ├── modal-window.js
│   │   ├── object_card.js
│   │   └── slider.js
│   └── sites/
│       ├── main_page.html
│       └── sites.json
├── templates/
│   ├── admin_panel.html
│   ├── dashboard.html
│   ├── home.html
│   ├── login.html
│   └── register.html
├── keys.py
├── app.py
├── config.py
├── readme.md
├── server.py
└── site_generator.py
```
