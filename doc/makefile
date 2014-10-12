all:
	pandoc -t beamer --template custom.beamer \
		-V graphics \
		-V theme=boxes \
		-V colortheme=dove \
		-V fonttheme=professionalfonts \
		-H preamble.tex \
		-s slides.md -o slides.pdf

presentation:
	open slides.pdf

clean:
	rm slides.pdf
