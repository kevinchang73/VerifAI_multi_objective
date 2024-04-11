iteration=5
scenario='multi_02'
log_file='result.log'
order=alternate

rm $scenario/outputs/*.txt
rm $scenario/outputs/*.png
python $scenario/$scenario.py -n $iteration --headless -e $scenario -sp $scenario/$scenario.scenic -gp $scenario/$scenario.sgraph -rp $scenario/$scenario\_spec.py -s demab -o $scenario/outputs --single-graph > $log_file
for i in $(seq 0 $(($iteration-1)));
do
    python $scenario/util/$scenario\_plot_traj.py $scenario/outputs/$scenario\_traj_$i.txt
done
python $scenario/util/$scenario\_collect_result.py $log_file single $order
