import nibabel as nib
import numpy as np


def mp2rage_process(inv1_file, inv2_file, uni_file, out_file, reg=100):
    # loading data
    inv1_data = nib.load(inv1_file).get_fdata(dtype=np.float32)
    inv2_data = nib.load(inv2_file).get_fdata(dtype=np.float32)
    uni_img = nib.load(uni_file)
    uni_data = uni_img.get_fdata(dtype=np.float32)

    # convert uni_data to -0.5 --- 0.5 scale
    uni_convert = np.zeros_like(uni_data)
    integer_format = False
    if np.min(uni_data) >= 0 and np.max(uni_data) >= 0.51:
        uni_convert = (uni_data - np.max(uni_data) / 2) / np.max(uni_data)
        integer_format = True

    # Give the correct polarity to INV1
    inv1_data = np.sign(uni_convert) * inv1_data
    uni_convert_denominator = uni_convert.copy()
    uni_convert_denominator[uni_convert_denominator == 0] = np.inf
    inv1_pos = (-1 * inv2_data + np.sqrt(np.square(inv2_data) - 4 * uni_convert *
                                         (np.square(inv2_data) * uni_convert))) / (-2 * uni_convert_denominator)
    inv1_pos[np.isnan(inv1_pos)] = 0

    inv1_neg = (-1 * inv2_data - np.sqrt(np.square(inv2_data) - 4 * uni_convert *
                                         (np.square(inv2_data) * uni_convert))) / (-2 * uni_convert_denominator)
    inv1_neg[np.isnan(inv1_neg)] = 0

    inv1_pos_index = np.abs(inv1_data - inv1_pos) > np.abs(inv1_data - inv1_neg)
    inv1_data[inv1_pos_index] = inv1_neg[inv1_pos_index]

    inv1_neg_index = np.abs(inv1_data - inv1_pos) <= np.abs(inv1_data - inv1_neg)
    inv1_data[inv1_neg_index] = inv1_pos[inv1_neg_index]

    # lambda calculation
    noise_level = reg * np.mean(inv2_data[-10:, :, -10:])
    t1w = (np.conj(inv1_data) * inv2_data - np.square(noise_level)) / \
          (np.square(inv1_data) + np.square(inv2_data) + 2 * np.square(noise_level))
    # convert the final image to uint (if necessary)
    if integer_format:
        t1w = np.round(4095 * (t1w + 0.5))

    t1w_img = nib.Nifti1Image(t1w, uni_img.affine, uni_img.header)
    nib.save(t1w_img, out_file)


if __name__ == '__main__':
    """
    combine multi MP2RAGE file to one file, and which can be preprocessed by FreeSurfer 
    """


    inv1_path = 'T1_MP2RAGE_SAG_P3_ISO_INV1_0005_t1_mp2rage_sag_p3_iso_20220503132751_5.nii'
    inv2_path = 'T1_MP2RAGE_SAG_P3_ISO_INV2_0006_t1_mp2rage_sag_p3_iso_20220503132751_6.nii'
    uni_path = 'T1_MP2RAGE_SAG_P3_ISO_UNI_IMAGES_0008_t1_mp2rage_sag_p3_iso_20220503132751_8.nii'
    out_file = 'T1_MP2RAGE_process.nii.gz'
    reg = 100
    mp2rage_process(inv1_path, inv2_path, uni_path, out_file, reg)
