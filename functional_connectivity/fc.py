#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------
# @Author : Ning An        @Email : Ning An <ninganme0317@gmail.com>
import os.path

import nibabel as nib
import numpy as np


def cal_pearsonr(x: np.ndarray, y: np.ndarray):
    """
    same as pearsonr(x, y[0])
    :param x:
    :param y:
    :return:
    """
    # from scipy.stats import pearsonr
    # pearsonr(x, y[0])

    x_mean = x.mean()
    x_std = x.std()
    y_mean = y.mean(axis=1)
    y_std = y.std(axis=1)
    top = (((x - x_mean)[np.newaxis]) * (y - y_mean[..., np.newaxis])).mean(axis=1)
    bottom = (x_std * y_std)
    r = top / (bottom + 1e-10)
    return r


def fisherz(x: np.ndarray, inverse=False):
    """
    fisherz and its inverse
    :param x: r or z
    :param inverse: if True: transform z to r
    :return:
    """
    if not inverse:
        return np.arctanh(x)
    else:
        return np.tanh(x)


def volume_roi_and_whole_brain_fc(mri_files, roi_file, fc_file, num=-1, use_fisherz=False):
    """
    calculate volume fc
    :param mri_files: fmri files
    :param roi_file: roi file
    :param fc_file: fc file
    :param num: how many files to use for cal pearsonr
    :param use_fisherz: use fisherz or not
    :return:
    """
    roi_img = nib.load(roi_file)
    roi = roi_img.get_fdata()[..., 0] > 0

    data_mri_cat = None
    for mri_file in mri_files[0:num]:
        img = nib.load(mri_file)
        data_mri = img.get_fdata()
        data_mri_cat = data_mri if data_mri_cat is None else np.concatenate([data_mri_cat, data_mri], axis=3)

    data_roi = data_mri_cat[roi].mean(axis=0)

    index = data_mri_cat.astype(bool).sum(axis=3) > 0
    fc_volume = cal_pearsonr(data_roi, data_mri_cat[index])

    if use_fisherz:
        fc_volume = fisherz(fc_volume)

    fc = np.zeros_like(roi, dtype=float)
    fc[index] = fc_volume

    fc_img = nib.Nifti1Image(fc[..., np.newaxis], roi_img.affine, roi_img.header)
    nib.save(fc_img, fc_file)


def get_surface_mri_data(files: list):

    data_cat = None
    files.sort()
    for mri_file in files:
        mri_f = nib.load(mri_file)
        mri_data = mri_f.get_fdata().reshape(-1, mri_f.shape[-1], order='F')
        data_cat = mri_data if data_cat is None else np.concatenate([data_cat, mri_data], axis=1)
    return data_cat


def surface_seed_and_whole_brain_fc(mri_files, lh_seeds, rh_seeds, fc_dir, num=-1, use_fisherz=False):
    """
    calculate volume fc
    :param mri_files: fmri files
    :param lh_seeds: left hemi seeds
    :param rh_seeds: right hemi seeds
    :param fc_dir: fc dir
    :param num: how many files to use for cal pearsonr
    :param use_fisherz: use fisherz or not
    :return:
    """
    files_lh = [mri_file for mri_file in mri_files if 'lh.' in mri_file][:num]
    files_rh = [mri_file.replace('lh.', 'rh.') for mri_file in files_lh]
    data_lh = get_surface_mri_data(files_lh)
    data_rh = get_surface_mri_data(files_rh)

    seeds_data = [(f'lh{seed}', data_lh[seed]) for seed in lh_seeds]
    rh_seed_data = [(f'rh{seed}', data_rh[seed]) for seed in rh_seeds]

    seeds_data.extend(rh_seed_data)

    for seed, data_seed in seeds_data:
        fc_lh = cal_pearsonr(data_seed, data_lh)
        fc_rh = cal_pearsonr(data_seed, data_rh)

        fc_lh[np.isnan(fc_lh)] = 0
        fc_rh[np.isnan(fc_rh)] = 0

        if use_fisherz:
            fc_lh = fisherz(fc_lh)
            fc_rh = fisherz(fc_rh)

        fc_lh_img = nib.Nifti1Image(fc_lh, np.eye(4))
        nib.save(fc_lh_img, os.path.join(fc_dir, f'lh.{seed}.whole_brain.nii.gz'))
        fc_rh_img = nib.Nifti1Image(fc_rh, np.eye(4))
        nib.save(fc_rh_img, os.path.join(fc_dir, f'rh.{seed}.whole_brain.nii.gz'))

        # nib.save(nib.MGHImage(fc_lh.astype(np.float32), np.eye(4)), os.path.join(fc_dir, f'lh.{seed}.whole_brain.mgz'))
        # nib.save(nib.MGHImage(fc_rh.astype(np.float32), np.eye(4)), os.path.join(fc_dir, f'rh.{seed}.whole_brain.mgz'))
        # nib.freesurfer.write_morph_data(os.path.join(fc_dir, f'lh.{seed}.whole_brain.sulc'), fc_lh)
        # nib.freesurfer.write_morph_data(os.path.join(fc_dir, f'rh.{seed}.whole_brain.sulc'), fc_rh)


if __name__ == '__main__':
    from result_files.preprocess import Preprocess

    '/home/anning/workspace/FC_Regis/FCmap/BSC_rest'
    p_path = '/home/anning/workspace/FC_Regis/FCmap/BSC_rest'
    sub = 'BSC19_AnNing'
    ses = '2022-09-06-09-49-20-BSC1902'
    pp = Preprocess(project_path=p_path, subject_name=sub, session_name=ses)

    # # cal volume fc
    # vol_files = pp.get_files('*rest_reorient_skip_faln_mc_g1000000000_bpss_resid_FS1mm_FS2mm_sm6_subrun0.nii.gz',
    #                          dir_name='vol')
    # roi_name = 'PCC'
    # roif = f'/home/anning/workspace/FC_Regis/FCmap/vol/script/{roi_name}_Brain.1.100.1.download_subjects_sorted1002.txt.2mm.nii.gz'
    # fcf = f'/home/anning/workspace/FC_Regis/FCmap/vol/script/{roi_name}_FC.nii.gz'
    # n = 5
    # volume_roi_and_whole_brain_fc(vol_files, roif, fcf, num=n, use_fisherz=True)

    # cal surface fc
    surf_files = pp.get_files('*sm6_fsaverage4.nii.gz',
                              dir_name='surf')
    l_seeds = [1803, 644]
    r_seeds = [355, 220]
    out_path = f'/home/anning/workspace/FC_Regis/FCmap/surf/fc'
    surface_seed_and_whole_brain_fc(surf_files, l_seeds, r_seeds, out_path, num=5, use_fisherz=True)
