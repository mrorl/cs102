import igraph
import time
from api import get_friends
from igraph import Graph, plot


def get_network(users_ids, as_edgelist=True):
    graph = []
    matrix = [[0 for i in range(len(users_ids))] for j in range(len(users_ids))]

    for user1 in range(len(users_ids)):
        response = get_friends(users_ids[user1])
        if response.get('error'):
            continue
        friends_list = response['response']['items']
        for user2 in range(user1 + 1, len(users_ids)):
            if users_ids[user2] in friends_list:
                if as_edgelist:
                    graph.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.4)
        print("slept, unlike you")
       
    if as_edgelist:
        return graph
    else:
        return matrix


def plot_graph(graph):
    vertices = [i for i in range(len(friends))]  # здесь указываем колтичество вершин - кол-во друзей
    edges = graph  # здесь указываем ребра графа - кто у кого в друзьях из твоих друзей

    # Создание графа
    g = Graph(vertex_attrs={"label": vertices, "shape": "circle", "size": 10},
    edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {
       "vertex_size": 20,
       "edge_color": "gray",
       "layout": g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)
    }

    # Удаляем петли и повторяющиеся ребра
    g.simplify(multiple=True, loops=True)

    # Разделяем вершины на группы по взаимосвязям
    clusters = g.community_multilevel()
    print(clusters)

    # Раскрашиваем разные группы вершин в разные цвета
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # Отрисовываем граф
    plot(g, **visual_style)


if __name__ == '__main__':
    response = get_friends(57902269)
    friends = response['response']['items'] 
    graph = get_network(friends, as_edgelist=True)
    plot_graph(graph)
