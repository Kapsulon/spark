##
## EPITECH PROJECT, %YEAR%
## %PROJECTNAME%
## File description:
## %DESCRIPTION%
##

NAME = %EXECUTABLENAME%

SRC = $(shell find . -type f -name "*.c")

LIBFLAG = -I./include -L./lib/my -lmy

$(NAME):
	cd lib/my && make
	gcc -o $(NAME) $(SRC) $(LIBFLAG)

all: $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)
	cd lib/my && make fclean

re: fclean all
