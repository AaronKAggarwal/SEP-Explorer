import json
import numpy as np
from sklearn.manifold import TSNE
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL, TextInput, CustomJS
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from sklearn.neighbors import NearestNeighbors
from matplotlib.cm import inferno
from matplotlib.colors import to_hex

embedded_json_path = 'data/Stanford Plato train cleaned embedded.json'
all_data_path = 'data/Stanford Plato with all data.json'

# Load JSON data
with open(embedded_json_path, 'r') as file:
    data = json.load(file)

with open(all_data_path, 'r') as file:
    link_data = json.load(file)

title_to_url = {item['title']: item['shorturl'] for item in link_data}

# Extract concepts and their vectors
concepts = [item['title'] for item in data]
vectors = np.array([item['embedding'] for item in data])

urls = [f"https://plato.stanford.edu/entries/{title_to_url[concept]}" for concept in concepts]

# Compute t-SNE for dimensionality reduction
tsne = TSNE(n_components=2, random_state=42)
vectors_reduced = tsne.fit_transform(vectors)

X = vectors_reduced

# Step 1: Calculate densities
nbrs = NearestNeighbors(n_neighbors=6).fit(X)  # Too many n_neighbors results in small but tight clusters being missed
distances, indices = nbrs.kneighbors(X)

# Density calculation (inverse of average distance to neighbors)
density = 1 / np.mean(distances, axis=1)

# Normalise the density values to [0, 1] for color mapping
density_normalised = (density - min(density)) / (max(density) - min(density))

# Step 2: Map densities to colors using a colormap
colors = [to_hex(c) for c in inferno(density_normalised)]

# Prepare Bokeh plot
source = ColumnDataSource(data={
    'x': vectors_reduced[:, 0],
    'y': vectors_reduced[:, 1],
    'concept': concepts,
    'url': urls,
    'color': colors,
    'alpha': [0.7] * len(concepts),
    'size': [10] * len(concepts)
})

p = figure(title="Encyclopedia Map", x_axis_label='t-SNE 1', y_axis_label='t-SNE 2',
           tools="pan,wheel_zoom,reset,save,tap")
p.add_tools(HoverTool(tooltips=[("Concept", "@concept")]))

p.title.text_font = "Arial"
p.title.text_font_size = "20pt"
p.title.text_font_style = "bold"

p.background_fill_color = "whitesmoke"
p.grid.visible = False

p.circle('x', 'y', color='color', size='size', source=source, alpha='alpha')

taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url="@url")

# TextInput widget for search
search_input = TextInput(value="", title="Search:")

# CustomJS callback to update the alpha based on search
callback = CustomJS(args=dict(source=source), code="""
    const data = source.data;
    const search_value = cb_obj.value.trim().toLowerCase();

    // Update alpha based on search; highlight matching concepts
    for (let i = 0; i < data.concept.length; i++) {
        if (search_value === "") {
            data.alpha[i] = 0.7;  // Reset alpha if search is cleared
            data.size[i] = 10;
        } else {
            if (data.concept[i].toLowerCase().includes(search_value)) {
                data.alpha[i] = 1.0;  // Make matching points fully opaque
                data.size[i] = 12;   // Increase size for matching points to make them more prominent
            } else {
                data.alpha[i] = 0.1;  // Make non-matching points almost transparent
                data.size[i] = 8;    // Optionally reduce the size of non-matching points
            }
        }
    }
    source.change.emit();
""")

search_input.js_on_change('value', callback)

layout = column(p, search_input)

output_file("tsne_visualisations/concepts_visualisation.html")
show(layout)
