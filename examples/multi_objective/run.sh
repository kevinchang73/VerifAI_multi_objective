iteration=10
scenario='multi_02'
rm $scenario/outputs/*.txt
rm $scenario/outputs/*.png
python $scenario/$scenario.py -n $iteration --headless -e $scenario -sp $scenario/$scenario.scenic -gp $scenario/ -rp $scenario/$scenario\_spec.py -s demab -o $scenario/outputs
for i in $(seq 0 $(($iteration-1)));
do
    python $scenario/util/$scenario\_plot_traj.py $scenario/outputs/$scenario\_traj_$i.txt
done
#-m scenic.simulators.carla.model
#python $scenario_old.py -n 2 --headless -e $scenario -p $scenario/$scenario.scenic -s emab -m scenic.simulators.carla.model