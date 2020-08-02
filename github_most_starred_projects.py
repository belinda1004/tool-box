#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# Get the top 30 most starred projects on Github by language.
# Generate a bar chart by the inquiry result.
# Click each bar to open the home page of the project.

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS


def get_most_starred_projects_by_language(language):

    url = 'https://api.github.com/search/repositories?q=language:%s&sort=stars' % language
    target = language + '_most_starred_projects.svg'
    try:
        r = requests.get(url)
    except:
        print('Network error.')
        return False

    if r.status_code != 200:
        print("Error (code: %d)." % r.status_code)
        return False

    response_dict = r.json()

    repo_dicts = response_dict['items']
    title = "Top %d rated %s repositories: " % (len(repo_dicts),language)

    names = []
    plot_dicts = []
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])
        plot_dict = {
            'value': repo_dict['stargazers_count'],
            'label': repo_dict['description'],
            'xlink': repo_dict['html_url'],
        }
        if not plot_dict['label']:
            plot_dict['label'] = ''
        plot_dicts.append(plot_dict)

    my_style = LS('#333366', base_style=LCS)


    my_config = pygal.Config()
    my_config.x_label_rotation = 45
    my_config.show_legend = False
    my_config.title_font_size = 24
    my_config.label_font_size = 14
    my_config.major_label_font_size = 18
    my_config.truncate_label = 15
    my_config.show_y_guides = False
    my_config.width = 1000


    chart = pygal.Bar(my_config,style=my_style)
    chart.title = 'Most-Starred %s Projects on GitHub' % language.capitalize()
    chart.x_labels = names
    chart.add('', plot_dicts)
    chart.render_to_file(target)
    print('Save result to %s. Please open it in your web browser.' % target)
    return True



while True:
    language = input('Inquiry the most starred projects written by language: ')
    if get_most_starred_projects_by_language(language.lower()):
        break
