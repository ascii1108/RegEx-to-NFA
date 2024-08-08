import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

def output_nfa(nfa):
    column_width = 10
    print("State".center(column_width), end=" ")
    for symbol in sorted(nfa['letters']):
        print(symbol.center(column_width), end=" ")
    print()
    for state in sorted(nfa['states'], key=lambda x: int(x[1:])):
        state_label = "> " + state if state == nfa['start_state'] else state
        state_label = "* " + state_label if state in nfa['finalStates'] else state_label
        print(state_label.center(column_width), end=" ")
        state_transitions = [t for t in nfa['transitionFunction'] if t[0] == state]
        for symbol in sorted(nfa['letters']):
            destinations = [t[2] for t in state_transitions if t[1] == symbol]
            print(','.join(destinations).center(column_width) if destinations else '-'.center(column_width), end=" ")
        print()


def visualize_nfa(nfa):
    plt.figure(figsize=(10, 10))
    G = nx.MultiDiGraph()

    for state in nfa['states']:
        G.add_node(state)

    for transition in nfa['transitionFunction']:
        G.add_edge(transition[0], transition[2], label=transition[1])

    initial_state = nfa['start_state']
    finalStates = nfa['finalStates']

    pos = nx.spring_layout(G, k=2)
    nx.draw_networkx_nodes(G, pos, node_size=700)

    nx.draw_networkx_labels(G, pos)

    for edge in G.edges(keys=True):
        if edge[0] != edge[1]:
            start = np.array(pos[edge[0]])
            end = np.array(pos[edge[1]])
            direction = end - start
            if np.linalg.norm(direction) != 0:
                direction /= np.linalg.norm(direction)
            start += direction * 0.1
            end -= direction * 0.1
            patch = mpatches.ConnectionPatch(start, end, 'data', 'data', arrowstyle='-|>',
                                             connectionstyle=f'arc3,rad={edge[2] * 0.5}',
                                             mutation_scale=20, lw=1, color='black')
            plt.gca().add_patch(patch)

    # Draw self-loops
    self_loops = [(edge[0], edge[1]) for edge in G.edges(keys=True) if edge[0] == edge[1]]
    nx.draw_networkx_edges(G, pos, edgelist=self_loops, arrowstyle='-|>', connectionstyle='arc3,rad=0.2')

    for edge in G.edges(keys=True):
        label = G.edges[edge]['label']
        start = pos[edge[0]]
        end = pos[edge[1]]
        middle = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        plt.annotate(label, middle, textcoords="offset points", xytext=(0, 10), ha='center')

    nx.draw_networkx_nodes(G, pos, nodelist=[initial_state], node_color='r', node_size=700)

    nx.draw_networkx_nodes(G, pos, nodelist=finalStates, node_color='g', node_size=700)

    plt.title('NFA Visualization')
    plt.axis('off')
    plt.show()
