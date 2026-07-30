#!/usr/bin/env bash
set -euo pipefail

gpu="${1:?usage: $0 GPU DATASET}"
dataset="${2:?usage: $0 GPU DATASET}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg_dir="$repo/tools/cfgs/astyx_models"
log_dir="$root/logs/fair_ablation"
status="$log_dir/stable_gate_lane_gpu${gpu}_${dataset}.status"
mkdir -p "$log_dir"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

case "$dataset" in
    astyx)
        overrides=(--set DATA_CONFIG.DATASET AstyxDataset
            DATA_CONFIG.DATA_PATH "$repo/data/astyx"
            DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']")
        ;;
    truckscenes)
        overrides=(--set DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified"
            DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']")
        ;;
    v2xradarv)
        overrides=(--set DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified"
            DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']")
        ;;
    kradar)
        overrides=(--set DATA_CONFIG.DATASET UnifiedRadarDataset
            DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified"
            DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']"
            DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']")
        ;;
    *) echo "unsupported dataset: $dataset" >&2; exit 2 ;;
esac

run_one() {
    local module="$1" seed="$2" cfg tag log
    if [[ "$module" == "pointpillars" ]]; then
        cfg="$cfg_dir/pointpillars_bevgate_${dataset}_car.yaml"
    else
        cfg="$cfg_dir/pointpillars_stable_bevgate_${dataset}_car.yaml"
    fi
    tag="fair_${module}_${dataset}_seed${seed}"
    log="$log_dir/${tag}_gpu${gpu}.log"
    if [[ -f "$log" ]] && grep -q 'Evaluation done' "$log"; then
        echo "$(date -Iseconds) SKIP_COMPLETE tag=$tag" | tee -a "$status"
        return
    fi
    echo "$(date -Iseconds) START tag=$tag" | tee -a "$status"
    cd "$repo"
    if [[ "$module" == "pointpillars" ]]; then
        env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/train.py \
            --cfg_file "$cfg" --batch_size 4 --epochs 160 --workers 4 \
            --extra_tag "$tag" --fix_random_seed --seed "$seed" \
            --ckpt_save_interval 160 --max_ckpt_save_num 1 \
            --set MODEL.BACKBONE_2D.USE_BEV_ATTENTION False \
            "${overrides[@]:1}" >"$log" 2>&1
    else
        env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/train.py \
            --cfg_file "$cfg" --batch_size 4 --epochs 160 --workers 4 \
            --extra_tag "$tag" --fix_random_seed --seed "$seed" \
            --ckpt_save_interval 160 --max_ckpt_save_num 1 \
            "${overrides[@]}" >"$log" 2>&1
    fi
    echo "$(date -Iseconds) END tag=$tag exit=0" | tee -a "$status"
}

echo "$(date -Iseconds) LANE_QUEUED gpu=$gpu dataset=$dataset" >>"$status"
while pgrep -f "tools/train.py.*fair_.*_${dataset}_seed" >/dev/null; do
    sleep 10
done
for seed in 2027 2028; do
    run_one pointpillars "$seed"
done
for seed in 2026 2027 2028; do
    run_one stable_bevgate "$seed"
done
echo "$(date -Iseconds) LANE_COMPLETE" | tee -a "$status"
