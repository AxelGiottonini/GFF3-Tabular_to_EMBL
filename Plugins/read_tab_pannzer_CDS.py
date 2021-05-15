#read_tab_pannzer_CDS

import pandas as pd

class Plugin:

    """
    """
    def feature_initialize(self, pre_feature, metadata):
        #print(self.feature_initialize_db_xref(pre_feature))
        return {
            "db_xref": self.feature_initialize_db_xref(pre_feature),
            "translation": self.feature_initialize_translation(pre_feature),
            "product": self.feature_initialize_product(pre_feature)
        }

    """
    """
    def feature_initialize_db_xref(self, pre_feature):
        sender = pd.Series([])

        for field in ["BP_ARGOT", "CC_ARGOT", "MF_ARGOT"]:
            try:
                sender = pd.concat([sender, pre_feature(field)["id"]])
            except KeyError:
                pass
        return [f"GO:{str(element)}" for element in sender]

    """
    """
    def feature_initialize_translation(self, pre_feature):
        sender = list()
        try:
            sender = [pre_feature("qseq").iloc[0,1]]
        except KeyError:
            pass
        return sender 

    """
    """
    def feature_initialize_product(self, pre_feature):
        sender = list()
        try:
            sender = [pre_feature("DE").iloc[0,1]]
        except KeyError:
            pass
        return sender

    """
    """
    def callbacks(self, app, calls, target):
        sender = []

        for app, key_plugin, *args in calls:
            temp = app.plugins[key_plugin].process(app, *args, target)
            if temp:
                sender += temp
    
        return sender

    """
    """
    def merge(self, feature, receiver):
        return feature

    """
    """
    def process(self, app, key_handle, calls:list=[], target=None):

        feature = self.feature_initialize(
            (lambda field: app.handles[key_handle].loc[(target[1], field)].reset_index()),
            app.metadata)

        receiver = self.callbacks(
            app,
            calls,
            target
        )

        return self.merge(feature, receiver)