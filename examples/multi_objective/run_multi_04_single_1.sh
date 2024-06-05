iteration=300
scenario='multi_04'
log_file="result_${scenario}_single_1.log"
result_file="result_${scenario}_single_1.txt"
csv_file="result_${scenario}_single_1"
sampler_idx=0 #redundant for single graph
sampler_type=dmab # demab / dmab / random / dce / halton / udemab
simulator=scenic.simulators.carla.model
to_plot=False # True / False
simulation_steps=600

rm $scenario/outputs/*traj*.txt
rm $scenario/outputs/*traj*.png
rm $scenario/outputs/$log_file
rm $scenario/outputs/$result_file
rm $scenario/outputs/$csv_file.csv
rm $scenario/outputs/$csv_file\_scatter.png
for seed in $(seq 0 2);
do
    if [[ $to_plot == 'True' ]]; then
        python $scenario/$scenario.py -n $iteration --headless -e $csv_file.$seed -sp $scenario/$scenario.scenic -gp $scenario/$scenario.sgraph -rp $scenario/$scenario\_spec.py -s $sampler_type --seed $seed --using-sampler $sampler_idx -m $simulator --max-simulation-steps $simulation_steps -co $scenario/outputs -o $scenario/outputs --single-graph >> $scenario/outputs/$log_file
        for i in $(seq 0 $(($iteration-1)));
        do
            python $scenario/util/$scenario\_plot_traj.py $scenario/outputs/$scenario\_traj_$i.txt
        done
    else
        python $scenario/$scenario.py -n $iteration --headless -e $csv_file.$seed -sp $scenario/$scenario.scenic -gp $scenario/$scenario.sgraph -rp $scenario/$scenario\_spec.py -s $sampler_type --seed $seed --using-sampler $sampler_idx -m $simulator --max-simulation-steps $simulation_steps -co $scenario/outputs --single-graph >> $scenario/outputs/$log_file
    fi
done
python $scenario/util/$scenario\_collect_result.py $scenario/outputs/$log_file single $sampler_idx >> $scenario/outputs/$result_file
python $scenario/util/$scenario\_analyze_diversity.py $scenario/outputs/ $csv_file single >> $scenario/outputs/$result_file
