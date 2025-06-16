# Auto_Pipeline

This repository contains automation scripts for generating and uploading content.

## Privacy Management

The `privacy` module implements utilities to comply with GDPR and CCPA "right to be forgotten" requirements. Use the `PrivacyManager` class to remove a user's data from local storage.

### Deleting a User's Data

```bash
python privacy/privacy_manager.py --delete <USER_ID>
```

This command deletes all records associated with `USER_ID` from `data/user_data.json`. Removing these records ensures we honor user requests for deletion in accordance with GDPR and CCPA regulations.

