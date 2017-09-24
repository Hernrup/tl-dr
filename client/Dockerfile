FROM teracy/angular-cli:1.0.0-rc.2

RUN mkdir -p /opt/app
ENV TERM=xterm
ENV APP=/opt/app
ENV NODE_ENV=development
ENV HTTPS_METHOD=noredirect

WORKDIR $APP
ADD ./client $APP

RUN yarn
CMD bash -c "yarn run start"

