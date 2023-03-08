## Dataset repare

1. Download DIOR [Google Drive](https://drive.google.com/drive/folders/1UdlgHk49iu6WpcJ5467iT-UqNPpx__CC) .

2. Unzip dataset package into your root_dir, and rename the folder to `DIOR-R`. Then, you can get folder as follow:

   ```
   DIOR-R
   └───JPEGImages-trainval
   │   │   00001.jpg
   │   │   00002.jpg
   │   │	...
   │   └───11725.jpg
   └───JPEGImages-test
   │   │   11725.jpg
   │   │   11726.jpg
   │   │	...
   │   └───23463.jpg
   └───Annotations
   |   └───Oriented Bounding Boxes
   │   │   |	00001.xml
   │   │   |	00002.xml
   │   │	|	...
   │   |	└───23463.xml    
   |   └───Oriented Bounding Boxes
   ```

3. Run `dior-a2dota.py `(modify the dataset dir to your own), and you will obtain directory as follow:

```
DIOR-R
└───JPEGImages-trainval
│   │   00001.jpg
│   │   00002.jpg
│   │	...
│   └───11725.jpg
└───JPEGImages-test
│   │   11725.jpg
│   │   11726.jpg
│   │	...
│   └───23463.jpg
└───Annotations
|   └───Oriented Bounding Boxes
│   │   |	00001.xml
│   │   |	00002.xml
│   │	|	...
│   |	└───23463.xml    
|   └───Oriented Bounding Boxes

```

5. Train, eval and test you model according to `ImageSets` settings.

**notes**: The integrated dataset contains 1510 images, with train set 755, val set 302, test set 452(following DOTA division 5:2:3). Files are numbered from 1-1510, in which `1-510` are cars, `511-1510` are airplanes. Besides, classname is attached to label file in format of `classname x1 y1 x2 y2 x3 y3 x4 y4 theta lx ly w h ` ,

for example:

```
car  2.763971e+02	9.125021e+01	2.911375e+02	3.823406e+01	3.308891e+02	4.928647e+01	3.161486e+02	1.023026e+02	1.055379e+02	2.787673e+02	3.876027e+01	4.975157e+01	6.301615e+01	
car  3.002141e+02	1.003123e+02	3.209637e+02	4.665470e+01	3.566901e+02	6.047021e+01	3.359405e+02	1.141279e+02	1.111416e+02	3.055889e+02	4.856245e+01	4.572642e+01	6.365764e+01	
...
```



**Reference**: [ming71/UCAS-AOD-benchmark](https://github.com/ming71/UCAS-AOD-benchmark)

