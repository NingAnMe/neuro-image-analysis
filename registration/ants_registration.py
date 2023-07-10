import sh
import argparse
import ants
"""reference
https://antspy.readthedocs.io/en/latest/registration.html

python ants_registration.py --moving_image moving_image.nii.gz --fixed_image fixed_image.nii.gz --output_image output_image.nii.gz --transform SyN  --output_transform transform.mat
"""

# 创建一个命令行解析器
parser = argparse.ArgumentParser(description='ANTS registration script')

# 添加需要的命令行参数
parser.add_argument('--moving_image', type=str, help='path to moving image')
parser.add_argument('--fixed_image', type=str, help='path to fixed image')
parser.add_argument('--output_image', type=str, help='path to output image')
parser.add_argument('--transform', type=str, default='SyN',
                    help='type of transform to use (default: SyN)')
parser.add_argument('--output_transform', type=str, default='transform.mat',
                    help='path to output transform file')

# 解析命令行参数
args = parser.parse_args()

# 读取固定图像和移动图像
fixed_image = ants.image_read(args.fixed_image)
moving_image = ants.image_read(args.moving_image)

# 进行图像配准
registration = ants.registration(fixed=fixed_image, moving=moving_image,
                                  type_of_transform=args.transform)

# 获取变换矩阵
transform_matrix = registration['fwdtransforms']

# 将变换应用到移动图像上
warped_image = ants.apply_transforms(fixed=fixed_image, moving=moving_image,
                                     transformlist=transform_matrix)

# 将结果保存为 NIfTI 格式文件
ants.image_write(warped_image, args.output_image)

# 将变换矩阵保存到文件中
print(f'>>> cp transform_matrix {transform_matrix} to {args.output_transform}')
sh.cp(transform_matrix, args.output_transform)
