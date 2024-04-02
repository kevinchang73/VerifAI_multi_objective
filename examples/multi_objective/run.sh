iteration=2
rm multi_03/outputs/*.txt
rm multi_03/outputs/*.png
python multi_03/multi_03.py -n $iteration --headless -e multi_03 -sp multi_03/multi_03.scenic -gp multi_03/ -rp multi_03/multi_03_spec.py -s demab -o multi_03/outputs
for i in $(seq 0 $(($iteration-1)));
do
    python util/plot_traj.py multi_03/outputs/multi_03_traj_$i.txt
done
#-m scenic.simulators.carla.model
#python multi_03_old.py -n 2 --headless -e multi_03 -p multi_03/multi_03.scenic -s emab -m scenic.simulators.carla.model