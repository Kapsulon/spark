##
## EPITECH PROJECT, %YEAR%
## %PROJECTNAME%
## File description:
## %DESCRIPTION%
##

RED = \033[1;31m
GREEN = \033[1;32m
WHITE = \033[0;37m
BLUE = \033[1;34m
GOLD = \033[1;33m
BEGINL = \033[A
CLEARL = \033[2K
COL_END  = \033[0m
CLEAR_COL = \033[2K\033[A
%EXECUTABLENAME%
SRC =	%SRC%

OBJ = $(SRC:.c=.o)

CFLAGS = -W -Wall -Wextra -I./include -Wpedantic

LDFLAGS =%LDFLAGS%

MAKE = make --no-print-directory

FILE = $(shell echo $(SRC) | wc -w | sed -e 's/ //g')
CURRENT_FILES = $(shell find src/ -type f -name '*.o' | wc -l | sed -e 's/ //g')
CURRENT_FILE = $(shell echo '$$(( $(CURRENT_FILES) + 1 ))')

%.o: %.c
	@$(CC) $(CFLAGS) $^ -c -o $@
	@echo -en "$(CLEARL)$(BLUE)[$(GOLD)building$(BLUE)]$(WHITE) "
	@echo -en "$(BLUE)$(notdir $@) "
	@echo -e "$(GREEN)($(CURRENT_FILE)/$(FILE))$(WHITE)$(BEGINL)"
%NAME%
all: $(NAME)

clean:
	@rm -f $(OBJ)
	@echo -e "$(BLUE)[$(GOLD)Cleaner$(BLUE)] $(RED)clean success"

fclean: clean
	@rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
