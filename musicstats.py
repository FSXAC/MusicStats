from math import trunc
from dataparser import *

import matplotlib.pyplot as plt

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

def plot_genre_pie(genre_data):
    """
    Plots the genre data into a pie chart
    @param genre_data: a dictionary of genres and their plays

    Note: we assume that the data is sorted by play count
    """

    # Create a pie chart of the genre data
    labels = [genre[0] for genre in genre_data]
    sizes = [genre[1] for genre in genre_data]

    # Explode all the slices just a bit
    # explode = [0.1 for i in range(len(sizes))]

    plt.pie(
        sizes,
        # labels=labels,
        # autopct='%1.1f%%',
        # explode=explode,
        wedgeprops={'edgecolor': 'white'},
        counterclock=False,
        shadow=False,
        startangle=90
    )
    plt.axis('equal')

    # Add a legend at the bottom
    plt.legend(
        loc='upper center',
        labels=[ l.lower() for l in labels ],
        bbox_to_anchor=(0.5, -0.01),
        ncol=4,
        # mode='expand',
        fancybox=False,
        frameon=False,
        shadow=False
    )

    # Save the plot
    plt.savefig('genre_pie.png', bbox_inches='tight', dpi=300)

def plot_artist_text(artist_data):
    """
    Plots the artist data into a list, where text is the artist name
    and the size is the play count
    @param artist_data: a dictionary of artists and their plays
    """

    # Create a pie chart of the artist data
    artists = [artist[0] for artist in reversed(artist_data)]
    playcounts = [artist[1] for artist in reversed(artist_data)]

    # Create a new plot
    plt.figure(figsize=(10, 10))

    # Turn off axis
    plt.axis('off')

    # For each artist, plot the artist's name
    for i, artist in enumerate(artists):
        plt.text(
            0.5,
            0.06 * i,
            artist,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=(playcounts[i] ** 0.5),

            # Bold
            weight='bold'
        )
    
    # Save the plot
    plt.savefig('artist_text.png', bbox_inches='tight', dpi=300)


# Test
if __name__ == '__main__':
    # Read the data
    data = read_data()

    TRUNCATE_AT = 18

    # Collect the genre information
    genre_info = collect_genre_info(data, truncate_at=TRUNCATE_AT)
    
    # Plot the genre info
    plot_genre_pie(genre_info)

    # Collect the artist information
    artist_info = collect_artist_info(data, truncate_at=TRUNCATE_AT)

    # Print the artists
    for artist, count in artist_info:
        print(artist, count)

    plot_artist_text(artist_info)
