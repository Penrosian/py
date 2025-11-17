import curses

def print(string, /, *args, end="\n"):
    with open("/tmp/debug_pipe", "w") as f:
        f.write(str(string))
        for s in args:
            f.write(" " + str(s))
        f.write(end)
        f.flush()

sylveon = [
    "$1        $2=",
    "$1      $2%::+$3::#",
    "$1     $2@::$4::: $3#+@",
    "$1    $1--$2--$4==:$3:::",
    "$1   $1@...$2-=+*            @::::",
    "$1  $1-..$2.$4.#$2---         #-:::::",
    "$1 $1@..$2.-$4=+$2---       ---$4--$2---",
    "$1 $1@ .$2#-$4++=$2=+ $1@.+  $2--@$3+-$2--**         $3-:@",
    "$1  $1@.$2:-$4=+=$2=-$1@..$2.@-*+$4+-$2---       $2=+=$4-::$3:@",
    "$1    $1-$2*=#=#$1-..$2.::*+%=$1#*       ...$2---",
    "$1    $2++--::$1:...$2-----$1...%   @ ....@",
    "$1     $1....$2+-----%-$1:...@  ......+-",
    "$1    $1.%- #.$2-$1#.#.$2.@#$1.::......=  $2---",
    "$1    $1..$3#$1@....@$3#$1-.              $2---",
    "$1    $1.$3###$1...$3###$1..   _   _     $2---@",
    "$1     $1.$3#$1+::..$3#$1.   .:::-$5::-# $2@----",
    "$1     $1..---...  .:-     $5--#$2==*==",
    "$1     $1@.$2.:. $1..............$2=+$5@",
    "$1    $1..@$2.$1.$2.$1................$2%-",
    "$1   $1@.. $5.%1...*...............$4=",
    "$1   $1@..@ $5:$1::  ...$5::::..%1.. ...",
    "$1    $1= $5*-+:#.$1...%   $5:::.$1.....-",
    "$1       $5@#=.$1..%      $5@--- $1-...",
    "$1         $5%$1..:-        $5--@ %1%..",
    "$1      $3--=$2.$1.-$5-@        $2==  .#",
    "$1     $3*--$2--+==@       =+  @-*",
    "$1       $2:-  +=       ==  ::-"
]

def main(stdscr):
    print("============")
    stdscr.clear()

    curses.start_color()
    curses.init_color(1, 1000, 1000, 1000) # White
    curses.init_color(2, 937, 604, 675) # Pink
    curses.init_color(3, 616, 875, 980) # Light Blue
    curses.init_color(4, 114, 600, 953) # Blue
    curses.init_color(5, 816, 816, 816) # Light Gray

    curses.init_pair(1, 1, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK)
    curses.init_pair(3, 3, curses.COLOR_BLACK)
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)

    curs_x = 0
    curs_y = 0
    try:
        for s in sylveon:
            segments = s.split("$")
            print(segments)
            for segment in segments:
                if segment == "":
                    continue
                color = curses.color_pair(int(segment[0]))
                segment = segment[1:]
                stdscr.attron(color)
                print("Drawing \"" + segment + "\"", "at", curs_x, curs_y)
                stdscr.addstr(curs_y, curs_x, segment)
                stdscr.attroff(color)
                curs_x += len(segment)
            curs_y += 1
            curs_x = 0
    except curses.error:
        print("Window too small!")
        stdscr.addstr(0, 0, "Window too small!")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)