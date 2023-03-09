##  The Preparation  before Training

Firstly, you need to change CLASSES in `mmrotate/datasets`, **for example:**

```
    # DOTA
    CLASSES = ('plane', 'baseball-diamond', 'bridge', 'ground-track-field',
                'small-vehicle', 'large-vehicle', 'ship', 'tennis-court',
                'basketball-court', 'storage-tank', 'soccer-ball-field',
                'roundabout', 'harbor', 'swimming-pool', 'helicopter')
    # HRSC2016
    CLASSES = ('ship',)
    # UCSA
    CLASSES = ('airplane', 'car')
    # DIOR
    CLASSES = ('airplane', 'airport', 'baseballfield', 'basketballcourt', 'bridge', 'chimney', 
               'Expressway-Service-area', 'Expressway-toll-station', 'dam', 'golffield','groundtrackfield',
               'harbor', 'overpass', 'ship',  'stadium', 'storagetank', 'tenniscourt', 'trainstation', 
               'vehicle', 'windmill')
```

Second, you need to modify **the dataset path** and related configuration in `configs/_base_/datasets/dotav1.py`, such as `img_scale`, `samples_per_gpu`, etc. 

```
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=8,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'Train/labelTxt/',
        img_prefix=data_root + 'Train/images/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'Test/labelTxt/',
        img_prefix=data_root + 'Test/images/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        # ann_file=data_root + 'test/images/',
        ann_file=data_root + 'Test/labelTxt/',
        img_prefix=data_root + 'Test/images/',
        pipeline=test_pipeline))
```

Finally, you need to modify `num_classes` in your `model config` file to match your dataset, such as:

Changes made in `configs/rotated_fcos/rotated_fcos_r50_fpn_1x_dior_le90.py`

```
    bbox_head=dict(
        type='RotatedFCOSHead',
        num_classes=20,
        in_channels=256,
        stacked_convs=4,
        feat_channels=256,
        strides=[8, 16, 32, 64, 128],
        center_sampling=True,
        center_sample_radius=1.5,
        norm_on_bbox=True,
        centerness_on_reg=True,
        separate_angle=False,
        scale_angle=True,
        bbox_coder=dict(
            type='DistanceAnglePointCoder', angle_version=angle_version),
```



