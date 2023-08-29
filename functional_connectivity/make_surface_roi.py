# python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author : Ning An        @Email : Ning An <ninganme0317@gmail.com>
import os.path

import nibabel as nib
import numpy as np


def get_index_in_faces(voxel: int, faces: np.ndarray):
    face_true = faces == voxel
    face_index = np.sum(face_true, axis=1) > 0
    return np.unique(faces[face_index])


def get_surface_roi(voxel_seed, surface, ring, output_dir):
    xyzs, faces = nib.freesurfer.read_geometry(surface)

    assert ring <= 10

    voxels = np.array([voxel_seed])
    for ring_num in range(1, ring + 1):
        neighbors = None
        for voxel in voxels:
            ns = get_index_in_faces(voxel, faces)
            neighbors = ns if neighbors is None else np.append(neighbors, ns)
        voxels = np.sort(np.unique(neighbors))
        print(voxels)
        roi = np.zeros((len(xyzs)), dtype=int)
        roi[voxels] = 1
        roi_file = os.path.join(output_dir, f'ROI_seed-{voxel_seed}_{ring_num}-ring.curv')
        nib.freesurfer.write_morph_data(roi_file, roi)


def load_surface_roi(roi_file):
    roi = nib.freesurfer.read_morph_data(roi_file) == 1
    return roi


if __name__ == '__main__':
    voxel_index_ = 33144
    surface_ = '/usr/local/freesurfer600/subjects/fsaverage6/surf/lh.white'  # any white、pial、sphere
    ring_ = 10  # 1 or 2

    result_path = ''
    get_surface_roi(voxel_index_, surface_, ring_, result_path)
