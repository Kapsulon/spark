##
## KAPSULON PROJECT, 2022
## spark
## File description:
## Main project Makefile
##

NAME = spark

all: $(NAME)

$(NAME):
	pyinstaller --onefile --name=$(NAME) spark.py
	mv dist/$(NAME) .
	make clean

clean:
	rm -rf build
	rm -rf dist
	rm -rf __pycache__
	rm -rf spark.spec

fclean: clean
	rm -rf $(NAME)

re: fclean all
