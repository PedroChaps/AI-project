for test in testes-takuzu/input*; do

    echo "running test $test...";
    echo "";
    
    output=$(/bin/time -f "%E segundos" python3 takuzu.py < $test > /dev/null);
    echo $output;
    
done