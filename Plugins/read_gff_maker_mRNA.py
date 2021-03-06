#read_gff_maker_mRNA.py

import pandas as pd
from Plugins.__read_gff_maker__ import __ReadGFFMaker__
from Bio.SeqFeature import SeqFeature, FeatureLocation, CompoundLocation

class Plugin(__ReadGFFMaker__):

    """
    """
    def feature_initialize(self, pre_feature, metadata):
        refactor_pre_feature = lambda element: FeatureLocation(
            int(element[0]),
            int(element[1]),
            (1,-1)[element[2] == "-"]
        )
        merge_pre_feature = lambda  array: array[0] if len(array) == 1 else CompoundLocation(array)

        return SeqFeature(
            merge_pre_feature(
                pre_feature.apply(refactor_pre_feature, axis=1)
            ),
            type="mRNA",
            qualifiers={
                "gene":None
            }
        )

    """
    """
    def process(self, app, caller_mode, key_handle, calls:list=[], target=None):
        try:
            feature = self.feature_initialize(
                app.handles[key_handle].loc[(target[0], f"{target[1]}-mRNA-1", "CDS"),:].reset_index(),
                app.metadata
            )
        except KeyError:
            return None
            
        feature.qualifiers["gene"]=target[1]
        receiver = self.callbacks(
            app,
            calls,
            (target[0], f"{target[1]}-mRNA-1", "mRNA")
        )
        
        return self.merge(feature, receiver)