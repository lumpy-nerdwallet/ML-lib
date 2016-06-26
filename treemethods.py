import networkx as nx

class RegressionTree:
    """
    
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.graph.add_node(1, variable = None, cutoff = None)
        self.nodes = 1
        self.X = None
        self.y = None
        self.learned = False
        
    def fit(self, X, y):
        self.X = X
        self.y = y
    
    def set_node(self, node_number, variable, cutoff):
        self.graph.node[node_number]['variable'] = variable
        self.graph.node[node_number]['cutoff'] = cutoff
        
    def new_nodes(self, parent, number):
        for i in range(number):
            self.nodes += 1
            self.graph.add_edge(parent, self.nodes)
        
    def CART(self, inputs, values):
        min_error = np.inf
        min_feature = None
        min_split = None
        for feature in range(np.shape(inputs)[1]):
            feature_vector = inputs[:, feature]
            sorted_vector = np.unique(np.sort(feature_vector))
            feature_splits = (sorted_vector[1:] + sorted_vector[:-1]) / 2
            for split in feature_splits:
                lower_class_average = np.mean(values[feature_vector < split])
                upper_class_average = np.mean(values[feature_vector > split])
                lower_class_errors = values[feature_vector < split] - lower_class_average
                upper_class_errors = values[feature_vector > split] - upper_class_average
                total_error = np.inner(lower_class_errors, lower_class_errors) + np.inner(upper_class_errors, upper_class_errors)
                if total_error < min_error:
                    min_error = total_error
                    min_feature = feature
                    min_split = split
        return min_feature, min_split
        
    def add_split(self, node_number):
        min_feature, min_split = self.CART(self.X, self.y)
        self.set_node(node_number, min_feature, min_split)
        self.new_nodes(self.nodes, 2)
        
    def get_predecessors(self, node_number):
        predecessors = []
        current_node = node_number
        print(current_node)
        while len(self.graph.predecessors(current_node)) > 0:
            current_node = self.graph.predecessors(current_node)[0]
            predecessors.append(current_node)
        return predecessors
        
    def partition_data(self, node_number):
        predecessors = self.get_predecessors(node_number)
        predecessors.reverse()
        predecessors.append(node_number)
        data_indices = np.array(range(len(self.y)))
        node_count = 0
        print(data_indices)
        while node_count < len(predecessors) - 1:
            current_node = predecessors[node_count]
            next_node = predecessors[node_count + 1]
            current_variable = self.graph.node[current_node]['variable']
            current_cutoff = self.graph.node[current_node]['cutoff']
            if next_node == min(self.graph.successors(current_node)):
                print( self.X[data_indices, current_variable] < current_cutoff)
                data_indices = data_indices[self.X[data_indices, current_variable] < current_cutoff]
            else:
                data_indices = data_indices[self.X[data_indices, current_variable] > current_cutoff]
            node_count +=1
        return data_indices
        
            
        
a = RegressionTree()        
a.fit(X, y)    
a.add_split(1)
a.graph.add_edge(2, 5)
print(a.partition_data(2))
nx.draw(a.graph)
pos=nx.spring_layout(a.graph)
labels = {1: str(a.graph.node[1]['variable']) + ": " +str(a.graph.node[1]['cutoff'])}
nx.draw_networkx_labels(a.graph, pos, labels)



