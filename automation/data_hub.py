class DataHub:
    """Collects and merges various data sources."""

    def collect_social_trends(self):
        # Example: Query a social API. Here we return mock data.
        return {"social_trends": ["trend1", "trend2"]}

    def collect_keyword_data(self):
        # Example: Pull from an SEO tool.
        return {"keywords": ["keyword1", "keyword2"]}

    def collect_competitor_info(self):
        return {"competitors": ["comp1", "comp2"]}

    def collect_site_metrics(self):
        return {"site": {"views": 1000}}

    def collect_all(self):
        data = {}
        data.update(self.collect_social_trends())
        data.update(self.collect_keyword_data())
        data.update(self.collect_competitor_info())
        data.update(self.collect_site_metrics())
        return data
