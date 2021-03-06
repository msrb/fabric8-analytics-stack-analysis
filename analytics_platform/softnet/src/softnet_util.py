from analytics_platform.softnet.src.softnet_constants import *
import pandas as pd
import numpy as np


def generate_parent_tuple_list(node_list, edge_dict_list):
    child_to_parent_dict = dict()
    for edge_dict in edge_dict_list:
        child = edge_dict[EDGE_DICT_TO]
        parent = edge_dict[EDGE_DICT_FROM]
        if child_to_parent_dict.has_key(child):
            temp_parent_list = child_to_parent_dict[child]
            temp_parent_list += [node_list.index(parent)]
            child_to_parent_dict[child] = temp_parent_list
        else:
            child_to_parent_dict[child] = [node_list.index(parent)]
    parent_tuple_list = list()
    for node in node_list:
        if child_to_parent_dict.has_key(node):
            parent_tuple_list.append(tuple(child_to_parent_dict[node]))
        else:
            parent_tuple_list.append(())
    return tuple(parent_tuple_list)


def get_similar_package_dict_list(package, package_list, package_to_topic_dict):
    topic_list_1 = package_to_topic_dict[package]
    package_score_dict_list = list()
    for package_2 in package_list:
        topic_list_2 = package_to_topic_dict[package_2]
        similarity_score = calculate_similarity_score(topic_list_1, topic_list_2)
        package_score_dict_list.append({KD_PACKAGE_NAME: package_2, KD_SIMILARITY_SCORE: similarity_score})
    sorted_package_score_dict_list = sorted(package_score_dict_list, key=lambda x: x[KD_SIMILARITY_SCORE], reverse=True)
    return sorted_package_score_dict_list


def calculate_similarity_score(topic_list_1, topic_list_2):
    average_length = (len(topic_list_1) + len(topic_list_2)) / 2
    intersection = [x for x in topic_list_1 if x in topic_list_2]
    return float(len(intersection)) / average_length


def create_empty_pandas_df(rowsize, columns_list):
    zero_data = np.zeros(shape=(rowsize, len(columns_list)), dtype=np.int8)
    df = pd.DataFrame(zero_data, columns=columns_list)
    return df
