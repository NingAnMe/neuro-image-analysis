import nibabel as nib
import numpy as np
import cv2


def create_contours_image(mni152_aparc_file, output_file):
    img = nib.load(mni152_aparc_file)
    affine = img.affine
    header = img.header
    data = img.get_fdata()
    data_threshold = np.zeros_like(data, dtype=np.uint8)
    data_threshold[data == 1] = 2
    data_output = np.zeros_like(data, dtype=np.uint8)
    for x in range(data.shape[2]):
        ret, binary = cv2.threshold(data_threshold[:, :, x], 1, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.drawContours(cv2.cvtColor(data_output[:, :, x], cv2.COLOR_GRAY2BGR), contours[:1], -1, (255, 255, 255), 1)
        data_output[:, :, x][img[:, :, 0] > 0] = 1
    img_out = nib.Nifti1Image(data_output, affine=affine, header=header)
    nib.save(img_out, output_file)


if __name__ == '__main__':
    mni152_seg_file = '/usr/local/fsl/data/standard/MNI152_T1_1mm_brain_mask.nii.gz'
    contours_MNI152 = 'MNI152_T1_1mm_Brain_contours.nii.gz'
    create_contours_image(mni152_seg_file, contours_MNI152)
