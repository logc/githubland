all:
	pandoc -t beamer --template custom.beamer \
		-V graphics \
		--listings \
		-V theme=boxes \
		-V colortheme=beaver \
		-V fonttheme=professionalfonts \
		-H preamble.tex \
		-s slides.md -o slides.pdf

presentation:
	open slides.pdf

clean:
	rm slides.pdf
