

from dataparser import *

import matplotlib.pyplot as plt
import itertools

# Collect information about the genre
def collect_genre_info(data, truncate_at=-1):
    """
    Builds a dataset given a dictionary of tracks
    @param data: a dictionary of tracks from the Apple Music library
    @return a dictionary of genres and their plays
    """
    

    genres = dict()

    # Iterate through the tracks
    for track in data.values():
        # If the genre is not in the dictionary, add it

        if 'Genre' not in track or 'Play Count' not in track:
            continue

        if track['Genre'] not in genres:
            genres[track['Genre']] = 0

        # Increment the genre's play count
        genres[track['Genre']] += track['Play Count']

    # Sort the genres by play count
    sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)

    # Truncate the list if necessary (keep end of list)
    if truncate_at > 0:
        sorted_genres = sorted_genres[:truncate_at]

    return sorted_genres

# Same thing as above, but for artists
def collect_artist_info(data, truncate_at=-1):
    """
    Builds a dataset given a dictionary of tracks
    @param data: a dictionary of tracks from the Apple Music library
    @return a dictionary of artists and their plays
    """

    artists = dict()

    for track in data.values():
        if 'Artist' not in track or 'Play Count' not in track:
            continue

        if track['Artist'] not in artists:
            artists[track['Artist']] = 0

        artists[track['Artist']] += track['Play Count']

    sorted_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)

    if truncate_at > 0:
        sorted_artists = sorted_artists[:truncate_at]

    return sorted_artists

def plot_genre_pie(ax, genre_data):
    """
    Plots the genre data into a pie chart
    @parma ax: the axis to plot the pie chart on
    @param genre_data: a dictionary of genres and their plays

    Note: we assume that the data is sorted by play count
    """

    # Create a pie chart of the genre data
    labels = [genre[0] for genre in genre_data]
    sizes = [genre[1] for genre in genre_data]

    ax.pie(
        sizes,
        labels=labels,
        # autopct='%1.1f%%',
        # explode=explode,
        wedgeprops={'edgecolor': 'white'},
        textprops={'color': 'white'},
        counterclock=False,
        shadow=False,
        startangle=90
    )
    ax.axis('equal')

    # Get handles and labels for legend
    handles, labels = ax.get_legend_handles_labels()

    # Helper functiont to re-order the legend
    def flip(items, ncol):
        return itertools.chain(*[items[i::ncol] for i in range(ncol)])

    ncols = 4
    legend_handles = list(flip(handles, ncols))
    legend_labels = list(flip([ l.lower() for l in labels ], ncols))

    # Add a legend at the bottom
    ax.legend(
        handles=legend_handles,
        labels=legend_labels,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.01),
        ncol=ncols,
        fancybox=False,
        frameon=False,
        shadow=False,
        # fontsize=6,
        
        prop = {'family': 'Helvetica Neue', 'size': 6}
    )

    # Save the plot
    # fig.savefig('genre_pie.png', bbox_inches='tight', dpi=300)

    # return fig

def plot_artist_text(ax, artist_data, count):
    """
    Plots the artist data into a list, where text is the artist name
    and the size is the play count
    @param ax: the axis to plot the artist data on
    @param artist_data: a dictionary of artists and their plays
    """

    # Create a pie chart of the artist data
    artist_length_cutoff = 48
    artists = [artist[0] if len(artist[0]) < artist_length_cutoff else artist[0][:artist_length_cutoff-3] + '...' for artist in reversed(artist_data)]
    playcounts = [artist[1] for artist in reversed(artist_data)]

    # Turn off axis
    ax.axis('off')

    y_offset = 0.0
    y_position = y_offset
    font_scale = 1.2

    for i in range(len(artists)):

        font_size = font_scale * playcounts[i] ** 0.5
        
        ax.text(
            0.5,
            y_position,
            artists[i],
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=font_size,

            # Font
            # fontname='Helvetica Neue Bold',
            # # weight = 'bold',

            font = {
                'family': 'Helvetica Neue',
                'weight': 'bold',
            }
        )

        # Increment the y position based on the text height
        y_position += (1.0 / count) * (0.1) * font_size

    
    # Save the plot
    # ax.savefig('artist_text.png', bbox_inches='tight', dpi=300)
    # return fig


# Test
if __name__ == '__main__':
    # Read the data
    data = read_data()

    # Filter the data to only include songs added in the last year
    data = filter_by_date(data, '2021-01-01')

    TRUNCATE_AT = 18

    # Collect the genre information
    genre_info = collect_genre_info(data, truncate_at=TRUNCATE_AT)

    # Setup plot with two subplots vertically stacked, with figsize
    fig, ax = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(5, 9)
    )
    
    # Plot the genre info
    plot_genre_pie(ax[0], genre_info)

    # Collect the artist information
    artist_info = collect_artist_info(data, truncate_at=TRUNCATE_AT)

    plot_artist_text(ax[1], artist_info, TRUNCATE_AT)

    # Save the plot
    fig.savefig('genre_artist.png', bbox_inches='tight', dpi=300)

    # Show the plot
    plt.show()
