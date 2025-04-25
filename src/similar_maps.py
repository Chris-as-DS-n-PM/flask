import numpy as np
import os
from src.array_funcs import ArrayFuncs

"""
Takes a beatmap id as input and returns an array of the most similar maps.
The map must have a leaderboard (ranked, loved, approved)
"""
def get_similar_maps(beatmap_id):
    af = ArrayFuncs()

    # Get cached tables and load them into tables
    current_directory = os.getcwd()
    map_table_filename = os.path.join(current_directory, "api", "src", "tables", "map_table_all.npy")
    data_table_filename = os.path.join(current_directory, "api", "src", "tables", "data_table_all.npy")
    map_table = af.load_numpy_array(map_table_filename)
    data_table = af.load_numpy_array(data_table_filename)

    # Get index of the current map in the table
    ref_index = np.where(map_table[:, 0] == beatmap_id)[0][0]
    bpm = data_table[ref_index][1]

    # Determine a "normalized" BPM compared to the current map
    # NOTE: This is only based on halved/doubled BPMS or similar.
    #       Not sure of a better way to implement this, especially for maps with different time signatures (ex. 1/3)
    for data_stats in data_table:
        bpms = np.array([data_stats[1] / 4, data_stats[1] / 2, data_stats[1], data_stats[1] * 2, data_stats[1] * 4])
        i = np.argmin(np.abs(bpms - bpm))
        stdized_bpm = bpms[i]
        data_stats[1] = stdized_bpm

    # SR, BPM, CS, AR, Slider factor, Circle/slider ratio, Aim/speed ratio, Speed/objects ratio
    # NOTE: This is based on my personal testing of what "finds" similar maps currently based on these stats.
    #       Will likely change with playtesting and more feedback.
    weights = [1.5, 0.5, 0.25, 0.25, 0.5, 1.5, 2, 0]

    # Standardize the table's statistics with the weights
    stdized_table = af.preprocess_data(data_table, weights)

    # Find the indices in the map table of the most similar maps
    # TODO: Change top_n to past 10, currently only 10 for testing
    # TODO: Implement the distances into the website
    similar_indices, distances = af.find_most_similar(stdized_table, ref_index, top_n=10)
    
    # Build an array of the most similar beatmap ids
    beatmap_ids = []
    for index in similar_indices:
        beatmap_ids.append(map_table[index][0])
    
    return beatmap_ids