import json


def update_main_html(path):
    html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <!-- basic -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!-- mobile metas -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="viewport" content="initial-scale=1, maximum-scale=1">
    <!-- site metas -->
    <title>СинтезСеть</title>
    <meta name="keywords" content="">
    <meta name="description" content="">
    <meta name="author" content="">
    <!-- bootstrap css -->
    <link rel="stylesheet" href="/static/css/main_page_styles/bootstrap.css">
    <!-- style css -->
    <link rel="stylesheet" href="/static/css/main_page_styles/style.css">
    <!-- Responsive-->
    <link rel="stylesheet" href="/static/css/main_page_styles/responsive.css">
    <!-- Scrollbar Custom CSS -->
    <link rel="stylesheet" href="/static/css/main_page_styles/jquery.mCustomScrollbar.css">
    <!-- Tweaks for older IEs-->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.css"
        media="screen">
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><![endif]-->
</head>
<!-- body -->

<body class="main-layout">
    <!-- loader  -->
    <div class="loader_bg">
        <div class="loader"><img src="/static/imgs/main_page_images/loading.gif" alt="#" /></div>
    </div>
    <!-- end loader -->
    <!-- header -->
    <header>
        <!-- header inner -->
        <div class="header">
            <div class="container">
                <div class="row">
                    <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col logo_section">
                        <div class="full">
                            <div class="center-desk">
                                <div class="logo">
                                    <a href="index.html"><img src="/static/imgs/main_page_images/logo.png" alt="#" /></a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-xl-9 col-lg-9 col-md-9 col-sm-9">
                        <nav class="navigation navbar navbar-expand-md navbar-dark ">
                            <button class="navbar-toggler" type="button" data-toggle="collapse"
                                data-target="#navbarsExample04" aria-controls="navbarsExample04" aria-expanded="false"
                                aria-label="Toggle navigation">
                                <span class="navbar-toggler-icon"></span>
                            </button>
                            <div class="collapse navbar-collapse" id="navbarsExample04">
                                <ul class="navbar-nav mr-auto">
                                    <li class="nav-item active">
                                        <a class="nav-link" href="#">Для пользователя</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/templates/home.html"> Личный кабинет</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="#service">Служба поддержки</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="#contact">Контакты</a>
                                    </li>
                                </ul>
                            </div>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
    </header>
    <!-- end header inner -->
    <!-- end header -->
    <!-- banner -->
    <section class="banner_main">
        <div class="container">
            <div class="row d_flex">
                <div class="col-md-5">
                    <div class="text-bg">
                        <h1>СинтезСеть</h1>
                        <span>Добро пожаловать на СинтезСеть!</span>
                        <p>
                            Рады видеть вас здесь!
                            СинтезСеть – ваш проводник в мир синтетических сайтов!
                            Наш сайт упрощает доступ к множеству синтетических ресурсов, предоставляя удобную навигацию
                            и актуальные ссылки.
                            Наслаждайтесь путешествием по цифровой вселенной вместе с СинтезСеть!
                            Если у вас возникнут вопросы или понадобится помощь, наша команда всегда готова помочь.
                            Приятного пользования!
                        </p>

                        <div class="tag-slider">
                            <div class="container">
                                <div class="row">
                                    <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 tag-slider-1">
                                        <div class="sl-links">
                                            <div class="sl-list">
                                                <ul class="sl-items">
    """
    with open("static/sites.json", 'r', encoding='utf-8') as f:
        try:
            sites = json.load(f)

        except Exception as ex:
            raise Exception(str(ex))
        
        for site, city in sites.items():
            html += f"""
                                                    <li class="item">
                                                        <a href="/static/sites/{site}/index.html">{city}</a>
                                                    </li>
            """
    html += """
                                                </ul>
                                            </div>
                                            <div class="sl-button">
                                                <div class="sl-prev"><a href="#"> &#8592 </a></div>
                                                <div class="sl-next"><a href="#"> &#8594 </a></div>
                                            </div>
                                        </div>
                                    </div> <!--col-->
                                </div> <!--row-->
                            </div> <!--container-->
                        </div> <!--tag-slider-->

                    </div>
                </div>

                <div class="col-md-7">
                    <div class="text-img">
                        <figure><img src="/static/imgs/main_page_images/img.png" /></figure>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- end banner -->
    <!-- Hosting -->
    <div id="" class="hosting">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="titlepage">
                        <h2>Что такое синтетические сайты?</h2>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="web_hosting">
                        <figure><img src="/static/imgs/main_page_images/web.jpg" alt="#" /></figure>
                        <p>
                            Синтетические сайты – это веб-ресурсы, созданные с использованием передовых технологий для
                            автоматической генерации контента, имитации данных и моделирования различных
                            онлайн-сервисов.
                            Эти сайты играют важную роль в разработке и тестировании программного обеспечения, а также
                            предоставляют уникальные возможности для исследования и обучения
                        </p>
                        <a href="#">Читать больше</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- end Hosting -->
    <!-- Services  -->
    <div id="service" class="Services">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="titlepage">
                        <h2>Сервисы для создания синтетических сайтов</h2>
                        <p>
                            Сервисы упрощают процесс создания синтетических сайтов и предоставляют мощные инструменты
                            для тестирования, <br>
                            разработки и прототипирования, снижая зависимость от реальных данных и ресурсов
                        </p>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="Services-box">
                        <i><img src="/static/imgs/main_page_images/service5.png" alt="#" /></i>
                        <h3>MockServer</h3>
                        <p>MockServer позволяет разработчикам создавать имитационные серверы, которые могут отвечать на
                            запросы HTTP/S с предопределенными ответами.</p>
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="Services-box">
                        <i><img src="/static/imgs/main_page_images/service1.png" alt="#" /></i>
                        <h3>Mockaroo</h3>
                        <p>Mockaroo позволяет пользователям создавать реалистичные данные для тестирования и разработки.
                            Сервис поддерживает различные форматы данных.</p>
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="Services-box">
                        <i><img src="/static/imgs/main_page_images/service6.png" alt="#" /></i>
                        <h3>Imposter</h3>
                        <p>Imposter позволяет разработчикам имитировать внешние сервисы и их API для тестирования
                            интеграций и уменьшения зависимости от внешних ресурсов.</p>
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="Services-box">
                        <i><img src="/static/imgs/main_page_images/service2.png" alt="#" /></i>
                        <h3>ChatGPT by OpenAI</h3>
                        <p>ChatGPT может использоваться для создания синтетического контента, автоматизации ответов на
                            запросы пользователей и разработки чатботов.</p>
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="Services-box">
                        <i><img src="/static/imgs/main_page_images/service3.png" alt="#" /></i>
                        <h3>Beeceptor</h3>
                        <p>Beeceptor позволяет пользователям создавать мок-эндпоинты для тестирования и отладки API,
                            смотреть журнал запросов.</p>
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="Services-box">
                        <i><img src="/static/imgs/main_page_images/service4.png" alt="#" /></i>
                        <h3>JSONPlaceholder</h3>
                        <p>JSONPlaceholder предоставляет поддельные данные и API для тестирования и прототипирования
                            веб-приложений.</p>
                    </div>
                </div>
                <a class="read_more" href="#">Читать больше</a>
            </div>
        </div>
    </div>
    <!-- end Servicess -->
    <!-- why -->
    <div id="why" class="why">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="titlepage">
                        <h2>Преимущества синтетических сайтов</h2>
                        <p>Эти преимущества делают синтетические сайты незаменимым инструментом для современных
                            разработчиков, тестировщиков и исследователей, обеспечивая безопасность, гибкость и
                            эффективность в работе с данными и сервисами. </p>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div id="box_ho" class="why-box">
                        <i><img src="/static/imgs/main_page_images/why1.png" alt="#" /></i>
                        <h3>Безопасность данных</h3>
                        <p>
                            Использование синтетических данных вместо реальных значительно снижает риск утечки
                            конфиденциальной информации.
                            В реальных данных часто содержатся чувствительные данные, такие как личные сведения,
                            финансовые записи или корпоративная информация.
                            При работе с такими данными в тестовых или разработческих средах существует риск их
                            случайного раскрытия или злоупотребления.
                            Синтетические сайты создают полностью искусственные данные, которые имитируют реальные, но
                            не содержат никакой конфиденциальной информации.
                            Это особенно важно в отраслях, требующих строгого соблюдения стандартов безопасности и
                            конфиденциальности, таких как здравоохранение, финансы и право.
                        </p>
                    </div>
                    <a class="read_more bg" href="#">Читать больше</a>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="why-box">
                        <i><img src="/static/imgs/main_page_images/why2.png" alt="#" /></i>
                        <h3>Масштабируемость и гибкость</h3>
                        <p>
                            Синтетические сайты могут легко масштабироваться и адаптироваться к различным требованиям
                            пользователей.
                            В отличие от реальных данных, которые могут быть ограничены по объему и сложности,
                            синтетические данные можно генерировать в любом необходимом количестве и с любыми
                            характеристиками.
                            Это позволяет разработчикам и тестировщикам создавать сценарии с высокой нагрузкой,
                            моделировать различные пользовательские случаи и проверять работу своих систем в
                            экстремальных условиях.
                            Кроме того, синтетические сайты можно быстро настраивать и изменять в зависимости от
                            изменяющихся потребностей проекта, что значительно ускоряет процесс разработки и
                            тестирования.
                        </p>
                    </div>
                    <a class="read_more bg" href="#">Читать больше</a>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12">
                    <div class="why-box">
                        <i><img src="/static/imgs/main_page_images/why3.png" alt="#" /></i>
                        <h3>Экономия времени и ресурсов</h3>
                        <p>
                            Создание и поддержка синтетических сайтов требует значительно меньше времени и ресурсов по
                            сравнению с использованием реальных данных и сервисов.
                            Сбор и подготовка реальных данных часто требуют значительных усилий, включая согласование с
                            владельцами данных, обеспечение соблюдения нормативных требований и проведение сложных
                            процедур очистки и анонимизации данных.
                            Синтетические данные, напротив, можно генерировать автоматически с помощью
                            специализированных инструментов, таких как Mockaroo, Faker или WireMock.
                            Это позволяет разработчикам сосредоточиться на решении основных задач проекта, а не на
                            обработке данных, что ускоряет цикл разработки и снижает затраты.
                        </p>
                    </div>
                    <a class="read_more bg" href="#">Читать больше</a>
                </div>
            </div>
        </div>
    </div>
    <!-- end why -->
    <!-- contact -->
    <div id="contact" class="contact">
        <div class="container">
            <div class="row">
                <div class="col-md-6 offset-md-3 ">
                    <form class="main_form">
                        <div class="row">
                            <div class="col-sm-12">
                                <input class="contactus" placeholder="Имя" type="text" name="Name">
                            </div>
                            <div class="col-sm-12">
                                <input class="contactus" placeholder="Электронная почта" type="text" name="Email">
                            </div>
                            <div class="col-sm-12">
                                <input class="contactus" placeholder="Номер телефона" type="text" name="Phone">
                            </div>
                            <div class="col-sm-12">
                                <input class="contactus" placeholder="Сообщение" type="text" name="Message">
                            </div>
                            <div class="col-sm-12">
                                <button class="send">Отправить</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- end contact -->
    <!--  footer -->
    <footer>
        <div class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-md-10 offset-md-1">
                        <div class="cont">
                            <h3>Спасибо, что посетили СинтезСеть!</h3>
                            <h2>Бесплатная многоцелевая адаптивная целевая страница 2024</h2>
                            <span>Свяжитесь с нами сейчас</span>
                            <p>
                                Мы надеемся, что наш портал помог вам открыть новые возможности синтетических сайтов и
                                ресурсов, необходимых для ваших проектов.
                                Независимо от того, являетесь ли вы разработчиком, тестировщиком, исследователем или
                                просто любознательным пользователем,
                                мы рады предложить вам лучшие инструменты и информацию для работы с синтетическими
                                данными и сервисами.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="copyright">
                <div class="container">
                    <div class="row">
                        <div class="col-md-12">
                            <p>© 2024 All Rights Reserved. <a href="https://html.design/">Free html Templates</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </footer>
<!-- end footer -->
    <!-- Javascript files-->
    <script src="/static/scripts/main_page/jquery.min.js"></script>
    <script src="/static/scripts/main_page/popper.min.js"></script>
    <script src="/static/scripts/main_page/bootstrap.bundle.min.js"></script>
    <script src="/static/scripts/main_page/jquery-3.0.0.min.js"></script>
    <script src="/static/scripts/main_page/plugin.js"></script>
    <script src="/static/scripts/main_page/script.js"></script>
    <!-- sidebar -->
    <script src="/static/scripts/main_page/jquery.mCustomScrollbar.concat.min.js"></script>
    <script src="/static/scripts/main_page/custom.js"></script>
    <script src="https:cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.min.js"></script>
    <!-- Linking of jQuery File -->
    <script src="/static/scripts/main_page/jQuery-v3.7.1.js"></script>
    <script src="/static/scripts/main_page/jQ_slider.js"></script>

</body>

</html>
    """
    with open(f"{path}/main_page.html", 'w', encoding="utf-8") as f:
        f.write(html)
    