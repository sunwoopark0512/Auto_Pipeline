from feast import FeatureStore

store = FeatureStore(repo_path="feature_store/feature_repo")

def feature_row(user_id):
    feats = store.get_online_features(
        features=[
            "user_events_5m:views_5m",
            "user_events_5m:clicks_5m",
            "user_conversion_stats:total_revenue",
        ],
        entity_rows=[{"user_id": user_id}]
    ).to_dict()
    return {k: v[0] for k, v in feats.items()}
