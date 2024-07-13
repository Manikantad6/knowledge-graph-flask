import networkx as nx
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt


def create_graph_image(df):
    # Create a directed graph
    G = nx.DiGraph()
    countries_list = df['Country'].unique()
    states_list = df['State'].unique()
    city_list = df['City'].unique()

    print(countries_list)

    # Add countries
    G.add_nodes_from(countries_list, type='country')

    # Add states
    G.add_nodes_from(states_list, type='state')

    # Add cities
    G.add_nodes_from(city_list, type='city')

    # Main node to link all countries
    G.add_node("countries", type="countries")

    # Add edges with labels to establish relationships
    for index, row in df.iterrows():
        G.add_edge(row['Country'], 'countries', relation='country')
        G.add_edge(row['Country'], row['State'], relation='state')
        G.add_edge(row['State'], row['City'], relation='city')
    
    

    # Define node colors based on their type
    node_colors = []
    for node in G.nodes(data=True):
        if node[1]['type'] == 'country':
            node_colors.append('red')
        elif node[1]['type'] == 'state':
            node_colors.append('green')
        elif node[1]['type'] == 'city':
            node_colors.append('blue')
        else:
            node_colors.append('orange')

    # Draw the graph with increased figure size
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=5000, font_size=10, font_color='white')
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='gray')

    plt.title("Geographic Relationships: Cities, States, and Countries")
    plt.savefig('static/graph.png')  # Save the figure as an image
    plt.close()
