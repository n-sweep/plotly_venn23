import plotly.graph_objs as go
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3


def venn23(sets, labels, colors, title=None, opacity=0.6):
    fig = go.Figure()

    # piggyback on matplotlib_venn for geometry
    if len(sets) == 2:
        venn = venn2(sets, labels)
    elif len(sets) == 3:
        venn = venn3(sets, labels)
    plt.close()

    # reset venn labels to show full set sizes
    for text, label in zip([len(s) for s in sets], venn.set_labels):
        label.set_text(text)

    for i, ((x, y), radius) in enumerate(zip(venn.centers, venn.radii)):
        # draw the circle
        fig.add_shape(
            type='circle',
            x0=x - radius,
            y0=y - radius,
            x1=x + radius,
            y1=y + radius,
            line={
                'width': 1,
                'color': 'black'
            },
            fillcolor=colors[i],
            opacity=opacity
        )

        # add a trace for generating the legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            name=labels[i],
            mode='markers',
            marker={
                'size': 15,
                'color': colors[i],
                'opacity': opacity
            }
        ))

    # draw label annotations
    for label in venn.set_labels + venn.subset_labels:
        x, y = label.get_position()
        txt = label.get_text()
        fig.add_annotation(
            x=x,
            y=y,
            text=txt,
            showarrow=False
        )

    axes_settings = {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    }
    fig.update_yaxes(**axes_settings)
    fig.update_xaxes(**axes_settings)

    fig.update_layout(
        title=title,
        plot_bgcolor='white',
        yaxis={'scaleanchor': 'x', 'scaleratio': 1},
        margin={c: 60 for c in 'lrbt'}
    )

    return fig
