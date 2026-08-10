from airdrop_agent.registry import load_targets


def test_twenty_targets_registered():
    targets = load_targets("config/targets.json")
    assert len(targets) == 20
    enabled = [target.id for target in targets if target.enabled]
    assert enabled == ["pacifica", "hibachi", "kyan", "lighter"]
