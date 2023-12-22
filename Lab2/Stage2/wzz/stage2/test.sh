for cf_batch_size in 512 1024 2048
do
    for kg_batch_size in 1024 2048 4096
    do
    	for test_batch_size in 1024 2048 4096
    	do
    	    python3 ./main_Embedding_based.py $cf_batch_size $kg_batch_size $test_batch_size 32 32
    	done
    done
done

for embed_dim in 16 24 32 48 64
do
    for relation_dim in  16 24 32 48 64
    do
    	python3 ./main_Embedding_based.py 1024 2048 2048 $embed_dim $relation_dim
    done
done
