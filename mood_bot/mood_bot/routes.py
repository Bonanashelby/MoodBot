def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home_view', '/')
    config.add_route('app_view', '/app')
    config.add_route('about_view', '/about')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('security', '/security')
    config.add_route('registration', '/register')
    config.add_route('twitter', '/twitter')
