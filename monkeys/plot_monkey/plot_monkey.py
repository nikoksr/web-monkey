#!/usr/bin/python3
''' imports '''
import sqlite3

import matplotlib.pyplot as plt
import numpy as np


class PlotMonkey():
    ''' Monkey to draw plots based on databases created by an UrlMonkey. '''

    def __init__(self, db_name):
        self.db_name = db_name

    def packup_small_ratios(self, url_dict, min_ratio):
        ''' Packs up ratios in an url ratio dictionary which are smaller
        than the given minimum ratio. '''

        packed_dict = {}
        other = 0.0

        for k, v in url_dict.items():
            if v < min_ratio:
                other += v
                continue
            packed_dict[k] = v

        if other > 0.0:
            packed_dict['Other'] = other

        return packed_dict

    def display_pie(self):
        ''' Read and display the given data in a pie plot. '''

        # Connect and create cursor
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Read all data and close connection
        row_count = c.execute('SELECT * FROM urls')
        row_count = len(row_count.fetchall())

        pie_data = c.execute(
            'SELECT origin, count(*) FROM urls GROUP BY origin')

        # Collect data in dict and calculate ratios
        urls = {}

        for d in pie_data:
            urls[d[0]] = round(float(d[1]) / float(row_count) * 100.0, 2)

        conn.close()

        # Pack up small ratios in dictionary
        urls = self.packup_small_ratios(urls, 1.0)

        # Set labels and sizes based on keys and values from url-dict
        labels = urls.keys()
        sizes = urls.values()

        # Colors
        num_labels = len(labels)
        num_colors = 256
        step = int(float(num_colors) / float(num_labels))
        cmap = plt.get_cmap('terrain')
        colors = cmap(np.arange(0, num_colors, step))

        # explsion
        explode = (0.05, ) * num_labels

        # Create pie
        fig1, ax = plt.subplots()
        fig1.suptitle(
            'Rational distribution of urls found under an url',
            fontsize=14,
            fontweight='bold')

        patches, texts, autotexts = ax.pie(
            sizes,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            explode=explode,
            colors=colors)

        # Draw circle
        center_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig2 = plt.gcf()
        fig2.gca().add_artist(center_circle)

        # Ensure that pie is drawn as a circle and draw pie
        ax.axis('equal')
        plt.legend(labels, loc='best')
        plt.show()
