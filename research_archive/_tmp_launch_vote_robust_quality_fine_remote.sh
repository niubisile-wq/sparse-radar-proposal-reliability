set -eu

root=/root/autodl-tmp/radar_champion
repo=$root/repos/OpenPCDet_current
py=$root/envs/radar310/bin/python

launch_dataset() {
  dataset=$1
  gpu=$2
  case "$dataset" in
    astyx)
      cfg=$repo/tools/cfgs/astyx_models/pointpillars_taac_astyx_car.yaml
      input=$root/results/aeq_stable_bevgate_iou0p30_a0p30_p0p25_u0p50_astyx_seed2028.pkl
      data_set=AstyxDataset
      data_path=$repo/data/astyx
      train_info="['astyx_infos_train.pkl']"
      test_info="['astyx_infos_val.pkl']"
      ;;
    truckscenes)
      cfg=$repo/tools/cfgs/astyx_models/pointpillars_taac_truckscenes_car.yaml
      input=$root/results/aeq_stable_bevgate_iou0p30_a0p30_p0p25_u0p50_truckscenes_seed2028.pkl
      data_set=UnifiedRadarDataset
      data_path=$root/data/man-truckscenes-mini/unified
      train_info="['truckscenes_infos_train.pkl']"
      test_info="['truckscenes_infos_val.pkl']"
      ;;
    v2xradarv)
      cfg=$repo/tools/cfgs/astyx_models/pointpillars_taac_v2xradarv_car.yaml
      input=$root/results/aeq_stable_bevgate_iou0p30_a0p30_p0p25_u0p50_v2xradarv_seed2028.pkl
      data_set=UnifiedRadarDataset
      data_path=$root/data/v2x-radar-v-400/unified
      train_info="['v2xradarv_infos_train.pkl']"
      test_info="['v2xradarv_infos_val.pkl']"
      ;;
    kradar)
      cfg=$repo/tools/cfgs/astyx_models/pointpillars_taac_kradar_car.yaml
      input=$root/results/aeq_stable_bevgate_iou0p30_a0p30_p0p25_u0p50_kradar_seed2028.pkl
      data_set=UnifiedRadarDataset
      data_path=$root/data/kradar-400/unified
      train_info="['kradar_infos_train.pkl']"
      test_info="['kradar_infos_val.pkl']"
      ;;
    *)
      exit 2
      ;;
  esac

  for vote_iou in 0.23 0.24 0.25; do
    for strength in 0.38 0.40 0.42 0.44 0.45; do
      tag=m3rob_q15p25_viou${vote_iou/./p}_s${strength/./p}
      log=$root/logs/fair_ablation/${tag}_${dataset}_seed2028_gpu${gpu}.log
      output=$root/results/${tag}_${dataset}_seed2028.pkl
      CUDA_VISIBLE_DEVICES=$gpu "$py" "$root/evaluate_box_voting.py" \
        --cfg_file "$cfg" --input "$input" --output "$output" \
        --vote_iou "$vote_iou" --strength "$strength" --mode xy \
        --residual_count 50 \
        --set DATA_CONFIG.DATASET "$data_set" DATA_CONFIG.DATA_PATH "$data_path" \
          DATA_CONFIG.INFO_PATH.train "$train_info" DATA_CONFIG.INFO_PATH.test "$test_info" \
        >"$log" 2>&1
    done
  done
}

launch_dataset astyx 0 > $root/logs/fair_ablation/fine_launch_astyx.out 2>&1 &
launch_dataset truckscenes 1 > $root/logs/fair_ablation/fine_launch_truckscenes.out 2>&1 &
launch_dataset v2xradarv 2 > $root/logs/fair_ablation/fine_launch_v2xradarv.out 2>&1 &
launch_dataset kradar 3 > $root/logs/fair_ablation/fine_launch_kradar.out 2>&1 &
wait

