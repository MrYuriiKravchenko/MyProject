def breadcrumbs(request):
    path = request.path.split('/')
    breadcrumbs = [{'name': 'Home', 'url': '/'}]
    for index, segment in enumerate(path[1:], start=1):
        if segment:
            url = '/'.join(path[:index + 1]) + '/'
            breadcrumbs.append({'name': segment.title(), 'url': url})
    return {'breadcrumbs': breadcrumbs}
