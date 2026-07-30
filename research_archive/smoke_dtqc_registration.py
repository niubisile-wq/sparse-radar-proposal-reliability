from pcdet.config import cfg, cfg_from_yaml_file
from pcdet.models.dense_heads import __all__ as dense_heads


assert "AnchorHeadDualTargetConsensus" in dense_heads
cfg_from_yaml_file(
    "tools/cfgs/astyx_models/pointpillars_dtqc_astyx_car.yaml", cfg
)
assert cfg.MODEL.DENSE_HEAD.NAME == "AnchorHeadDualTargetConsensus"
assert float(cfg.MODEL.DENSE_HEAD.QUALITY_FUSION_ALPHA) == 0.5
print("DTQC registration/config smoke: PASS")

cfg.clear()
cfg_from_yaml_file(
    "tools/cfgs/astyx_models/pointpillars_dtqcatss_astyx_car.yaml", cfg
)
assert cfg.MODEL.DENSE_HEAD.NAME == "AnchorHeadDualTargetConsensus"
assert cfg.MODEL.DENSE_HEAD.TARGET_ASSIGNER_CONFIG.NAME == "ATSS"
assert int(cfg.MODEL.DENSE_HEAD.TARGET_ASSIGNER_CONFIG.TOPK) == 9
print("DTQC+ATSS registration/config smoke: PASS")
