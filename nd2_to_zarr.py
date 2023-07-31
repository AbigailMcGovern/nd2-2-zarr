from nd2reader import ND2Reader
from nd2_dask.nd2_reader import nd2_reader
import zarr
import json
import numpy as np
from pathlib import Path
import os


def read_nd2_plus_meta(image_path, save_dir):
    data = ND2Reader(image_path)
    meta = data.metadata
    del data
    layerlist = nd2_reader(image_path)
    images = [l[0].compute() for l in layerlist]
    images = np.stack(images)
    meta['scale'] = layerlist[0][1]['scale']
    meta['date'] = meta['date'].strftime("%m/%d/%Y, %H:%M:%S")
    meta['frames'] = meta['frames'].stop
    meta['z_levels'] = meta['z_levels'].stop
    json_object = json.dumps(meta, indent=4)
    meta_path = os.path.join(save_dir, Path(image_path).stem + '_meta.json')
    with open(meta_path, "w") as outfile:
        outfile.write(json_object)
    save_path = os.path.join(save_dir, Path(image_path).stem + '.zarr')
    zarr.save(save_path, images)




p = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/human/nd2s/201118_hTR4_DMSO_3000s_.nd2'
sd = '/Users/abigailmcgovern/Data/iterseg/invitro_platelets/ACBD/human/zarrs'

read_nd2_plus_meta(p, sd)