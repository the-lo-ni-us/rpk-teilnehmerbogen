class CompositeCol(list):
    def __init__(self, *liste):
        list.__init__(self, liste)
    def __composite_values__(self):
        return self
