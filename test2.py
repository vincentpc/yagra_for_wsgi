
def application(environ, start_response):
    
    
    
    status = '200 ok'

    output = "wsgi.multithread = %s" % repr(environ['wsgi.multithread'])

    response_headers = [('Content-type', 'text/plain'),
                       ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
