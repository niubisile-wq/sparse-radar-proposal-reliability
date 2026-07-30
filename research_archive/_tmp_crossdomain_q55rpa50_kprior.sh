set -euo pipefail

root=/root/autodl-tmp/radar_champion
repo="$root/repos/OpenPCDet_current"
py="$root/envs/radar310/bin/python"
logdir="$root/logs/fair_ablation"
outdir="$root/results"
mkdir -p "$logdir" "$outdir"
export PYTHONPATH="$repo${PYTHONPATH:+:$PYTHONPATH}"

summary="$outdir/crossdomain_q55rpa50_kprior_seed2026.tsv"
printf 'source\ttarget\tap\trecall\n' > "$summary"

source_cfg() {
  case "$1" in
    astyx) echo "$repo/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_astyx_car.yaml" ;;
    truckscenes) echo "$repo/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_truckscenes_car.yaml" ;;
    v2xradarv) echo "$repo/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_v2xradarv_car.yaml" ;;
    kradar) echo "$repo/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_kradar_car.yaml" ;;
    *) return 2 ;;
  esac
}

source_ckpt() {
  case "$1" in
    astyx) echo "$repo/output/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_astyx_car/screen_q55rpa50_kprior_astyx_seed2026/ckpt/checkpoint_epoch_160.pth" ;;
    truckscenes) echo "$repo/output/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_truckscenes_car/screen_q55rpa50_kprior_truckscenes_seed2026/ckpt/checkpoint_epoch_160.pth" ;;
    v2xradarv) echo "$repo/output/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_v2xradarv_car/screen_q55rpa50_kprior_v2xradarv_seed2026/ckpt/checkpoint_epoch_160.pth" ;;
    kradar) echo "$repo/output/root/autodl-tmp/radar_champion/repos/OpenPCDet_current/tools/cfgs/astyx_models/pointpillars_q55rpa50_kprior_kradar_car/screen_q55rpa50_kprior_kradar_seed2026/ckpt/checkpoint_epoch_160.pth" ;;
    *) return 2 ;;
  esac
}

target_dataset() {
  case "$1" in
    astyx) echo AstyxDataset ;;
    truckscenes|v2xradarv|kradar) echo UnifiedRadarDataset ;;
    *) return 2 ;;
  esac
}

target_path() {
  case "$1" in
    astyx) echo "$repo/data/astyx" ;;
    truckscenes) echo "$root/data/man-truckscenes-mini/unified" ;;
    v2xradarv) echo "$root/data/v2x-radar-v-400/unified" ;;
    kradar) echo "$root/data/kradar-400/unified" ;;
    *) return 2 ;;
  esac
}

target_train_info() {
  case "$1" in
    astyx) echo astyx_infos_train.pkl ;;
    truckscenes) echo truckscenes_infos_train.pkl ;;
    v2xradarv) echo v2xradarv_infos_train.pkl ;;
    kradar) echo kradar_infos_train.pkl ;;
    *) return 2 ;;
  esac
}

target_val_info() {
  case "$1" in
    astyx) echo astyx_infos_val.pkl ;;
    truckscenes) echo truckscenes_infos_val.pkl ;;
    v2xradarv) echo v2xradarv_infos_val.pkl ;;
    kradar) echo kradar_infos_val.pkl ;;
    *) return 2 ;;
  esac
}

sources=(astyx truckscenes v2xradarv kradar)
targets=(astyx truckscenes v2xradarv kradar)

for src in "${sources[@]}"; do
  cfg=$(source_cfg "$src")
  ckpt=$(source_ckpt "$src")
  for tgt in "${targets[@]}"; do
    if [[ "$src" == "$tgt" ]]; then
      continue
    fi
    tag="cross_q55rpa50_kprior_${src}_to_${tgt}_seed2026"
    log="$logdir/${tag}_gpu0.log"
    env CUDA_VISIBLE_DEVICES=0 "$py" "$repo/tools/test.py" \
      --cfg_file "$cfg" --batch_size 8 --workers 2 \
      --extra_tag "$tag" --ckpt "$ckpt" \
      --set MODEL.POST_PROCESSING.SCORE_THRESH 0.0 \
           MODEL.POST_PROCESSING.NMS_CONFIG.NMS_THRESH 0.50 \
           DATA_CONFIG.DATASET "$(target_dataset "$tgt")" \
           DATA_CONFIG.DATA_PATH "$(target_path "$tgt")" \
           DATA_CONFIG.INFO_PATH.train "['$(target_train_info "$tgt")']" \
           DATA_CONFIG.INFO_PATH.test "['$(target_val_info "$tgt")']" \
      >"$log" 2>&1
    ap=$(grep -o 'Car radar AP_R40@3D IoU 0.50: [0-9.]*' "$log" | tail -n 1 | awk '{print $NF}')
    recall=$(grep -o 'Car radar max recall: [0-9.]*' "$log" | tail -n 1 | awk '{print $NF}')
    printf '%s\t%s\t%s\t%s\n' "$src" "$tgt" "$ap" "$recall" | tee -a "$summary"
  done
done

cat "$summary"
