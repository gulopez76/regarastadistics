# -*- coding: utf-8 -*-

class ExampleGrid(JqGrid):
	model = carrier # could also be a queryset
        fields = ['idcarrier', 'codcarrier', 'carriername'] # optional 
        url = reverse_lazy('datacubes:grid_handler')
        caption = 'My First Grid' # optional
        colmodel_overrides = {    # optional
            'idcarrier': { 'editable': False, 'width':11 },
            'codcarrier': { 'editable': False, 'width':3 },
            'carriername': { 'editable': True, 'width':50 },
     	}
