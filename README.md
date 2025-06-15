# Auto Pipeline

This repository contains automation scripts for keyword discovery and publishing.

## Google Ads Integration

To fetch real CPC values for each keyword, the pipeline uses the Google Ads API.
Set the following environment variables before running `keyword_auto_pipeline.py`:

- `GOOGLE_ADS_DEVELOPER_TOKEN`
- `GOOGLE_ADS_CLIENT_ID`
- `GOOGLE_ADS_CLIENT_SECRET`
- `GOOGLE_ADS_REFRESH_TOKEN`
- `GOOGLE_ADS_CUSTOMER_ID`
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID` *(optional)*

Refer to the [Google Ads API documentation](https://developers.google.com/google-ads/api/docs/client-libs/python/oauth-service) for steps to obtain these credentials.
