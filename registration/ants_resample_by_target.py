import argparse
import ants
"""reference
https://antspy.readthedocs.io/en/latest/registration.html

python ants_registration.py source_image.nii.gz target_image.nii.gz output_image.nii.gz
"""

# 创建一个命令行解析器
parser = argparse.ArgumentParser(description='ANTS registration script')

# 添加需要的命令行参数
parser.add_argument('--source_image', type=str, help='path to source image')
parser.add_argument('--target_image', type=str, help='path to target image')
parser.add_argument('--output_image', type=str, help='path to output image')
parser.add_argument('--interp_type', type=str, help='interp type: default is for float value, "genericLabel" for label value')

# 解析命令行参数
args = parser.parse_args()

# 读取固定图像和移动图像
target_image = ants.image_read(args.target_image)
source_image = ants.image_read(args.source_image)

if args.interp_type is not None:
    resampled = ants.resample_image_to_target(source_image, target_image, interp_type=args.interp_type, verbose=True)
else:
    resampled = ants.resample_image_to_target(source_image, target_image, verbose=True)

# 将结果保存为 NIfTI 格式文件
ants.image_write(resampled, args.output_image)

# 将变换矩阵保存到文件中
print(f'<<< source_image {args.source_image}')
print(f'<<< target_image {args.target_image}')
print(f'>>> output_image {args.output_image}')
