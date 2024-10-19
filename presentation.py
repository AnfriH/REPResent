from helpers import *
from text import text_parse

WIDTH = 90
HEIGHT = 23

# this is the size of the panel. keep it in mind

# #----------------------------------------------------------------------------------------#
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# |                                                                                        |
# #----------------------------------------------------------------------------------------#

DASHED_ROUND = "┆┄╭╮╰╯"
DASHED_CORNER = "┆┄╭┬├╯"

LABEL_HEIGHT = 5
VERSION_GAG = "a0.0.1v2_final_final"


def border(charset: str):
    with box(charset):
        empty(0, 0, WIDTH - 2, HEIGHT - 2)


def labeled_border(title: str):
    border(DASHED_ROUND)
    with box(DASHED_CORNER):
        text(
            0,
            0,
            f"""

            {title}

            """,
            len(list(text_parse(title))) + 6,
            True
        )


def quick_fuzz(**kwargs):
    transition(fuzz, 0.2, **kwargs)


def quick_sweep(**kwargs):
    transition(sweep, 0.2, **kwargs)


def quick_shift(**kwargs):
    transition(shift, 0.2, **kwargs)


# image(WIDTH - 50 - 2, 3, 50, "images/walrus.png", True)


with presentation(WIDTH, HEIGHT):
    with slide():
        ...
    transition(shift, 0.2, axis="y")

    # start of presentation
    with slide("start"):
        image(-2, 5, 45, "images/hourglass", True)
        border(DASHED_ROUND)
        text(35, 2, """
        ░▒▓████████▓▒░ 
        ░▒▓█▓▒░        
        ░▒▓█▓▒░        
        ░▒▓███████▓▒░  
               ░▒▓█▓▒░ 
               ░▒▓█▓▒░ 
        ░▒▓███████▓▒░  
        """)
        text(52, 6, """
        ┓┏         ┓ ┏  ┓┓  ┳┳          
        ┗┫┏┓┏┓┏┓┏  ┃┃┃┏┓┃┃  ┃┃┏┓┏┏┓┏┓┏┓╋
        ┗┛┗╸┗┻┛ ┛  ┗┻┛┗╸┗┗  ┗┛╹╹┛┣┛┗╸╹╹┗    
        """)
        text(35, 11, "From Python 3.8 to the future of Python")
        text(44, HEIGHT - 2, f"Created using REPResent {VERSION_GAG}")

    quick_fuzz()

    with slide("about me"):
        image(49, 0, 40, "images/computer.png", True)
        labeled_border("About Me")

        text(2, LABEL_HEIGHT + 1, """
        Student at Victoria University of Wellington
            - 4th-year
            - Software Engineering
            - Currently fighting music robots with code 
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 6, """
        Previous intern at NZX
            - Helped with migration project
            - Wrote a core testing framework
            - Made multiple live-data tests
            - Didn't break everything   
        """)

    quick_fuzz()

    with cont():
        text(2, LABEL_HEIGHT + 12, """
        Interests:
            - Cycling
            - Drumming
            - Programming
            - Old(ish)-tech restoration (2000 - early 2010's)
        """)

    quick_sweep()

    with slide():
        text((90 - 20) // 2, HEIGHT // 2, "But enough about me! Let's talk Python!", 20, True)

    quick_sweep(flip=True)

    # with slide("py38 eol"):
    #     labeled_border("Python 3.8 EOL")
    #     text(2, LABEL_HEIGHT + 1, """
    #
    #     """)

    with slide("eol"):
        labeled_border("Python 3.8 EOL")
        text(2, LABEL_HEIGHT + 1, """
        Python 3.8 was released October 14th 2019
        """)

    with cont():
        text(6, LABEL_HEIGHT + 3, """
        However, security support has ended!
        """)

    with cont():
        text(10, LABEL_HEIGHT + 5, """
        <$red| bold>If you are still running Python 3.8, you should upgrade!<$>
        """)

    with cont():
        text(2, HEIGHT - 2, """
        <$italic><$blink>Un<$>fortunately, 3.8 != 2.7<$>
        """)

    quick_shift()

    with slide("performance"):
        labeled_border("Performance")
        image(WIDTH - 52, 2, 50, "images/fast.png", True)
        text(2, LABEL_HEIGHT + 1, """
        Massive performance improvements!
        
        <$red|>**10 - 60%**<$> improvement from 3.10 - 3.11
        
        Notable Improvements:
            - Python startup is 1.66x faster
            - Subscripts are 10 - 25% faster
            - Function calls are 20% faster
            - **...And many more!**
        """)
        text(36, HEIGHT - 2, "*for more info, see https://github.com/faster-cpython*")

    quick_shift()
    with slide("fstring"):
        labeled_border("F-string Improvements")
        text(2, LABEL_HEIGHT + 1, """
        Introduced in Python 3.6, but have received massive improvements since
        """)

    quick_fuzz()

    with slide(copy="fstring"):
        text(2, LABEL_HEIGHT + 3, """
        **Expression Values**
        Allow you to create F-strings with the expression represented
        
        Example:
        <$cyan|>a<$> = <$green|>3<$>
        <$cyan|>b<$> = <$green|>5<$>
        <$cyan|>print<$>(<$purple|>f"{<$cyan|>a<$>=}, {<$cyan|>b<$>=}, {<$cyan|>a<$>+<$cyan|>b<$>=}"<$>)
        
        >>> a=3, b=5, a+b=8
        
        """)

    quick_fuzz()

    with slide(copy="fstring"):
        text(2, LABEL_HEIGHT + 3, """
        **Improved Evaluation**
        F-strings can now:
        - Evaluate infinitely deep
        - Expressions can be written over multiple lines
        - Escape characters work correctly
        
        <$purple|>f"{f"{
        \"\"\"multiple lines
        oh so\\\\nmany\"\"\"
        }"} lines"<$>
        
        >>> multiple lines
            oh so
            many lines
        """)

    quick_shift()
    with slide("typehints"):
        labeled_border("Typehints<$purple|>[T]<$>")
        text(2, LABEL_HEIGHT + 1, """
            Whilst typehints have technically been in Python since 3.5,
            they have been refined, and are a core part of effective Python!
        """)

    quick_fuzz()
    with cont():
        with box(DASHED_ROUND):
            text(6, LABEL_HEIGHT + 4, """
            <$light_green|>Do I *reallllyyy* need typehints?<$>
            """)

    quick_fuzz()
    with cont():
        with box(DASHED_ROUND):
            text(WIDTH-6-6, LABEL_HEIGHT + 6, """
            <$red| blink>**Yes!**<$>
            """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 10, """
            I believe that everyone who writes Python should use typehints!
            
            If you don't use typehints, <$light_purple|>**you're limiting what your typechecker can do for you!**<$>  
        """)

    quick_shift()
    with slide("typehints 2"):
        labeled_border("Typehints<$purple|>[T]<$>")
        text(2, LABEL_HEIGHT + 1, """
        <$YELLOW|>def<$> <$cyan|>play_note<$>(<$cyan|>note<$>):
            <$YELLOW|>if<$> <$cyan|>len<$>(<$cyan|>note<$>) > <$green|>3<$>:
                <$cyan|>note<$> = <$cyan|>note<$>[:<$green|>3<$>]
            <$YELLOW|>return<$> <$cyan|>internal_play_note<$>(<$cyan|>note<$>)
        
        How do we call play_note()?
        """)

    quick_fuzz()
    with cont():
        text(2+28, LABEL_HEIGHT + 6, """
        "abc"?, [1,2,3]?, {4.0,2.2,6.7,9.1}?
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 8, """
                <$YELLOW|>def<$> <$cyan|>play_note<$>(<$cyan|>note<$>: <$purple|>**list[int]**<$>): -> <$purple|>**bool**<$>
                    <$YELLOW|>if<$> <$cyan|>len<$>(<$cyan|>note<$>) > <$green|>3<$>:
                        <$cyan|>note<$> = <$cyan|>note<$>[:<$green|>3<$>]
                    <$YELLOW|>return<$> <$cyan|>internal_play_note<$>(<$cyan|>note<$>)
                    
                <$cyan|>play_note<$>([<$green|>20<$>, <$green|>24<$>, <$green|>27<$>])
                
                
                <$red|black underline>**Always**<$> typehint your functions and methods.
                """)

    quick_shift()
    with slide("typehints 3"):
        labeled_border("Typehints<$purple|>[T]<$>")
        text(2, LABEL_HEIGHT + 1, """<$light_blue|>There are plenty of typehints to see!<$>""")

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 3, """
        **Collections:**
        <$purple|>list[T]<$>, <$purple|>set[T]<$>, <$purple|>dict[K, V]<$>, <$purple|>tuple[T, T2, T3, ...]<$>, etc
        
        <$cyan|>book_lengths<$>: <$purple|>dict[str, int]<$> = {}
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 8, """
            **Unions:**
            <$yellow|>def<$> <$cyan|>chars<$>(<$cyan|>characters<$>: <$purple|>str | list[str]<$>):
                ...
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 12, """
        **And many more!**
            - <$purple|>Self<$>                              - <$purple|>Literal["a", "b", ...]<$>
            - <$purple|>TypeGuard<$>                         - <$purple|>Final<$>
            - <$yellow|>type<$> <$cyan|>MyList<$> = <$purple|>list[str]<$>           - <$purple|>Any<$>
            - <$purple|>TypeIs<$>                            - <$purple|>None<$>
        """)

    quick_shift()
    with slide("typehints 4"):
        image(WIDTH - 28 - 2, 1, 32, "images/wazard.png", True)
        labeled_border("Typehints<$purple|>[\\*\\*P]<$>")
        text(2, LABEL_HEIGHT + 1, """
        Because Python is awesome, typehints can even do variadics!
        
        **TypeVarTuple:**
        <$yellow|>def<$> <$cyan|>args_only<$>[<$purple|>\\*Ts<$>](<$cyan|>\\*args<$>: <$purple|>\\*Ts<$>):
            ...
            
        **ParamSpec:**
        <$yellow|>def<$> <$cyan|>args_kwargs<$>[<$purple|>\\*\\*P<$>](<$cyan|>\\*args<$>: <$purple|>P.args<$>, <$cyan|>\\*\\*kwargs<$>: <$purple|>P.kwargs<$>):
            ...
        
        
        
        
        
        *It's unlikely that you'll use these,
        unless you're a code wizard...*
        """)

    quick_shift()

    with slide("protocols"):
        labeled_border("Protocols")
        text(2, LABEL_HEIGHT + 1, """
        Protocols represent class traits
        
        They're similar to <$brown|>Rust<$>'s "Traits" and <$cyan|>Go<$>'s "Interfaces"
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 5, """
        <$yellow|>class<$> <$purple|>Drawable<$>(<$purple|>Protocol<$>):
            <$yellow|>def<$> <$cyan|>draw<$>(<$cyan|>canvas<$>: <$purple|>Canvas<$>):
                ...
        
        <$dark_gray|># Box is drawable<$>
        <$yellow|>class<$> <$purple|>Box<$>:
            <$yellow|>def<$> <$cyan|>draw<$>(<$cyan|>canvas<$>: <$purple|>Canvas<$>):
                ...
        
        <$cyan|>can_draw<$>: <$purple|>Drawable<$> = <$purple|>Box<$>()
        """)

    quick_fuzz()
    with cont():
        text(2, HEIGHT-2, """
        Whilst you can explicitly inherit Protocols, *you don't have to!*
        """)

    quick_shift()
    with slide("protocols 2"):
        labeled_border("Protocols")
        text(2, LABEL_HEIGHT + 1, """
        Of course, Python already has Abstract Base Class (ABC)
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 3, """
        Protocols and ABC's are similar, but have different purposes:
            - ABC's block instantiation for abstract types
            - Protocols are implicit, whereas ABC is explicit
            - Protocols are really good as one-trick ponies i.e <$purple|>Iterable<$>
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 8, """
            Many core types have been grandfathered into the Protocol system:
            - <$purple|>Sequence[T]<$>
            - <$purple|>Iterator[T]<$>
            - <$purple|>Callable[[\\*\\*P], R]<$>
        """)

    quick_shift()
    with slide("walrus"):
        labeled_border("??????")
        text(2, LABEL_HEIGHT + 1, """
        Ok... let's talk about the
        big fella in the room...
        """)

    quick_fuzz()
    with cont():
        labeled_border("<$red|>**Walrus**<$>")
        text(2, LABEL_HEIGHT + 4, """
        Let's talk about the <$red|>walrus<$>
        """)
        image(WIDTH - 50 - 2, 3, 50, "images/walrus.png", True)

    quick_sweep(flip=True)
    with slide("walrus 2"):
        labeled_border("<$red|>**Walrus**<$>")

        text(2, LABEL_HEIGHT + 1, """
        The walrus was one of the most controversial features added to the language
        
        It allows for assignment as an expression:
        
        <$cyan|>a<$> = (<$cyan|>b<$> = <$green|>2<$>) <$dark_gray|># not allowed<$>
        <$cyan|>a<$> = (<$cyan|>b<$> := <$green|>2<$>) <$dark_gray|># allowed<$>
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 9, """
        *"Now that PEP 572 is done, I don't ever want to have to fight
         so hard for a PEP and find that so many people despise my decisions.
         
         ...
         
         I'll still be here, but I'm trying to let you all figure something
         out for yourselves. I'm tired, and need a very long break."
         - Guido van Rossum, on stepping down from BDFL*
        """)

    quick_shift()
    with slide("walrus 3"):
        labeled_border("<$red|>**Walrus**<$>")

        text(2, LABEL_HEIGHT + 1, """
        Personally, I don't see why the walrus was such a big deal
        Whilst it can be abused, that follows for nearly every feature in Python
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 4, """
        *Use common sense, follow the Zen of Python, don't cut your sandwich with a chainsaw!*
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 8, """
        Here are some uses for walrus I like:
        
        <$dark_gray|># single line expensive computation<$>
        <$cyan|>x<$> <$yellow|>if<$> (<$cyan|>x<$> := <$cyan|>expensive_list<$>(...) <$yellow|>else<$> [<$purple|>"default"<$>]])
        
        <$dark_gray|># inline if definition<$>
        <$yellow|>if<$> <$cyan|>search<$> <$yellow|>in<$> (<$cyan|>result<$> := <$cyan|>find<$>()):
            <$cyan|>print<$>(<$purple|>f"{<$cyan|>search<$>} found in {<$cyan|>result<$>}"<$>)
        """)

    quick_shift()
    with slide("match"):
        labeled_border("Match")
        text(2, LABEL_HEIGHT + 1, """
            Match statements are **awesome!**
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 3, """
            They act as the semantic *equivalent\\** to switch statements
            
            <$yellow|>match<$> <$cyan|>html_tag<$>:
                <$yellow|>case<$> <$purple|>"p"<$>:
                    ...
                <$yellow|>case<$> <$purple|>"h1"<$>:
                    ...
                <$yellow|>case<$> <$purple|>"h2"<$>:
                    ...
                <$yellow|>case<$> <$cyan|>other<$>:
                    ...
        """)

    quick_fuzz()
    with cont():
        text(2, HEIGHT-2, """
            <$dark_gray|>*\\*under the hood they use if-else, but you didn't hear that from me!*<$>
        """)

    quick_sweep(flip=True)
    with slide("match 2"):
        labeled_border("Match")
        text(2, LABEL_HEIGHT + 1, """
        Match statements can also be used for conditional matches:
        
        <$yellow|>match<$> <$cyan|>traffic_light<$>.<$cyan|>colour<$>:
            <$yellow|>case<$> <$purple|>"green"<$>:
                ...
            <$yellow|>case<$> <$purple|>"orange"<$> <$yellow|>if not<$> <$cyan|>traffic_light<$>.<$cyan|>blinking<$>:
                ...
            <$yellow|>case<$> <$purple|>"red"<$>:
                ...
            <$yellow|>case<$> <$cyan|>broken<$>:
                ...
        """)

    quick_sweep()
    with slide("match 3"):
        labeled_border("Match")
        text(2, LABEL_HEIGHT + 1, """
        Additionally, they can be used for structural matching:

        <$yellow|>match<$> <$cyan|>instruction<$>:
            <$yellow|>case<$> [<$cyan|>inst<$>]:
               ...
            <$yellow|>case<$> [<$purple|>"delete"<$>, <$cyan|>\\*arg<$>]:
               ...
            <$yellow|>case<$> [<$cyan|>other<$>, <$cyan|>\\*arg<$>]:
               ...
        
        <$yellow|>match<$> <$cyan|>direction<$>:
            <$yellow|>case<$> <$purple|>"north"<$> | <$purple|>"east"<$>:
                ...
            <$yellow|>case<$> <$cyan|>_<$>:
                ...
    """)

    quick_sweep(flip=True)
    with slide("match 4"):
        labeled_border("Match")
        text(2, LABEL_HEIGHT + 1, """
        Additionally, they can be used for structural matching:
            
        <$brown|>@dataclass<$>
        <$yellow|>class<$> <$purple|>Box<$>:
            <$cyan|>width<$>: <$purple|>int<$>
            <$cyan|>height<$>: <$purple|>int<$>
        
        ...
        
        <$yellow|>match<$> <$cyan|>object<$>:
            <$dark_gray|># match square boxes<$>
            <$yellow|>case<$> <$purple|>Box<$>(<$cyan|>width<$>, <$cyan|>height<$>) <$yellow|>if<$> <$cyan|>width<$> == <$cyan|>height<$>:
                ...
            <$yellow|>case<$> <$cyan|>_<$>:
                ...
        """)

    quick_sweep()
    with slide("match 5"):
        labeled_border("Match")
        text(2, LABEL_HEIGHT + 1, """
        Caution! All non-dotted expressions as a case pattern will be read as wildcard!
        
        <$yellow|>match<$> <$cyan|>type<$>(<$cyan|>some_value<$>):
            <$dark_gray|># every value will blow up, because "int" is not a type, it's a wildcard name<$>
            <$yellow|>case<$> <$cyan|>int<$>:
                <$cyan|>blow_up<$>()
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 8, """
        If you need that behaviour, do this instead:
        
        <$yellow|>match<$> <$cyan|>some_value<$>:
            <$yellow|>case<$> <$purple|>int<$>():
                <$cyan|>blow_up<$>()
                
                
                
        *for more info, check out https://peps.python.org/pep-0636/*
        """)

    quick_shift()
    with slide("error"):
        labeled_border("Error Messages")
        text(2, LABEL_HEIGHT + 1, """
        Older versions of Python are pretty bad at error messages.
        
        Often, errors were reported on incorrect liines,
        or were just vague and hard to understand.
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../presentation.py", line 4, in <strcomp>
                or were just vague and hard to understand.
                ^
            TypoError: misspelled word<$>
        """)

    quick_shift()
    with slide("error 2"):
        labeled_border("Error Messages")
        text(2, LABEL_HEIGHT + 1, """
        <$cyan|>fav_languages<$> = [<$purple|>"Python"<$>, <$purple|>"Rust"<$>, <$purple|>"OCaml"<$>, <$purple|>"Kotlin"<$>]
        <$cyan|>fav_animals<$> = [<$purple|>"PYTHON"<$>, <$purple|>"raccoon"<$>, <$purple|>"opossum"<$>]
        
        <$cyan|>mutuals<$> = [<$cyan|>e<$> <$yellow|>for<$> <$cyan|>e<$> <$yellow|>in<$> <$cyan|>fav_languages<$> <$yellow|>if<$> <$cyan|>f<$>.<$cyan|>lower<$>() <$yellow|>in<$> (<$cyan|>f<$>.<$cyan|>lower<$>() <$yellow|>for<$> <$cyan|>f<$> <$yellow|>in<$> <$cyan|>fav_animals<$>)]
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../main.py", line 4, in <listcomp>
                mutuals = [e for e in fav_languages if f.lower() in (f.lower() for f ...
            NameError: name 'f' is not defined<$>
        
        *what do you mean! f is defined! it's right there!*
        """)

    quick_sweep()
    with slide(copy="error 2"):
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../main.py", line 4, in <listcomp>
                mutuals = [e for e in fav_languages if f.lower() in (f.lower() for f ...
                                                        ^
            NameError: name 'f' is not defined<$>
        """)

    quick_shift()
    with slide("error 3"):
        labeled_border("Error Messages")
        text(2, LABEL_HEIGHT + 1, """
        <$yellow|>def<$> <$cyan|>x_transforms<$>(<$cyan|>x<$>: <$purple|>int<$>) -> <$purple|>Tuple[int, int, int]<$>:
            <$yellow|>return<$> (<$cyan|>x<$>, <$green|>1<$> / (<$cyan|>x<$> \\* <$cyan|>x<$>, <$green|>6<$> - <$cyan|>x<$>)

        <$cyan|>print<$>(<$cyan|>x_transforms<$>(<$green|>3<$>))
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../main.py", line 4
                print(x_transforms(3))
                ^
            SyntaxError: invalid syntax<$>

        *buh? but print is a builtin? how is that line not valid!*
        """)

    quick_sweep()
    with slide(copy="error 3"):
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../main.py", line 3
                return (x, 1 / (x \\* x, 6 - x)
                       ^
            SyntaxError: '(' was never closed<$>
        """)

    quick_shift()
    with slide("error 4"):
        labeled_border("Error Messages")
        text(2, LABEL_HEIGHT + 1, """
        <$yellow|>try<$>:
            <$yellow|>raise<$> <$purple|>ValueError<$>(<$purple|>"Explode"<$>)

        <$cyan|>print<$>(<$purple|>"Oh the joys of coding"<$>)
        """)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../main.py", line 4
                print("Oh the joys of coding")
                ^
            SyntaxError: invalid syntax<$>

        <$light_gray|>*ok I think we get the idea...*<$>
        """)

    quick_sweep()
    with slide(copy="error 4"):
        text(2, LABEL_HEIGHT + 7, """
        >>>   <$red|>File "/home/anfri/.../main.py", line 4
                print("Oh the joys of coding")
                ^^^^^
            SyntaxError: expected 'except' or 'finally' block<$>
        """)

    quick_shift()
    with slide("other"):
        labeled_border("Other Stuff")
        text(2, LABEL_HEIGHT + 1, """
        Over 5 years of updates, Python has received an
        overwhelming number of changes, bugfixes and tweaks.
        
        Given the sheer magnitude, I'll only be covering the highlights!
        """)
        image(WIDTH-1-24, 5, 24, "images/gear.png", True)

    quick_fuzz()
    with cont():
        text(2, LABEL_HEIGHT + 6, """
        **Position-Only Params:**
        
        <$yellow|>def<$> <$cyan|>foobar<$>(<$cyan|>a<$>, /, <$cyan|>b<$>, \\*, <$cyan|>c<$>):
            ...
        
        <$cyan|>foobar<$>(<$cyan|>a<$>=<$green|>2<$>, <$green|>2<$>, <$cyan|>c<$>=<$green|>5<$>)
        """)

    quick_fuzz()
    with slide(copy="other"):
        text(2, LABEL_HEIGHT + 6, """
        **| and |= dicts:**
        
        <$cyan|>features<$> = {<$purple|>"length"<$>: <$green|>2<$>, <$purple|>"width"<$>: <$green|>5<$>}
        <$cyan|>features<$> |= {<$purple|>"weight"<$>: <$green|>30<$>}
        <$cyan|>moar_features<$> = <$cyan|>features<$> | {<$purple|>"shmoves"<$>: <$green|>3<$>}
        """)

    quick_fuzz()
    with slide(copy="other"):
        text(2, LABEL_HEIGHT + 6, """
        **Multiple Contexts:**
        
        <$yellow|>with<$> (
            <$cyan|>open<$>(<$purple|>"file1.txt"<$>) <$yellow|>as<$> <$cyan|>first<$>,
            <$cyan|>open<$>(<$purple|>"file2.txt"<$>) <$yellow|>as<$> <$cyan|>second<$>
        ):
            ...
        """)

    quick_shift()
    with slide("future"):
        labeled_border("So... What's Next?")
        text(2, LABEL_HEIGHT + 1, """
            **No-GIL Mode:**
            - Called using separate <$cyan|>python3.13t<$> executable
            - https://peps.python.org/pep-0703/

            **JIT Compilation:**
            - Already performing similar to existing Cython implementation
            - Potential for massive speedup in execution times
            - https://peps.python.org/pep-0744/
        """)

    quick_fuzz()
    with slide("end"):
        with box(DASHED_ROUND):
            text(1, 1, "Thanks for watching!")
        text(2, 16, """
                    **<$cyan|>Anfri Hayward<$>**
        <$blue|>discord<$>: anfri
        <$green|>email<$>: anfrih@gmail.com
        <$brown|>github<$>: https://github.com/AnfriH
        <$purple|>linkedin<$>: https://www.linkedin.com/
                  in/anfri-hayward-a79a97289/
        """)
        image(WIDTH - 48, 0, 46, "images/emoji09.png", True)
