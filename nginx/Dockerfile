FROM nginx:latest

RUN mkdir -p /www/static
ENV APP=/www

WORKDIR $APP

RUN rm -f /etc/nginx/conf.d/default.conf
ADD nginx/nginx.conf /etc/nginx/nginx.conf
ADD nginx/conf.d /etc/nginx/conf.d
ADD nginx/snippets /etc/nginx/snippets
ADD images /www/static/img
