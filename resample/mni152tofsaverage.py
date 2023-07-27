import os
from neuromaps import transforms


def transform_mni152_to_fsaverage(input_file, lh_output_file, rh_output_file, fsavg_density='41k', method='linear'):
    """Projects img in MNI152 space to fsaverage surface

Parameters
:
img (str or os.PathLike or niimg_like) – Image in MNI152 space to be projected

fsavg_density ({'3k', '10k', '41k', '164k'}, optional) – Desired output density of fsaverage surface. Default: ‘41k’

method ({'nearest', 'linear'}, optional) – Method for projection. Specify ‘nearest’ if img is a label image. Default: ‘linear’

Returns
:
fsaverage – Projected img on fsaverage surface

Return type
:
(2,) tuple-of-nib.GiftiImage
    """
    assert os.path.isfile(input_file)
    lh_gii, rh_gii = transforms.mni152_to_fsaverage(input_file, fsavg_density=fsavg_density, method=method)
    lh_gii_file = 'lh.' + os.path.basename(input_file) + '.func.gii'
    rh_gii_file = 'rh.' + os.path.basename(input_file) + '.func.gii'
    lh_gii.to_filename(lh_gii_file)
    rh_gii.to_filename(rh_gii_file)
    os.system(f'mri_convert {lh_gii_file} {lh_output_file}')
    os.system(f'mri_convert {rh_gii_file} {rh_output_file}')
    os.remove(lh_gii_file)
    os.remove(rh_gii_file)


if __name__ == '__main__':
    mni152_file = ''
    lh_fsaverage = 'rh.sulc'
    rh_fsaverage = 'lh.sulc'
    fsavg_density = '41k'  # '3k', '10k', '41k', '164k'
    methods = 'nearest'  # 'nearest', 'linear'
    transform_mni152_to_fsaverage(mni152_file, lh_fsaverage, rh_fsaverage, fsavg_density, methods)
