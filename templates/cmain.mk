##
## EPITECH PROJECT, %YEAR%
## %PROJECT_NAME%
## File description:
## %DESCRIPTION%
##

NAME = %EXECUTABLE_NAME%

SRC = $(shell find . -type f -name "*.c")

LIBFLAG = -I.././include -L.././lib/my -lmy

$(NAME):
	cd ../lib/my && make
	gcc -o $(NAME) $(SRC) $(LIBFLAG)

all: $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)
	cd ../lib/my && make fclean

re: fclean all
