import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import math


def plot_anat(anat_file):
    # 加载 MRI 数据
    # img = nib.load('anat.nii.gz')
    img = nib.load(anat_file)
    data = img.get_fdata()

    # 设置子图参数
    n_rows = 4
    n_cols = 12

    # 计算间隔
    interval_x = math.ceil(data.shape[0] / (n_rows * n_cols))
    interval_y = math.ceil(data.shape[1] / (n_rows * n_cols))
    interval_z = math.ceil(data.shape[2] / (n_rows * n_cols))

    # 绘制沿着 x 轴的图像
    fig_x, ax_x = plt.subplots(n_rows, n_cols, figsize=(12, 9))
    for i in range(n_rows):
        for j in range(n_cols):
            slice_index = i * n_cols + j
            slice_index *= interval_x
            if slice_index < data.shape[0]:
                slice_data = np.rot90(data[slice_index, :, :])
                ax_x[i, j].imshow(slice_data, cmap='gray')
                ax_x[i, j].set_title(f'X={slice_index}')
                ax_x[i, j].axis('off')
            else:
                ax_x[i, j].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

    plt.show()

    # 绘制沿着 y 轴的图像
    fig_y, ax_y = plt.subplots(n_rows, n_cols, figsize=(12, 9))
    for i in range(n_rows):
        for j in range(n_cols):
            slice_index = i * n_cols + j
            slice_index *= interval_y
            if slice_index < data.shape[1]:
                slice_data = np.rot90(data[:, slice_index, :])
                ax_y[i, j].imshow(slice_data, cmap='gray')
                ax_y[i, j].set_title(f'Y={slice_index}')
                ax_y[i, j].axis('off')
            else:
                ax_y[i, j].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

    plt.show()

    # 绘制沿着 z 轴的图像
    fig_z, ax_z = plt.subplots(n_rows, n_cols, figsize=(12, 9))
    for i in range(n_rows):
        for j in range(n_cols):
            slice_index = i * n_cols + j
            slice_index *= interval_z
            if slice_index < data.shape[2]:
                slice_data = np.rot90(data[:, :, slice_index])
                ax_z[i, j].imshow(slice_data, cmap='gray')
                ax_z[i, j].set_title(f'Z={slice_index}')
                ax_z[i, j].axis('off')
            else:
                ax_z[i, j].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

    plt.show()


def plot_func(func_file):
    # 加载 MRI 数据
    # img = nib.load('func.nii.gz')
    img = nib.load(func_file)
    data = img.get_fdata()

    # 设置子图参数
    n_rows = 4
    n_cols = 12

    # 计算间隔
    interval_x = math.ceil(data.shape[0] / (n_rows * n_cols))
    interval_y = math.ceil(data.shape[1] / (n_rows * n_cols))
    interval_z = math.ceil(data.shape[2] / (n_rows * n_cols))

    # 绘制沿着 x 轴的图像
    fig_x, ax_x = plt.subplots(n_rows, n_cols, figsize=(12, 9))
    for i in range(n_rows):
        for j in range(n_cols):
            slice_index = i * n_cols + j
            slice_index *= interval_x
            if slice_index < data.shape[0]:
                slice_data = np.rot90(data[slice_index, :, :, 0])
                ax_x[i, j].imshow(slice_data, cmap='gray')
                ax_x[i, j].set_title(f'X={slice_index}')
                ax_x[i, j].axis('off')
            else:
                ax_x[i, j].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

    plt.show()

    # 绘制沿着 y 轴的图像
    fig_y, ax_y = plt.subplots(n_rows, n_cols, figsize=(12, 9))
    for i in range(n_rows):
        for j in range(n_cols):
            slice_index = i * n_cols + j
            slice_index *= interval_y
            if slice_index < data.shape[1]:
                slice_data = np.rot90(data[:, slice_index, :, 0])
                ax_y[i, j].imshow(slice_data, cmap='gray')
                ax_y[i, j].set_title(f'Y={slice_index}')
                ax_y[i, j].axis('off')
            else:
                ax_y[i, j].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

    plt.show()

    # 绘制沿着 z 轴的图像
    fig_z, ax_z = plt.subplots(n_rows, n_cols, figsize=(12, 9))
    for i in range(n_rows):
        for j in range(n_cols):
            slice_index = i * n_cols + j
            slice_index *= interval_z
            if slice_index < data.shape[2]:
                slice_data = np.rot90(data[:, :, slice_index, 0])
                ax_z[i, j].imshow(slice_data, cmap='gray')
                ax_z[i, j].set_title(f'Z={slice_index}')
                ax_z[i, j].axis('off')
            else:
                ax_z[i, j].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=-0.2, hspace=-0.2)

    plt.show()


if __name__ == '__main__':

    plot_anat('mri_data/anat.nii.gz')
    plot_func('mri_data/func.nii.gz')
