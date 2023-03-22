def before_scenario(context, feature):
    for tag in feature.tags:
        if "contract_name" in tag:
            # assert False, tag
            pass


def after_scenario(context, feature):
    for tag in feature.tags:
        print(tag)
