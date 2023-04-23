import numpy as np
import nibabel as nib
from nilearn import masking, plotting, image


def calculate_fmri_snr(file_path, mask=True, figure=False, out_file=None):
    """
    计算fMRI数据的信噪比（SNR）
    参数：
    file_path: str, fMRI数据文件路径
    mask: bool, 是否对数据应用掩码，默认为True
    figure: bool, 是否输出SNR图，默认为False
    out_file: str, 保存SNR数据的输出文件路径，默认为None
    返回值：
    median_tsnr: float，计算出的fMRI数据的SNR的中位数
    """
    print(f"INFO: computing TSNR for {file_path}")

    # 加载数据
    img = image.load_img(file_path)

    # 应用掩码
    if mask:
        print("INFO: computing EPI mask")
        mask = masking.compute_epi_mask(img)
    else:
        # 如果没有掩码，则至少删除0值
        nonzeros = (img.get_fdata().sum(axis=3) != 0).astype(int)
        mask = nib.Nifti1Image(nonzeros, affine=img.affine)

    img_2d = masking.apply_mask(img, mask)

    # 计算SNR
    tsnr = np.mean(img_2d, axis=0) / np.std(img_2d, axis=0)
    mean_tsnr = np.mean(tsnr)
    print(f"INFO: mean TSNR = {mean_tsnr:.3f}")

    # 输出SNR图
    if figure:
        # 重新创建3D nifti图像并用Nilearn绘制
        tsnr_img = masking.unmask(tsnr, mask_img=mask)
        plotting.plot_epi(tsnr_img)

    if out_file is not None:
        print(f"INFO: Saving TSNR data to {out_file}")
        nib.save(masking.unmask(tsnr, mask_img=mask), out_file)

    return mean_tsnr


if __name__ == '__main__':
    calculate_fmri_snr('../demo/mri_data/func.nii.gz', figure=True, out_file='func_snr.nii.gz')
