iteration=300
scenario='multi_04'
log_file="result_${scenario}.log"
result_file="result_${scenario}.txt"
sampler_order=0
sampler_idx=0
sampler_type=demab

rm $scenario/outputs/*.txt
rm $scenario/outputs/*.png
rm $result_file
for seed in $(seq 0 2);
do
    python $scenario/$scenario.py -n $iteration --headless -e $scenario -sp $scenario/$scenario.scenic -gp $scenario/ -rp $scenario/$scenario\_spec.py -s $sampler -o $scenario/outputs --seed $seed --using-sampler $sampler_idx -m scenic.simulators.carla.model --max-simulation-steps 600 --single-graph > $log_file
    for i in $(seq 0 $(($iteration-1)));
    do
        python $scenario/util/$scenario\_plot_traj.py $scenario/outputs/$scenario\_traj_$i.txt
    done
    python $scenario/util/$scenario\_collect_result.py $log_file multi $sampler_order >> $result_file
done