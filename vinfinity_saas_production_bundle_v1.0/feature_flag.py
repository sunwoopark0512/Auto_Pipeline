from ldclient import LDClient, Context

ld = LDClient("LAUNCHDARKLY_SDK_KEY")

def flag_on(user_id: str, flag_key: str) -> bool:
    ctx = Context.builder(user_id).build()
    return ld.variation(flag_key, ctx, False)
