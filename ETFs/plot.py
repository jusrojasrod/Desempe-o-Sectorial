# Copyright 2023-2023 Juan Sebastian Rojas Rodriguez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns


def matrix_to_plot(serie):
    """
    Parameters
    ----------
    serie: pandas Series
        Series containing best and worst returns.

    Returns
    -------
    new_names: numpy.ndarray
        Names to plot.
    new_array: numpy.ndarray
        Values to plot.
    """
    length = len(serie)
    # the idea is to shape an a X b matrix
    a = int(np.sqrt(length))
    b = int(np.ceil(length/a))
    m_length = a * b                # matrix "length"

    if m_length >= length:
        # compute how many elements need to be add to the array
        diff = abs(length - m_length)

        # creatre a diff lenght array
        add = np.full(diff, np.nan)
        new_array = np.append(serie, add)
        new_array = new_array.reshape(a, b)

        # add names to the plot
        names = serie.index.to_list()
        add_names = np.full(diff, '---')
        new_names = np.append(names, add_names)
        new_names = new_names.reshape(a, b)

    return new_names, new_array


def heatmap(values, labels, max_, min_, sector, path, show=True):
    """
    Create a heatmap from a numpy array and two lists of labels

    Parameters
    ----------
    values: numpy.ndarray
        Values to plot.
    labels: numpy.ndarray
        Names to plot.
    max_: int
        Max return value.
    min_: int
        Min return value.
    sector: string
        Sector name.

    """
    cmap_ = LinearSegmentedColormap.from_list('rg', ["r", "w", "g"], N=256)

    # "RdYlGn"
    fig, ax = plt.subplots()

    # Especificamos paleta de colores a usar y rango de valores a representar.
    ax.imshow(values, cmap=cmap_, vmin=min_*100, vmax=max_*100)
    # borrar axis labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Reducimos la longitud de las marcas a 0 para que no sean visibles
    ax.tick_params(axis=u'both', which=u'both', length=0)
    for lado in ['left', 'right', 'bottom', 'top']:
        ax.spines[lado].set_visible(False)

    # # Indicamos las posiciones donde dibujaremos la rejilla
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    ax.set_xticks(np.arange(xmin, xmax+1), minor=True)
    ax.set_yticks(np.arange(ymax, ymin+1), minor=True)

    # Dibujamos la rejilla de color blanco para que actue como separador.
    # ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
    # ax.tick_params(which="minor", bottom=False, left=False)

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            # print(i, j, values[i,j])
            text = ax.text(j, i, str(labels[i, j]) + '\n' + str(values[i, j])+'%',
                           ha="center", va="center", color="k", size=6)

    ax.set_title(f"{sector}\n")

    plt.savefig(f"{path}/{sector}.png")

    if show is True:
        plt.show()


def plot_bar_sectors(x, y):
    """
    """
    # Establecer un tema
    sns.set_style("darkgrid")

    ax = sns.barplot(x=x, y=y, color="r")
    ax.bar_label(ax.containers[0], fontsize=8)
    ax.set_xticklabels( 
        labels=x, rotation=90, size=8)

    ax.set(xlabel='Sectores', ylabel='Retorno (%)',
           title='Rendimiento en la última semana de los Sectores')

    plt.show()
