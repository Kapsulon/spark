##
## EPITECH PROJECT, %YEAR%
## %PROJECT_NAME%
## File description:
## %DESCRIPTION%
##

NAME = libmy.a

SRC = $(shell find . -type f -name "*.c")

OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	gcc -c $(SRC)
	ar rc $(NAME) $(OBJ)
	make clean

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)
	cd ../ && rm -f $(NAME)

re: fclean all
