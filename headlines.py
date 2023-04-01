try:
    from IPython.display import display, Markdown, Audio
    beep = lambda: display(Audio("beep.wav", autoplay=True))
    def h1(text):
        display(Markdown(f'# {text}'))
    def h2(text):
        display(Markdown(f'## {text}'))
    def h3(text):
        display(Markdown(f'### {text}'))
    def h4(text):
        display(Markdown(f'#### {text}'))
    def h5(text):
        display(Markdown(f'##### {text}'))
    def h6(text):
        display(Markdown(f'###### {text}'))
    def pf(f, d):
        display(Markdown(f'**{f}**: {d}'))
except:
    beep = lambda x: print("Beep!") 
    def h1(text):
        print(f'# {text}')
    def h2(text):
        print(f'## {text}')
    def h3(text):
        print(f'### {text}')
    def h4(text):
        print(f'#### {text}')
    def h5(text):
        print(f'##### {text}')
    def h6(text):
        print(f'###### {text}')
    def pf(f, d):
        print(f'**{f}**: {d}')
