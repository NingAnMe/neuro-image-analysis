import nibabel as nib
import numpy as np


def make_volume_roi_file(template_file: str, template_file_res: int, roi_xyz: list, size: int, roi_file: str):
    """
    make roi of template file
    :param template_file: template file for index of roi
    :param template_file_res: mm resolution of template file
    :param roi_xyz: index of roi
    :param size: mm size of roi
    :param roi_file: output file
    :return:
    """
    img = nib.load(template_file)
    shape = img.shape
    x_range = np.arange(shape[0])
    y_range = np.arange(shape[1])
    z_range = np.arange(shape[2])
    nx, ny, nz = np.meshgrid(x_range, y_range, z_range, indexing='ij')
    distance = (nx - roi_xyz[0]) ** 2 + (ny - roi_xyz[1]) ** 2 + (nz - roi_xyz[2]) ** 2
    threshold = (size / template_file_res)
    roi_index = distance <= threshold ** 2
    roi_img = nib.Nifti1Image(roi_index[..., np.newaxis], img.affine, img.header)
    nib.save(roi_img, roi_file)


if __name__ == '__main__':
    tf = '/home/anning/workspace/FC_Regis/FCmap/vol/script/Brain.1.100.1.download_subjects_sorted1002.txt.2mm.nii.gz'
    tfr = 2
    rxyz = [64, 51, 37]
    s = 6
    roi_name = 'PCC'
    rf = f'/home/anning/workspace/FC_Regis/FCmap/vol/script/{roi_name}_Brain.1.100.1.download_subjects_sorted1002.txt.2mm.nii.gz'
    make_volume_roi_file(tf, tfr, rxyz, s, rf)
