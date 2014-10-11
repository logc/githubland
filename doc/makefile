all: reveal.js
	pandoc -t revealjs -V theme=serif -s slides.md -o slides.html

reveal.js:
	mkdir reveal.js
	wget https://github.com/hakimel/reveal.js/archive/2.6.2.tar.gz -O revealjs.tar.gz && tar xfzv revealjs.tar.gz -C reveal.js/ --strip-components=1
