import nibabel as nib
import numpy as np


def cal_pearsonr(x, y):
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
    r = top / bottom
    return r


def fisherz(a):
    return np.arctanh(a)


def volume_fc(mri_files, roi_file, fc_file, num=-1, use_fisherz=False):
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


if __name__ == '__main__':
    from result_files.preprocess import Preprocess

    '/home/anning/workspace/FC_Regis/FCmap/BSC_rest'
    p_path = '/home/anning/workspace/FC_Regis/FCmap/BSC_rest'
    sub = 'BSC19_AnNing'
    ses = '2022-09-06-09-49-20-BSC1902'
    pp = Preprocess(project_path=p_path, subject_name=sub, session_name=ses)
    vol_files = pp.get_files('*rest_reorient_skip_faln_mc_g1000000000_bpss_resid_FS1mm_FS2mm_sm6_subrun0.nii.gz', dir_name='vol')

    print()

    roi_name = 'PCC'
    rf = f'/home/anning/workspace/FC_Regis/FCmap/vol/script/{roi_name}_Brain.1.100.1.download_subjects_sorted1002.txt.2mm.nii.gz'
    fcf = f'/home/anning/workspace/FC_Regis/FCmap/vol/script/{roi_name}_FC.nii.gz'
    n = 5

    volume_fc(vol_files, rf, fcf, num=n, use_fisherz=True)
