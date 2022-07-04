SOURCE_BASE_PATH="/MapReduce"
INPUT_HADOOP_DIR="/MapReduce/data/input"
OUTPUT_HADOOP_DIR="/MapReduce/data/output"
HADOOP_STREAMING_PATH="${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

hdfs dfs -test -d ${INPUT_HADOOP_DIR}
if [ $? -eq 0 ];
  then
    echo "Remove ${INPUT_HADOOP_DIR}"
    hdfs dfs -rm -r ${INPUT_HADOOP_DIR}
fi

hdfs dfs -test -d ${OUTPUT_HADOOP_DIR}
if [ $? -eq 0 ];
  then
    echo "Remove ${OUTPUT_HADOOP_DIR}"
    hdfs dfs -rm -r ${OUTPUT_HADOOP_DIR}
fi

test -d ${SOURCE_BASE_PATH}/data/output
if [ $? -eq 0 ];
  then
    echo "Remove ${SOURCE_BASE_PATH}/data/output"
    rm -rf ${SOURCE_BASE_PATH}/data/output
fi

#====================================================================================
#====================================================================================
#====================================================================================

hdfs dfs -mkdir -p /MapReduce/bag_for_cat 	 # Для конкатенации файлов
hdfs dfs -mkdir -p ${INPUT_HADOOP_DIR}/stage_1 # Для входного файла последовательности: ratings.csv


hdfs dfs -copyFromLocal ${SOURCE_BASE_PATH}/data/input/stage_1/* ${INPUT_HADOOP_DIR}/stage_1

chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_1.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_1.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_2.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_2.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_3.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_3.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_4.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_4.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_5.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_5.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_6.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_6.py


#====================================================================================
#====================================================================================
#====================================================================================

hadoop_streaming_arguments="\
  -D mapred.reduce.tasks=3 \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper_1.py -reducer src/reducer_1.py \
  -input ${INPUT_HADOOP_DIR}/stage_1 -output ${OUTPUT_HADOOP_DIR}/stage_1 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

mkdir /MapReduce/bag_for_cat
hdfs dfs -get ${OUTPUT_HADOOP_DIR}/stage_1/* /MapReduce/bag_for_cat/
rm /MapReduce/bag_for_cat/_SUCCESS
cat /MapReduce/bag_for_cat/* > /MapReduce/bag_for_cat/mean_ratings.txt



hadoop_streaming_arguments="\
  -D mapred.reduce.tasks=3 \
  -files ${SOURCE_BASE_PATH}/src,/MapReduce/bag_for_cat/mean_ratings.txt \
  -mapper src/mapper_2.py -reducer src/reducer_2.py \
  -input ${INPUT_HADOOP_DIR}/stage_1 -output ${OUTPUT_HADOOP_DIR}/stage_2 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}
rm -r bag_for_cat



hadoop_streaming_arguments="\
  -D mapred.reduce.tasks=3 \
  -files ${SOURCE_BASE_PATH}/src \
  -mapper src/mapper_3.py -reducer src/reducer_3.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_2 -output ${OUTPUT_HADOOP_DIR}/stage_3 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}
hdfs dfs -cp ${INPUT_HADOOP_DIR}/stage_1/ratings.csv ${OUTPUT_HADOOP_DIR}/stage_3
hdfs dfs -rm ${OUTPUT_HADOOP_DIR}/stage_3/_SUCCESS



hadoop_streaming_arguments="\
  -D mapred.reduce.tasks=10 \
  -files ${SOURCE_BASE_PATH}/src,${INPUT_HADOOP_DIR}/stage_1/ratings.csv \
  -mapper src/mapper_4.py -reducer src/reducer_4.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_3 -output ${OUTPUT_HADOOP_DIR}/stage_4 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}



hadoop_streaming_arguments="\
  -D mapred.reduce.tasks=3 \
  -files ${SOURCE_BASE_PATH}/src \
  -mapper src/mapper_5.py -reducer src/reducer_5.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_4 -output ${OUTPUT_HADOOP_DIR}/stage_5 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}



hadoop_streaming_arguments="\
  -D mapred.reduce.tasks=3 \
  -files ${SOURCE_BASE_PATH}/src,${INPUT_HADOOP_DIR}/movies.csv \
  -mapper src/mapper_6.py -reducer src/reducer_6.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_5 -output ${OUTPUT_HADOOP_DIR}/stage_6 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

hdfs dfs -mkdir /MapReduce/data/output/final
mkdir /MapReduce/bag_for_cat2
hdfs dfs -get ${OUTPUT_HADOOP_DIR}/stage_6/* /MapReduce/bag_for_cat2/
rm /MapReduce/bag_for_cat2/_SUCCESS
cat /MapReduce/bag_for_cat/* > /MapReduce/bag_for_cat2/recommendations.txt
hdfs dfs -put /MapReduce/bag_for_cat2/recommendations.txt /MapReduce/data/output/final/
rm -r /MapReduce/bag_for_cat2

#hdfs dfs -rm -r ${INPUT_HADOOP_DIR}
#hdfs dfs -rm -r ${OUTPUT_HADOOP_DIR}
