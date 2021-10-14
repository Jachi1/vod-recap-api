import matplotlib.pyplot as plt
from functions import *
from matplotlib.pyplot import figure

# Returns filename
def plotter(chat: list) -> str:

    # Only plotting for emotes_by_usage
    emote_dict = emotes_by_usage(chat)

    fig, ax = plt.subplots()
    ax.bar(emote_dict.keys(), emote_dict.values())
    plt.xticks(range(len(emote_dict)), list(emote_dict.keys()), rotation = 90)
    plt.xlabel("Emote")
    plt.ylabel("Emote Usage")

    fig = plt.gcf()
    fig.set_size_inches(20, 20)
    fig.savefig('outputImg.png', dpi=100)
    
    return 'outputImg.png'
