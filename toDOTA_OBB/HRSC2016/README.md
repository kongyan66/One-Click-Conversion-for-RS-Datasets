## Dataset Prepare

1. Download HRSC2016 [Baidu Drive](https://pan.baidu.com/s/1DydeXOX3x-wB43tM8nRzcA)[9ozp] .

2. Unzip dataset package into your root dir. Then, you can get folder as follow:

   ```
   HRSC2016
   └───FullDataSet
   |   └───Annotations
   │   │   JPEGImages
   │   │   LandMask
   │   └───Segmentations
   └───ImageSets
   │   │   train.txt
   │   │   trainval.txt
   │   │	...
   │   └───val.txt
   └───Test
   |   └───AllImages
   │   │   |	100000003.bmp
   │   │   |	100000005.bmp
   │   │   |	...
   │   |   └─── 100001675.bmp 
   |   └───Annotations
   │   │   |	100000003.xml
   │   │   |	100000005.xml
   │   │   |	...
   │   |   └─── 100001675.xml 
   |   └───Segmentations
   └───Train
   |   └───AllImages
   |   └───Annotations
   |   └───Segmentations
   ```

3. Run `hrsc2dota.py `(modify the dataset dir to your own)

   ```
   test_path = '/home/z/code/kch/RS_Dataset/hrsc2016/Test'
   train_path = '/home/z/code/kch/RS_Dataset/hrsc2016/Train'
   ```

   Then a new folder labelTxt will be generated under the Test and Train files:

   ```
      └───Test
      |   └───AllImages
      |   └───Annotations
      |   └───Segmentations
      |   └───labelTxt
      └───Train
      |   └───AllImages
      |   └───Annotations
      |   └───Segmentations
      |   └───labelTxt
   ```

   





