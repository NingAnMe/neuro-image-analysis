#! /usr/bin/env python3
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


def get_surface_roi(hemi, voxel_seed, surface, ring, output_dir):
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
        roi_file = os.path.join(output_dir, f'ROI_hemi-{hemi}_seed-{voxel_seed}_{ring_num}-ring.roi')
        nib.freesurfer.write_morph_data(roi_file, roi)
        print(f'>>> {roi_file}')


def load_surface_roi(roi_file):
    roi = nib.freesurfer.read_morph_data(roi_file) == 1
    return roi


if __name__ == '__main__':
    freesurfer_home = '/usr/local/freesurfer600'

    hemi = 'lh'
    roi_seed = 33144
    fs_res = 'fsaverage6'
    ring_num = 3  # from 1 to ring_num
    result_path = ''


    geo_surface = f'{freesurfer_home}/subjects/{fs_res}/surf/{hemi}.white'  # any white、pial、sphere
    get_surface_roi(hemi, roi_seed, geo_surface, ring_num, result_path)
