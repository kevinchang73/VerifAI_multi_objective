iteration=50
scenario='multi_hri'
log_file='result_run_2.log'
order=alternate

rm $scenario/outputs/*.txt
rm $scenario/outputs/*.png
python $scenario/$scenario.py -n $iteration --headless -e $scenario -sp $scenario/proj_scene_verifai.scenic -gp $scenario/ -rp $scenario/$scenario\_spec.py -s demab   -m scenic.simulators.habitat.model  -o $scenario/outputs > $log_file 
#for i in $(seq 0 $(($iteration-1)));
#do
    #python $scenario/util/$scenario\_plot_traj.py $scenario/outputs/$scenario\_traj_$i.txt
#done
#python $scenario/util/$scenario\_collect_result.py $log_file multi $order
#-m scenic.simulators.carla.model
