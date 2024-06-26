def generate_html(city_name, selected_objects, site_name):
    html = f"""
    <!DOCTYPE html>
    <html>
        <head lang="ru">
            <meta charset="UTF-8">
            <link rel="stylesheet" href="/static/css/slider.css">
            <link rel="stylesheet" href="/static/css/style.css">
            <link rel="stylesheet" href="/static/css/back_button_style.css">
        </head>

        <body>
            <div class="main-container">
                <button id="backButton" onclick="goBack()" aria-label="Назад">&lt; Назад</button>
                <h1 class="page-title">{city_name}</h1>
                <div class="Description">
                    <div class="slider-container">
                        <div class="slider">
                            <div class="slide">
                                <img data-enlargeable width="100" style="cursor: zoom-in" src="/static/imgs/Города/{city_name}.jpg" alt="City">
                            </div>
                            <div class="slide">
                                <iframe src="/static/sites/{site_name}/interactive_map.html"></iframe>
                            </div>
                        </div>
                        <button class="prev-button" type="button" aria-label="Посмотреть предыдущий слайд">&lt;</button>
                        <button class="next-button" type="button" aria-label="Посмотреть следующий слайд">&gt;</button>
                    </div>
                    <div id="objectCard" class="object-card">
                        <button id="close-button" onclick="closeObjectCard()">Закрыть</button>
                        <div class="object-content"></div>
                    </div>
                </div>
            
            <div class="objects">
    """
    max_visit = -1
    for object in selected_objects:
        max_visit_curr = max([i for i in object.visits.values()])
        if max_visit_curr > max_visit:
            max_visit = max_visit_curr
    
    for object in selected_objects:
        html += f"""
        <div class="object" id={object.id}>

                    <div class="object-header">
                        <img name="category" alt="{object.category}" data-enlargeable width="100" style="cursor: zoom-in" src="/{object.image_path}" >
                        <h1 name="location">{object.name}</h1>
                        <p name="description">{object.description}</p> 
                    </div>

                    <div class="coordinates">
                        <p>Координаты:</p>
                        <span name="lattitude">{object.coords[0]}</span>
                        <span>, </span>
                        <span name="longitude">{object.coords[1]}</span>
                    </div>
                    
                    <span class="likes" name="likes">{object.likes} &#10084;</span>
                    
                    <div class="comments">
                        <p>Отзывы:</p>
                        <ul class="comments-list">
        """
        for review, rate, date in object.reviews:
            html += f"""

                            <li class="comment">
                                <div class="comment-container">
                                    <div class="comment-header">
                                        <div class="rate">
                                            <span class="rating" name="rating">{"&#9733;"*rate}</span>
                                        </div>
                                        <div class="metadata">
                                            <span class="date" name="date">{date}</span>
                                        </div>
                                    </div>
                                    <p class="review">{review}</p>
                                </div>
                            </li>
            """
        html += f"""
                        </ul>
                    </div>

                    <div class="visits">

                        <p>Посещаемость:</p>

                        <div>
                            <div class="day-of-week">Понедельник</div>
                            <div class="line">
                                <div style="width: {object.visits["monday"]/max_visit*100}%"> </div>
                            </div>
                        </div>

                        <div>
                            <div class="day-of-week">Вторник</div>
                            <div class="line">
                                <div style="width: {object.visits["tuesday"]/max_visit*100}%"> </div>
                            </div>
                        </div>

                        <div>
                            <div class="day-of-week">Среда</div>
                            <div class="line">
                                <div style="width: {object.visits["wednesday"]/max_visit*100}%"> </div>
                            </div>
                        </div>

                        <div>
                            <div class="day-of-week">Четверг</div>
                            <div class="line">
                                <div style="width: {object.visits["thursday"]/max_visit*100}%"> </div>
                            </div>
                        </div>

                        <div>
                            <div class="day-of-week">Пятница</div>
                            <div class="line">
                                <div style="width: {object.visits["friday"]/max_visit*100}%"> </div>
                            </div>
                        </div>

                        <div>
                            <div class="day-of-week">Суббота</div>
                            <div class="line">
                                <div style="width: {object.visits["saturday"]/max_visit*100}%"> </div>
                            </div>
                        </div>
                        
                        <div>
                            <div class="day-of-week">Воскресенье</div>
                            <div class="line">
                                <div style="width: {object.visits["sunday"]/max_visit*100}%"> </div>
                            </div>
                        </div>

                    </div>
                </div>
        """
    html += """
            </div>
            </div>
            
            <script src="/static/scripts/slider.js"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
            <script src="/static/scripts/modal-window.js"></script>
            <script src="/static/scripts/back_button.js"></script>
            <script src="/static/scripts/object_card.js"></script>

        </body>
    </html>
    """
    
    return html