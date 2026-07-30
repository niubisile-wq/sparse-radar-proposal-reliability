#!/usr/bin/env bash
set -euo pipefail

seed="${1:?usage: $0 SEED}"
root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
python_bin="$root/envs/radar310/bin/python"
cfg_dir="$repo/tools/cfgs/astyx_models"
log_dir="$root/logs/fair_ablation"
status="$log_dir/wave_dapg_seed${seed}.status"
mkdir -p "$log_dir"

export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"
cd "$repo"

run_experiment() {
    local gpu="$1"
    local dataset="$2"
    local cfg="$3"
    shift 3

    local tag="fair_bevgate_dapg_${dataset}_seed${seed}"
    local log="$log_dir/${tag}_gpu${gpu}.log"
    echo "$(date -Iseconds) START gpu=$gpu tag=$tag" | tee -a "$status"

    env CUDA_VISIBLE_DEVICES="$gpu" "$python_bin" -u tools/train.py \
        --cfg_file "$cfg" \
        --batch_size 4 \
        --epochs 160 \
        --workers 4 \
        --extra_tag "$tag" \
        --fix_random_seed \
        --seed "$seed" \
        --ckpt_save_interval 160 \
        --max_ckpt_save_num 1 \
        "$@" >"$log" 2>&1

    echo "$(date -Iseconds) END gpu=$gpu tag=$tag exit=0" | tee -a "$status"
}

run_experiment \
    0 astyx "$cfg_dir/pointpillars_bevgate_dapg_astyx_car.yaml" \
    --set \
    DATA_CONFIG.DATASET AstyxDataset \
    DATA_CONFIG.DATA_PATH "$repo/data/astyx" \
    DATA_CONFIG.INFO_PATH.train "['astyx_infos_train.pkl']" \
    DATA_CONFIG.INFO_PATH.test "['astyx_infos_val.pkl']" &

run_experiment \
    1 truckscenes "$cfg_dir/pointpillars_bevgate_dapg_truckscenes_car.yaml" \
    --set \
    DATA_CONFIG.DATASET UnifiedRadarDataset \
    DATA_CONFIG.DATA_PATH "$root/data/man-truckscenes-mini/unified" \
    DATA_CONFIG.INFO_PATH.train "['truckscenes_infos_train.pkl']" \
    DATA_CONFIG.INFO_PATH.test "['truckscenes_infos_val.pkl']" &

run_experiment \
    2 v2xradarv "$cfg_dir/pointpillars_bevgate_dapg_v2xradarv_car.yaml" \
    --set \
    DATA_CONFIG.DATASET UnifiedRadarDataset \
    DATA_CONFIG.DATA_PATH "$root/data/v2x-radar-v-400/unified" \
    DATA_CONFIG.INFO_PATH.train "['v2xradarv_infos_train.pkl']" \
    DATA_CONFIG.INFO_PATH.test "['v2xradarv_infos_val.pkl']" &

run_experiment \
    3 kradar "$cfg_dir/pointpillars_bevgate_dapg_kradar_car.yaml" \
    --set \
    DATA_CONFIG.DATASET UnifiedRadarDataset \
    DATA_CONFIG.DATA_PATH "$root/data/kradar-400/unified" \
    DATA_CONFIG.INFO_PATH.train "['kradar_infos_train.pkl']" \
    DATA_CONFIG.INFO_PATH.test "['kradar_infos_val.pkl']" &

wait
echo "$(date -Iseconds) WAVE_COMPLETE" | tee -a "$status"
