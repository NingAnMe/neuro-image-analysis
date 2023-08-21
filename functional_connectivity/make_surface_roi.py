# python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author : Ning An        @Email : Ning An <ninganme0317@gmail.com>

import nibabel as nib
import numpy as np


def get_index_in_faces(voxel: int, faces: np.ndarray):
    face_true = faces == voxel
    face_index = np.sum(face_true, axis=1) > 0
    return np.unique(faces[face_index])


def get_surface_roi(voxel, surface, ring, roi_file):
    xyzs, faces = nib.freesurfer.read_geometry(surface)
    voxels = get_index_in_faces(voxel, faces)

    assert ring in (1, 2)

    if ring == 2:
        voxel_tmp = voxels.tolist()

        for voxel in voxel_tmp:

            tmp = get_index_in_faces(voxel, faces)
            voxels = np.append(voxels, tmp)
    voxels = np.unique(voxels)
    print(voxels)
    roi = np.zeros((len(xyzs)), dtype=int)
    roi[voxels] = 1
    nib.freesurfer.write_morph_data(roi_file, roi)


def load_surface_roi(roi_file):
    roi = nib.freesurfer.read_morph_data(roi_file) == 1
    return roi


if __name__ == '__main__':
    voxel_index_ = 13
    surface_ = '/usr/local/freesurfer600/subjects/fsaverage/surf/lh.white'  # any white、pial、sphere
    ring_ = 2  # 1 or 2
    result = 'roi.curv'  # roi == 1, background == 0

    get_surface_roi(voxel_index_, surface_, ring_, result)
