
import cufflinks as cf
import plotly.offline as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import numpy as np
import pandas as pd

tableau20 = ['rgba(31, 119, 180,1.0)',  'rgba(255, 127, 14,1.0)',     
                 'rgba(44, 160, 44,1.0)', 'rgba(214, 39, 40,1.0)',     
                 'rgba(148, 103, 189,1.0)','rgba(140, 86, 75,1.0)',  
                 'rgba(227, 119, 194,1.0)', 'rgba(127, 127, 127,1.0)',    
                 'rgba(188, 189, 34,1.0)',  'rgba(23, 190, 207,1.0)',
                 'rgba(174, 199, 232,1.0)','rgba(255, 187, 120,1.0)',
                 'rgba(152, 223, 138,1.0)','rgba(255, 152, 150,1.0)',
                 'rgba(197, 176, 213,1.0)', 'rgba(196, 156, 148,1.0)',
                 'rgba(247, 182, 210,1.0)','rgba(199, 199, 199,1.0)',
                'rgba(219, 219, 141,1.0)', 'rgba(158, 218, 229,1.0)',]

def format_standard_cufflinks_chart(df, title, source="", note="", subtitle="", color="", height=800, width=500, line_width=2.5,
	zero_line_emphasis=False,color_coded_legend=False, legend_random_shift=False):

	cf.go_offline()

	dims = (width, height)
	width = line_width

	cufflinks_params = dict(theme='white', dimensions=dims, width=width, asFigure=True)

	#optional cufflinks params
	if color <> "":
		cufflinks_params['color']=color
	else:
		#use tableau colors if no plotly colors are specified
		color = []
		for x in range(len(df.columns)):
			color.append(tableau20[x])
		cufflinks_params['color']=color

	if zero_line_emphasis == True:
		cufflinks_params['hline'] = dict(y=.0001,color='black',width=1.25)



	#use cufflinks to make a quick plot
	fig = df.iplot(**cufflinks_params)

	#update plot margins
	fig['layout'].update(margin=dict(l=100,r=100,t=100,b=120, pad = 0))

	#### annotation time ###
	annotations=[]
	
	#add title to chart
	title_dict = create_title_dict(title=title, subtitle=subtitle)
	annotations.append(title_dict)

	#add note and source to annotations
	note_dict = create_note_dict(note=note, source=source)
	annotations.append(note_dict)

	##add color coded legend to annotations
	if color_coded_legend==True:
		#create color coded legend list
		legend_list = create_color_coded_legend(df, y_shift=legend_random_shift)
		
		#append color coded legend list
		for x in legend_list:
			annotations.append(x)
		fig['layout'].update(margin=dict(l=100,r=190,t=100,b=120, pad = 0))

	#update annotations
	fig['layout'].update(annotations=annotations)

	if color_coded_legend == True:
		fig['layout'].update(showlegend=False)

	return fig



def create_title_dict(title, subtitle):
	
	#format title/subtitle
	#title is bold, subtitle is one line below not bolded
	if subtitle == "":
		title = "<b>%s</b>" % (title)
	else:
		title = "<b>%s</b><br>%s" % (title, subtitle)

	if title == None:
		return None

	title_dict =  dict(showarrow=False,
                        x=-0.062,
                        y=1.2,                                        
                        align='left',
                        text = title,
                        font=dict(size=16,
                                  color='rgb(68,68,68)',),
                        xanchor='left',
                        yanchor='auto',
                        yref='paper',
                        xref='paper')

	return title_dict


def create_note_dict(note, source):

	if note == "":
		note = source
	else:
		source = "<br>%s" % source
		note += source 

	if note == "":
		return None

	#format note/source
	note_dict = dict(showarrow=False,
				        x=-0.062,
				        y=-0.28,                                        
				        align='left',
				        text = note,
				        font=dict(size=12,
				                  color='#444',),
				        xanchor='left',
				        yanchor='auto',
				        yref='paper',
				        xref='paper')

	return note_dict

def create_color_coded_legend(df, y_shift=False):


	df_range = (max(df.max()) - min(df.min())) / 10

	cols = list(df.columns)
	legend_list = []

	for rank, column in enumerate(cols):

		#sometimes ending values are too close together, legends
		#overlap. By putting random shifts on, function can be run
		#until no overlap exists.
		if y_shift == False:
			y_shift_amt = 0
		else:
			y_shift_amt = np.random.uniform(0, df_range, size=1)
			y_shift_amt = y_shift_amt[0]

		y_pos = df[column].values[-1]
		y_pos += y_shift_amt


		legend_list.append(dict(showarrow=False,
	                    x=1.0,
	                    y=y_pos,                                        
	                    align='left',
	                    text = column,
	                    font=dict(size=16,
	                              color=tableau20[rank],),
	                    xanchor='left',
	                    yanchor='auto',
	                    yref='y',
	                    xref='paper')
	                    )

	return legend_list


def shift_legend_entry(fig, col_name, shift_amt):

    annotation_list = []
    
    for col in range(len(fig['layout'].annotations)):

        new_annotation = fig['layout'].annotations[col]
        if new_annotation.text == col_name:
            new_annotation.y += shift_amt       

        annotation_list.append(new_annotation)

    fig['layout'].update(annotations=annotation_list)
    
    return fig

def create_dist_plot_legend(series_name, color):

	dict_legend = dict(showarrow=False,
				        x=.75,
				        y=.9,                                        
				        align='left',
				        text = series_name,
				        font=dict(size=16,
				                  color=color),
				        xanchor='left',
				        yanchor='auto',
				        yref='paper',
				        xref='paper')

	return dict_legend




def format_dist_plot(series, bin_size, title="", subtitle="", series_name = "",source="", note="", color="", xaxis_range=[-1000,1000], 
					tick_distance="", ticklen=6, height=500, width=700):

	names = ['x']
	series_list = []
	series_list.append(series)

	dist_plot_params = dict(hist_data=series_list, group_labels=names, bin_size=bin_size)

	if color <> "":
		color_list = []
		color_list.append(color)
		dist_plot_params['colors'] = color_list


	fig = FF.create_distplot(**dist_plot_params)
	fig['layout'].update(showlegend=False)

	if tick_distance == "":
		tick_distance = bin_size*2

	fig['layout'].update(xaxis = dict(range=xaxis_range,  ticks='outside',ticklen=ticklen ,dtick=tick_distance))
	fig['layout'].update(width=width)
	fig['layout'].update(height=height)


	### Annotation Time ###

	annotations = []
	#add title to chart
	title_dict = create_title_dict(title=title, subtitle=subtitle)
	if title_dict <> None:
		annotations.append(title_dict)

	#add note and source to annotations
	note_dict = create_note_dict(note=note, source=source)
	if note_dict <> None:
		annotations.append(note_dict)

	#add legend to annotations
	dict_legend = create_dist_plot_legend(series_name, color)
	annotations.append(dict_legend)

	#update annotations
	fig['layout'].update(annotations=annotations)

	return fig