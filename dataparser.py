# This contains the functions for parsing the library XML file

import xml.etree.ElementTree as ET


# Reads the data from file
def read_data(file_path='data/Library.xml'):
    return parseXML(file_path)

# This function parses the XML file and returns a list of tracks
def parseXML(file):
    tree = ET.parse(file)
    root = tree.getroot()[0]

    # Get the root for the dict of tracks
    tracks = root.find('dict')

    # Get the root for the array of playlists
    # TODO: currently not doing anything with playlists
    playlists = root.find('array')

    # Inside the tracks dict, the data is organized where there is a <key>
    # followed by a <dict> with the track data
    # Parse all the tracks and add them to a dictionary
    tracks_data = {}
    for track in tracks:

        # Tag must be a dict
        if track.tag != 'dict':
            continue

        # Get the track data from within the dict
        # Each property is a <key> followed by a another tag of <integer>,
        # <string>, <date>, or <true> or <false>
        track_data_iter = iter(track)
        track_data_dict = {}
        for track_data_key in track_data_iter:
                
                # Must have a tag of 'key'
                assert track_data_key.tag == 'key'
    
                # Get the key
                property_key = track_data_key.text
    
                # Next iter
                track_data_value = next(track_data_iter)
    
                # Tag must be a dict
                property_type = track_data_value.tag
                if property_type == 'integer':
                    property_value = int(track_data_value.text)
                elif property_type == 'string':
                    property_value = track_data_value.text
                elif property_type == 'date':
                    property_value = track_data_value.text
                elif property_type == 'true':
                    property_value = True
                elif property_type == 'false':
                    property_value = False
                else:
                    raise Exception('Unexpected tag: ' + track_data_value.tag)
    
                # Add the key and value to the dict
                track_data_dict[property_key] = property_value

        # Add the track to the tracks dict
        tracks_data[track_data_dict['Track ID']] = track_data_dict 

    return tracks_data


# Test
if __name__ == "__main__":
    print(parseXML("data/Library.xml"))