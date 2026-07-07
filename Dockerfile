FROM jekyll/builder

WORKDIR /tmp
ADD Gemfile /tmp/
ADD Gemfile.lock /tmp/
RUN bundle install

FROM jekyll/jekyll
RUN useradd -m jekyll
USER jekyll

VOLUME /src
EXPOSE 4000

WORKDIR /src
ENTRYPOINT ["jekyll", "serve", "--livereload", "-H", "0.0.0.0"]
